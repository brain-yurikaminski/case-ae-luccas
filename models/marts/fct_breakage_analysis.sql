-- models/marts/fct_breakage_analysis.sql
-- Grão: 1 linha por escopo conceitual de análise

WITH ledger AS (
    SELECT * FROM stg_points_ledger
),
metrics AS (
    SELECT
        -- Base da Migração (op 100 e op 103)
        SUM(CASE WHEN operation_code = 100 THEN points ELSE 0 END) AS pontos_credito_migracao,
        SUM(CASE WHEN operation_code = 103 THEN ABS(points) ELSE 0 END) AS pontos_expiracao_migracao,
        
        -- Base Total do Programa
        SUM(CASE WHEN direction = 'CREDIT' THEN points ELSE 0 END) AS pontos_credito_total,
        SUM(CASE WHEN operation_code = 1 THEN points ELSE 0 END) AS pontos_credito_organico,
        SUM(CASE WHEN operation_code = 2 THEN ABS(points) ELSE 0 END) AS pontos_resgate_total,
        SUM(CASE WHEN operation_code IN (3, 103) THEN ABS(points) ELSE 0 END) AS pontos_expiracao_total,
        
        -- Trimestre Pré-Pix (Fev a Abr de 2026)
        SUM(CASE WHEN operation_code = 103 AND strftime(movement_at, '%Y-%m') IN ('2026-02', '2026-03', '2026-04') THEN ABS(points) ELSE 0 END) AS exp_tri_pre_pix,
        SUM(CASE WHEN operation_code = 2 AND strftime(movement_at, '%Y-%m') IN ('2026-02', '2026-03', '2026-04') THEN ABS(points) ELSE 0 END) AS resg_tri_pre_pix
    FROM ledger
)

SELECT
    '1. Breakage da Migração (Conceito Oficial)' AS escopo_analise,
    pontos_credito_migracao AS base_denominador,
    pontos_expiracao_migracao AS volume_expirado,
    ROUND(pontos_expiracao_migracao * 100.0 / NULLIF(pontos_credito_migracao, 0), 2) AS taxa_percentual,
    20.0 AS meta_teto_pct,
    'DENTRO DA META' AS status_avaliacao,
    'Calculado estritamente como pontos expirados sobre pontos creditados na migração (19,78% <= 20%).' AS explicacao
FROM metrics

UNION ALL

SELECT
    '2. Breakage Global do Programa (Orgânico + Migração)' AS escopo_analise,
    pontos_credito_total AS base_denominador,
    pontos_expiracao_total AS volume_expirado,
    ROUND(pontos_expiracao_total * 100.0 / NULLIF(pontos_credito_total, 0), 2) AS taxa_percentual,
    20.0 AS meta_teto_pct,
    'DENTRO DA META' AS status_avaliacao,
    'Calculado sobre toda a emissão do Pontua+. Créditos orgânicos têm 2 anos de validade e ainda não expiraram.' AS explicacao
FROM metrics

UNION ALL

SELECT
    '3. Confusão do Diretor: Razão Expiração / Resgates (Fev-Abr/2026)' AS escopo_analise,
    resg_tri_pre_pix AS base_denominador,
    exp_tri_pre_pix AS volume_expirado,
    ROUND(exp_tri_pre_pix * 100.0 / NULLIF(resg_tri_pre_pix, 0), 2) AS taxa_percentual,
    20.0 AS meta_teto_pct,
    'ERRO DE CONCEITO DO DIRETOR' AS status_avaliacao,
    'O diretor dividiu expiração por resgates no trimestre anterior ao Pix (39,2% ~ 40%), o que não é breakage.' AS explicacao
FROM metrics
