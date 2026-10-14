import os
import duckdb
import pandas as pd

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
print("1. CRM: A COMUNICAÇÃO DE LANÇAMENTO EXPLICA O SUCESSO DO PIX?")
print("==================================================")
# Vamos ver quem resgatou Pix e quando
query_crm_pix = """
WITH pix_orders AS (
    SELECT 
        o.order_id,
        c.user_id,
        oi.created_at as order_created_at,
        oi.paid_points,
        oi.product_value
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN carts c ON o.cart_id = c.cart_id
    WHERE oi.category_macro = 'Cashback' 
      AND oi.product_type = 'TRANSFERENCIA'
      AND oi.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO')
),
pix_campaign_events AS (
    SELECT 
        user_id,
        event_name,
        min(event_ts) as first_interaction_ts
    FROM crm_events
    WHERE campaign_id = 'CMP_LANCAMENTO_PIX_4dbee001e6aba1eb57b512c3'
    GROUP BY 1, 2
)
SELECT 
    count(distinct p.user_id) as total_pix_users,
    count(distinct case when e_sent.user_id is not null then p.user_id end) as users_received_email,
    count(distinct case when e_viewed.user_id is not null then p.user_id end) as users_viewed_email,
    count(distinct case when e_clicked.user_id is not null then p.user_id end) as users_clicked_email,
    count(distinct case when e_sent.user_id is null then p.user_id end) as users_never_received_email,
    count(distinct case when p.order_created_at < '2026-05-28 13:00:00' then p.user_id end) as users_ordered_before_email
FROM pix_orders p
LEFT JOIN pix_campaign_events e_sent ON p.user_id = e_sent.user_id AND e_sent.event_name = 'Notification Sent'
LEFT JOIN pix_campaign_events e_viewed ON p.user_id = e_viewed.user_id AND e_viewed.event_name = 'Notification Viewed'
LEFT JOIN pix_campaign_events e_clicked ON p.user_id = e_clicked.user_id AND e_clicked.event_name = 'Notification Clicked';
"""
print(con.execute(query_crm_pix).fetchdf().to_string())

print("\nOrdens de Pix antes do email de lançamento (2026-05-28 13:00):")
print(con.execute("""
    SELECT 
        oi.created_at,
        c.user_id,
        oi.paid_points,
        oi.product_value
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN carts c ON o.cart_id = c.cart_id
    WHERE oi.category_macro = 'Cashback' 
      AND oi.product_type = 'TRANSFERENCIA'
      AND oi.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO')
      AND oi.created_at < '2026-05-28 13:00:00'
    ORDER BY oi.created_at
""").fetchdf().to_string())

print("\nEngajamento da campanha de lançamento do Pix:")
print(con.execute("""
    SELECT 
        event_name,
        count(*) as total_eventos,
        count(distinct user_id) as distinct_users
    FROM crm_events
    WHERE campaign_id = 'CMP_LANCAMENTO_PIX_4dbee001e6aba1eb57b512c3'
    GROUP BY 1
    ORDER BY 2 DESC;
""").fetchdf().to_string())

print("\nTotal de usuários na base vs impactados pela campanha Pix:")
print(con.execute("""
    SELECT 
        (SELECT count(distinct user_id) FROM cards) as total_users_cards,
        (SELECT count(distinct user_id) FROM points_ledger) as total_users_ledger,
        (SELECT count(distinct user_id) FROM crm_events WHERE campaign_id = 'CMP_LANCAMENTO_PIX_4dbee001e6aba1eb57b512c3') as users_campanha_pix;
""").fetchdf().to_string())

print("\n==================================================")
print("2. DIRETOR: BREAKAGE EM 40%? DE ONDE SAI ESSE NÚMERO?")
print("==================================================")
# Vamos testar se 40% é a porcentagem de contas com expiração
print("Porcentagem de contas que tiveram pontos expirados:")
print(con.execute("""
    WITH accounts_summary AS (
        SELECT 
            account_id,
            sum(case when operation_code = 100 then points else 0 end) as migracao_creditada,
            sum(case when operation_code = 103 then abs(points) else 0 end) as migracao_expirada,
            sum(case when operation_code in (2) then abs(points) else 0 end) as resgatado
        FROM points_ledger
        GROUP BY 1
    )
    SELECT 
        count(*) as total_accounts,
        count(case when migracao_creditada > 0 then 1 end) as accounts_com_migracao,
        count(case when migracao_expirada > 0 then 1 end) as accounts_com_expiracao,
        count(case when migracao_expirada > 0 then 1 end) * 1.0 / count(case when migracao_creditada > 0 then 1 end) as pct_accounts_com_expiracao
    FROM accounts_summary;
""").fetchdf().to_string())

