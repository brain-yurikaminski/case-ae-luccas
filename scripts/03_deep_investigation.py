import os
import duckdb
import pandas as pd
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "dados")

con = duckdb.connect(database=":memory:")
tables = [
    "cards", "carts", "crm_events", "dim_operation",
    "order_items", "orders", "points_ledger", "redeemed_points",
    "relatorio_mensal_cliente"
]
for t in tables:
    filepath = os.path.join(DATA_DIR, f"{t}.csv")
    con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{filepath}')")

print("==================================================")
print("INVESTIGAÇÃO 1: AFIRMAÇÃO DO OPERADOR (PIX A R$ 0,016)")
print("==================================================")
# Vamos comparar mês a mês order_items (com status) vs relatorio_mensal_cliente
query_pix_compare = """
WITH pix_items AS (
    SELECT 
        strftime(oi.created_at, '%Y-%m') as mes,
        oi.status,
        count(distinct oi.order_id) as qtd_pedidos,
        count(*) as qtd_items,
        sum(oi.paid_points) as paid_points,
        sum(oi.product_value) as product_value,
        sum(oi.paid_currency) as paid_currency,
        sum(oi.refunded_points) as refunded_points
    FROM order_items oi
    WHERE oi.category_macro = 'Cashback' AND oi.product_type = 'TRANSFERENCIA'
    GROUP BY 1, 2
)
SELECT * FROM pix_items ORDER BY mes, status;
"""
print(con.execute(query_pix_compare).fetchdf().to_string())

print("\nComparando apenas APROVADO + FINALIZADO_COM_SUCESSO:")
query_pix_approved = """
WITH pix_valid AS (
    SELECT 
        strftime(oi.created_at, '%Y-%m') as mes,
        count(distinct oi.order_id) as transacoes,
        sum(oi.paid_points) as pontos,
        sum(oi.product_value) as reais,
        sum(oi.product_value) / sum(oi.paid_points) as reais_por_ponto
    FROM order_items oi
    WHERE oi.category_macro = 'Cashback' 
      AND oi.product_type = 'TRANSFERENCIA'
      AND oi.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO')
    GROUP BY 1
)
SELECT 
    r.mes,
    r.pix_transacoes as relatorio_transacoes,
    p.transacoes as items_transacoes,
    r.pix_pontos as relatorio_pontos,
    p.pontos as items_pontos,
    r.pix_reais as relatorio_reais,
    p.reais as items_reais,
    r.pix_reais / r.pix_pontos as relatorio_reais_por_ponto,
    p.reais / p.pontos as items_reais_por_ponto,
    p.reais - r.pix_reais as diff_reais,
    r.pix_pontos - p.pontos as diff_pontos
FROM relatorio_mensal_cliente r
LEFT JOIN pix_valid p ON r.mes = p.mes
WHERE r.mes >= '2026-05';
"""
print(con.execute(query_pix_approved).fetchdf().to_string())

print("\nE se olharmos redeemed_points para o Pix?")
query_redeemed_pix = """
SELECT 
    strftime(oi.created_at, '%Y-%m') as mes,
    rp.movement_type,
    count(*) as qtd,
    sum(rp.points) as total_pontos
FROM redeemed_points rp
JOIN order_items oi ON rp.order_item_id = oi.order_item_id
WHERE oi.category_macro = 'Cashback' AND oi.product_type = 'TRANSFERENCIA'
GROUP BY 1, 2
ORDER BY 1, 2;
"""
print(con.execute(query_redeemed_pix).fetchdf().to_string())

print("\nPor que a diferença de reais entre o relatório e order_items?")
print("Vamos inspecionar a razão entre relatorio_reais e items_reais:")
query_ratio = """
WITH pix_valid AS (
    SELECT 
        strftime(oi.created_at, '%Y-%m') as mes,
        sum(oi.paid_points) as pontos,
        sum(oi.product_value) as reais
    FROM order_items oi
    WHERE oi.category_macro = 'Cashback' 
      AND oi.product_type = 'TRANSFERENCIA'
      AND oi.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO')
    GROUP BY 1
)
SELECT 
    r.mes,
    r.pix_reais,
    p.reais as items_reais,
    r.pix_reais / p.reais as ratio_reais,
    r.pix_pontos,
    p.pontos as items_pontos,
    r.pix_pontos / p.pontos as ratio_pontos
FROM relatorio_mensal_cliente r
JOIN pix_valid p ON r.mes = p.mes;
"""
print(con.execute(query_ratio).fetchdf().to_string())

