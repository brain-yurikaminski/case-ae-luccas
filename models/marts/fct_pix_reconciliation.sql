-- models/marts/fct_pix_reconciliation.sql
-- Grão: 1 linha por mês (mes) a partir do lançamento do Pix (2026-05)

WITH pix_items_all AS (
    SELECT
        mes,
        -- Métricas Aprovadas (Liquidadas)
        COUNT(DISTINCT CASE WHEN is_approved THEN order_id END) AS pedidos_aprovados,
        SUM(CASE WHEN is_approved THEN paid_points ELSE 0 END) AS pontos_aprovados,
        SUM(CASE WHEN is_approved THEN product_value ELSE 0.0 END) AS reais_aprovados,
        
        -- Métricas Canceladas / Estornadas / Inválidas
        COUNT(DISTINCT CASE WHEN NOT is_approved THEN order_id END) AS pedidos_nao_aprovados,
        SUM(CASE WHEN NOT is_approved THEN paid_points ELSE 0 END) AS pontos_nao_aprovados,
        
        -- Métricas Brutas (Total Criado no Sistema)
        COUNT(DISTINCT order_id) AS pedidos_brutos_sistema,
        SUM(paid_points) AS pontos_brutos_sistema,
        SUM(product_value) AS reais_brutos_sistema
    FROM fct_order_items
    WHERE is_pix = TRUE
    GROUP BY 1
),
relatorio AS (
    SELECT
        mes,
        pix_transacoes AS relatorio_transacoes,
        pix_pontos AS relatorio_pontos,
        pix_reais AS relatorio_reais,
        pix_reais / NULLIF(pix_pontos, 0) AS relatorio_reais_por_ponto
    FROM stg_relatorio_mensal
    WHERE pix_pontos IS NOT NULL
)

SELECT
    r.mes,
    -- Dados reportados pelo Operador
    r.relatorio_transacoes,
    r.relatorio_pontos,
    r.relatorio_reais,
    ROUND(r.relatorio_reais_por_ponto, 6) AS relatorio_razao_operador,
    
    -- Realidade dos Dados Transacionais (Aprovados)
    p.pedidos_aprovados,
    p.pontos_aprovados,
    p.reais_aprovados,
    ROUND(p.reais_aprovados / NULLIF(p.pontos_aprovados, 0), 6) AS custo_real_por_ponto_aprovado,
    
    -- Realidade dos Dados Brutos (Todos os Pedidos Criados)
    p.pedidos_brutos_sistema,
    p.pontos_brutos_sistema,
    p.pedidos_nao_aprovados,
    p.pontos_nao_aprovados,
    
    -- Comprovação do Erro do Operador:
    -- O operador pegou os Reais Aprovados e dividiu pelos Pontos Brutos Solicitados
    ROUND(r.relatorio_reais / NULLIF(p.pontos_brutos_sistema, 0), 6) AS simulacao_calculo_operador,
    
    -- Testes de Igualdade
    CASE WHEN r.relatorio_transacoes = p.pedidos_brutos_sistema THEN TRUE ELSE FALSE END AS transacoes_batem_com_bruto,
    CASE WHEN r.relatorio_pontos = p.pontos_brutos_sistema THEN TRUE ELSE FALSE END AS pontos_batem_com_bruto,
    CASE WHEN ROUND(p.reais_aprovados / NULLIF(p.pontos_aprovados, 0), 3) = 0.019 THEN TRUE ELSE FALSE END AS preco_unitario_foi_exatamente_19_centavos
FROM relatorio r
JOIN pix_items_all p ON r.mes = p.mes
ORDER BY r.mes