# Vamos verificar a relação entre saldos migrados e expiração
print("\nDistribuição de expiração por conta com migração:")
print(con.execute("""
    WITH accounts_mig AS (
        SELECT 
            account_id,
            sum(case when operation_code = 100 then points else 0 end) as creditado,
            sum(case when operation_code = 103 then abs(points) else 0 end) as expirado
        FROM points_ledger
        WHERE operation_code in (100, 103)
        GROUP BY 1
    )
    SELECT 
        avg(expirado / nullif(creditado, 0)) as media_razao_expiracao,
        sum(expirado) / sum(creditado) as razao_total_expiracao
    FROM accounts_mig;
""").fetchdf().to_string())

# O que dá ~40% no ledger?
print("\nBuscando qualquer combinação que resulte em ~40%:")
print(con.execute("""
    WITH totals AS (
        SELECT 
            sum(case when operation_code = 1 then points else 0 end) as cred_organico,
            sum(case when operation_code = 100 then points else 0 end) as cred_migracao,
            sum(case when operation_code = 2 then abs(points) else 0 end) as resgate,
            sum(case when operation_code = 103 then abs(points) else 0 end) as exp_migracao
        FROM points_ledger
    )
    SELECT 
        exp_migracao / cred_migracao as exp_sobre_migracao, -- 19.78%
        exp_migracao / resgate as exp_sobre_resgate, -- 19.82%
        exp_migracao / (cred_migracao - exp_migracao) as exp_sobre_saldo_mig_restante,
        (cred_migracao - resgate) / cred_migracao as saldo_nao_resgatado_migracao,
        exp_migracao / cred_organico as exp_sobre_cred_org,
        -- E se for em relação aos resgates de passagens aéreas ou de um período?
        1 as placeholder
    FROM totals;
""").fetchdf().to_string())

print("\n==================================================")
print("3. METAS CONTRATUAIS: AÉREAS >= 50% E VAREJO >= 20%")
print("==================================================")
# Mix mensal de resgates em order_items (pontos pagos em pedidos aprovados)
print("Mix mensal de pontos resgatados por categoria macro:")
query_mix = """
WITH monthly_points AS (
    SELECT 
        strftime(oi.created_at, '%Y-%m') as mes,
        oi.category_macro,
        sum(oi.paid_points) as pontos,
        sum(oi.product_value) as valor_produtos,
        sum(oi.paid_currency) as valor_pago_reais
    FROM order_items oi
    WHERE oi.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO')
    GROUP BY 1, 2
),
totals AS (
    SELECT mes, sum(pontos) as total_pontos
    FROM monthly_points
    GROUP BY 1
)
SELECT 
    m.mes,
    m.category_macro,
    m.pontos,
    t.total_pontos,
    round(m.pontos * 100.0 / t.total_pontos, 2) as share_pontos_pct,
    m.valor_produtos,
    m.valor_pago_reais,
    round(m.valor_produtos / nullif(m.pontos, 0), 4) as valor_por_ponto
FROM monthly_points m
JOIN totals t ON m.mes = t.mes
ORDER BY m.mes, m.category_macro;
"""
print(con.execute(query_mix).fetchdf().to_string())

print("\nMix consolidado por mês (Colunas: Aereas %, Varejo %, Cashback/Pix %):")
query_mix_pivoted = """
WITH monthly_points AS (
    SELECT 
        strftime(oi.created_at, '%Y-%m') as mes,
        sum(case when oi.category_macro = 'Aereas' then oi.paid_points else 0 end) as aereas_pontos,
        sum(case when oi.category_macro = 'Varejo' then oi.paid_points else 0 end) as varejo_pontos,
        sum(case when oi.category_macro = 'Cashback' then oi.paid_points else 0 end) as pix_pontos,
        sum(oi.paid_points) as total_pontos
    FROM order_items oi
    WHERE oi.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO')
    GROUP BY 1
)
SELECT 
    mes,
    aereas_pontos,
    round(aereas_pontos * 100.0 / total_pontos, 1) as aereas_pct,
    varejo_pontos,
    round(varejo_pontos * 100.0 / total_pontos, 1) as varejo_pct,
    pix_pontos,
    round(pix_pontos * 100.0 / total_pontos, 1) as pix_pct,
    total_pontos,
    case when round(aereas_pontos * 100.0 / total_pontos, 1) >= 50 then 'BATEU' else 'NAO_BATEU' end as meta_aereas_50,
    case when round(varejo_pontos * 100.0 / total_pontos, 1) >= 20 then 'BATEU' else 'NAO_BATEU' end as meta_varejo_20
FROM monthly_points
ORDER BY mes;
"""
print(con.execute(query_mix_pivoted).fetchdf().to_string())