print("\n==================================================")
print("INVESTIGAÇÃO 2: AFIRMAÇÃO DO DIRETOR (BREAKAGE EM 40% vs META 20%)")
print("==================================================")
# Como breakage pode ser calculado?
# 1. Pontos expirados / pontos acumulados (earn)
# 2. Pontos expirados / pontos resgatados (burn)
# 3. Pontos expirados da migração / pontos da migração
# 4. Taxa de expiração por coorte
# 5. Saldo sem movimentação
print("Resumo de pontos_ledger por operação:")
print(con.execute("""
    SELECT 
        l.operation_code,
        d.operation_name,
        d.direction,
        count(*) as qtd,
        sum(l.points) as soma_pontos
    FROM points_ledger l
    JOIN dim_operation d ON l.operation_code = d.operation_code
    GROUP BY 1, 2, 3
    ORDER BY 1;
""").fetchdf().to_string())

print("\nPontos da migração:")
print(con.execute("""
    SELECT 
        sum(case when operation_code = 100 then points else 0 end) as credito_migracao,
        sum(case when operation_code = 103 then abs(points) else 0 end) as expiracao_migracao,
        sum(case when operation_code = 103 then abs(points) else 0 end) / 
            nullif(sum(case when operation_code = 100 then points else 0 end), 0) as taxa_expiracao_migracao
    FROM points_ledger;
""").fetchdf().to_string())

print("\nE quanto ao total de créditos vs expirações?")
print(con.execute("""
    SELECT 
        sum(case when d.direction = 'CREDIT' then l.points else 0 end) as total_creditado,
        sum(case when l.operation_code = 1 then l.points else 0 end) as credito_organico,
        sum(case when l.operation_code = 100 then l.points else 0 end) as credito_migracao,
        sum(case when l.operation_code in (3, 103) then abs(l.points) else 0 end) as total_expirado,
        sum(case when l.operation_code in (3, 103) then abs(l.points) else 0 end) / 
            sum(case when d.direction = 'CREDIT' then l.points else 0 end) as breakage_sobre_total_credito,
        sum(case when l.operation_code in (3, 103) then abs(l.points) else 0 end) / 
            sum(case when l.operation_code = 100 then l.points else 0 end) as breakage_sobre_migracao
    FROM points_ledger l
    JOIN dim_operation d ON l.operation_code = d.operation_code;
""").fetchdf().to_string())

print("\nQuem falou que o breakage está em 40%? De onde sai 40%?")
print("Vamos testar várias combinações matemáticas possíveis:")
print(con.execute("""
    SELECT 
        -- expiracao_migracao / credito_organico?
        64090805.0 / 437817783.0 as exp_mig_div_cred_org,
        -- expiracao_migracao / resgate?
        64090805.0 / 323423650.0 as exp_mig_div_resgate,
        -- expiracao_migracao / (credito_migracao - resgate)?
        64090805.0 / (324024198.0 - 323423650.0) as teste3,
        -- O que dá 40%?
        -- Se saldo a expirar? Vamos ver datas de valid_until!
        1 as placeholder;
""").fetchdf().to_string())

print("\nDatas de valid_until em points_ledger:")
print(con.execute("""
    SELECT 
        strftime(valid_until, '%Y-%m') as mes_expiracao,
        count(*) as qtd,
        sum(points) as pontos
    FROM points_ledger
    WHERE operation_code = 1 -- CREDITO
    GROUP BY 1
    ORDER BY 1
    LIMIT 20;
""").fetchdf().to_string())

print("\nQuando ocorreram as expirações da migração (op 103)?")
print(con.execute("""
    SELECT 
        strftime(movement_at, '%Y-%m') as mes_movimento,
        count(*) as qtd,
        sum(points) as pontos
    FROM points_ledger
    WHERE operation_code = 103
    GROUP BY 1
    ORDER BY 1;
""").fetchdf().to_string())

print("\n==================================================")
print("INVESTIGAÇÃO 3: CRM E LANÇAMENTO DO PIX (2026-05-27)")
print("==================================================")
print("Campanhas enviadas em maio de 2026:")
print(con.execute("""
    SELECT 
        campaign_id,
        campaign_type,
        min(event_ts) as start_ts,
        max(event_ts) as end_ts,
        count(distinct user_id) as users_impactados,
        count(*) as eventos
    FROM crm_events
    WHERE event_ts >= '2026-05-01' and event_ts < '2026-06-01'
    GROUP BY 1, 2
    ORDER BY start_ts;
""").fetchdf().to_string())

print("\nDetalhes dos eventos de CRM (event_name):")
print(con.execute("""
    SELECT 
        event_name,
        count(*) as qtd
    FROM crm_events
    GROUP BY 1;
""").fetchdf().to_string())

print("\nPropriedades dos eventos em crm_events:")
print(con.execute("""
    SELECT distinct campaign_id, event_properties
    FROM crm_events
    WHERE event_ts >= '2026-05-20' and event_ts <= '2026-06-05'
    LIMIT 15;
""").fetchdf().to_string())
