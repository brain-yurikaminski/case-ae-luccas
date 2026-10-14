import os
import duckdb
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "dados")

con = duckdb.connect(database=":memory:")

# Carrega todas as tabelas
tables = [
    "cards", "carts", "crm_events", "dim_operation",
    "order_items", "orders", "points_ledger", "redeemed_points",
    "relatorio_mensal_cliente"
]

for t in tables:
    filepath = os.path.join(DATA_DIR, f"{t}.csv")
    con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{filepath}')")

print("=== 1. DIM_OPERATION ===")
print(con.execute("SELECT * FROM dim_operation").fetchdf())

print("\n=== 2. RELATORIO_MENSAL_CLIENTE (COMPLETO) ===")
relatorio = con.execute("SELECT * FROM relatorio_mensal_cliente").fetchdf()
print(relatorio.to_string())
# Calcula razao pix_reais / pix_pontos
print("\nRazão pix_reais / pix_pontos no relatório mensal:")
relatorio_pix = con.execute("""
    SELECT mes, pix_reais, pix_pontos, pix_transacoes,
           CASE WHEN pix_pontos > 0 THEN pix_reais / pix_pontos ELSE NULL END as reais_por_ponto,
           CASE WHEN pix_reais > 0 THEN pix_pontos / pix_reais ELSE NULL END as pontos_por_real
    FROM relatorio_mensal_cliente
""").fetchdf()
print(relatorio_pix.to_string())

print("\n=== 3. CATEGORIAS E TIPOS DE PRODUTO EM ORDER_ITEMS ===")
print(con.execute("""
    SELECT category_macro, product_type, count(*) as count_items, 
           sum(paid_points) as total_paid_points, 
           sum(paid_currency) as total_paid_currency,
           sum(product_value) as total_product_value
    FROM order_items
    GROUP BY 1, 2
    ORDER BY 3 DESC
""").fetchdf())

print("\n=== 4. STATUS DOS PEDIDOS E ITEMS ===")
print("Orders status:")
print(con.execute("SELECT status, count(*) FROM orders GROUP BY 1").fetchdf())
print("Order_items status:")
print(con.execute("SELECT status, count(*) FROM order_items GROUP BY 1").fetchdf())

print("\n=== 5. USER_ID EM ORDERS VS CARTS ===")
print(con.execute("""
    SELECT 
        count(*) as total_orders,
        count(user_id) as orders_with_user_id,
        count(distinct cart_id) as distinct_carts
    FROM orders
""").fetchdf())
print("Join orders com carts:")
print(con.execute("""
    SELECT 
        count(o.order_id) as total_orders,
        count(c.user_id) as carts_with_user_id,
        count(distinct c.user_id) as distinct_users
    FROM orders o
    LEFT JOIN carts c ON o.cart_id = c.cart_id
""").fetchdf())

print("\n=== 6. PIX EM ORDER_ITEMS (DETALHES DE VALORES E PONTOS) ===")
print(con.execute("""
    SELECT 
        strftime(created_at, '%Y-%m') as mes,
        count(*) as qtd,
        sum(paid_points) as total_pontos,
        sum(paid_currency) as total_currency,
        sum(product_value) as total_valor,
        avg(product_value / nullif(paid_points, 0)) as avg_valor_por_ponto,
        sum(product_value) / nullif(sum(paid_points), 0) as weighted_valor_por_ponto,
        sum(paid_currency) / nullif(sum(paid_points), 0) as paid_currency_por_ponto
    FROM order_items
    WHERE category_macro ILIKE '%pix%' or product_type ILIKE '%pix%' or supplier_name ILIKE '%pix%'
    GROUP BY 1
    ORDER BY 1
""").fetchdf())

print("\n=== 7. POINTS_LEDGER OPERAÇÕES E BREAKAGE ===")
print(con.execute("""
    SELECT 
        l.operation_code,
        d.operation_name,
        d.direction,
        count(*) as qtd_movimentos,
        sum(l.points) as total_pontos
    FROM points_ledger l
    LEFT JOIN dim_operation d ON l.operation_code = d.operation_code
    GROUP BY 1, 2, 3
    ORDER BY 1
""").fetchdf())

print("\n=== 8. CRM_EVENTS (CAMPANHAS E GRUPO DE CONTROLE) ===")
print(con.execute("""
    SELECT 
        campaign_type,
        control_group,
        count(*) as total_eventos,
        count(distinct user_id) as distinct_users,
        min(event_ts) as min_ts,
        max(event_ts) as max_ts
    FROM crm_events
    GROUP BY 1, 2
""").fetchdf())

print("\nEventos específicos de Pix ou da época do lançamento (2026-05-27):")
print(con.execute("""
    SELECT 
        campaign_id,
        campaign_type,
        control_group,
        event_name,
        count(*) as qtd,
        min(event_ts) as min_ts,
        max(event_ts) as max_ts
    FROM crm_events
    WHERE event_ts >= '2026-05-20'
    GROUP BY 1, 2, 3, 4
    ORDER BY min_ts
    LIMIT 20
""").fetchdf())
