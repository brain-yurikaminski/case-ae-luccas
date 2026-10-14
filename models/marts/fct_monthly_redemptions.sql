-- models/marts/fct_monthly_redemptions.sql
-- Grão: 1 linha por mês (mes)

WITH items AS (
    SELECT * 
    FROM fct_order_items 
    WHERE is_approved = TRUE
),
aggregated AS (
    SELECT
        mes,
        -- Volumes em Pontos
        SUM(CASE WHEN categoria_consolidada = 'Aereas' THEN paid_points ELSE 0 END) AS pontos_aereas,
        SUM(CASE WHEN categoria_consolidada = 'Varejo' THEN paid_points ELSE 0 END) AS pontos_varejo,
        SUM(CASE WHEN categoria_consolidada = 'Pix' THEN paid_points ELSE 0 END) AS pontos_pix,
        SUM(CASE WHEN categoria_consolidada = 'Compra Pontos' THEN paid_points ELSE 0 END) AS pontos_compra_pontos,
        SUM(paid_points) AS pontos_totais,
        
        -- Transações
        COUNT(DISTINCT CASE WHEN categoria_consolidada = 'Aereas' THEN order_id END) AS pedidos_aereas,
        COUNT(DISTINCT CASE WHEN categoria_consolidada = 'Varejo' THEN order_id END) AS pedidos_varejo,
        COUNT(DISTINCT CASE WHEN categoria_consolidada = 'Pix' THEN order_id END) AS pedidos_pix,
        COUNT(DISTINCT order_id) AS pedidos_totais,
        
        -- Valores Financeiros (Reais)
        SUM(CASE WHEN categoria_consolidada = 'Aereas' THEN product_value ELSE 0.0 END) AS valor_aereas,
        SUM(CASE WHEN categoria_consolidada = 'Varejo' THEN product_value ELSE 0.0 END) AS valor_varejo,
        SUM(CASE WHEN categoria_consolidada = 'Pix' THEN product_value ELSE 0.0 END) AS valor_pix,
        SUM(product_value) AS valor_total_produtos,
        SUM(paid_currency) AS valor_pago_moeda_usuario
    FROM items
    GROUP BY 1
)

SELECT
    mes,
    pontos_aereas,
    ROUND(pontos_aereas * 100.0 / NULLIF(pontos_totais, 0), 2) AS pct_aereas,
    pontos_varejo,
    ROUND(pontos_varejo * 100.0 / NULLIF(pontos_totais, 0), 2) AS pct_varejo,
    pontos_pix,
    ROUND(pontos_pix * 100.0 / NULLIF(pontos_totais, 0), 2) AS pct_pix,
    pontos_totais,
    
    -- Verificação de Metas Contratuais com o Banco Aurora
    CASE WHEN (pontos_aereas * 100.0 / NULLIF(pontos_totais, 0)) >= 50.0 THEN TRUE ELSE FALSE END AS meta_aereas_atingida,
    CASE WHEN (pontos_varejo * 100.0 / NULLIF(pontos_totais, 0)) >= 20.0 THEN TRUE ELSE FALSE END AS meta_varejo_atingida,
    
    -- Finanças e Transações
    pedidos_aereas,
    pedidos_varejo,
    pedidos_pix,
    pedidos_totais,
    valor_aereas,
    valor_varejo,
    valor_pix,
    valor_total_produtos,
    valor_pago_moeda_usuario,
    
    -- Custo Unitário Médio por Ponto (R$/Ponto)
    ROUND(valor_aereas / NULLIF(pontos_aereas, 0), 4) AS reais_por_ponto_aereas,
    ROUND(valor_varejo / NULLIF(pontos_varejo, 0), 4) AS reais_por_ponto_varejo,
    ROUND(valor_pix / NULLIF(pontos_pix, 0), 4) AS reais_por_ponto_pix
FROM aggregated
ORDER BY mes
