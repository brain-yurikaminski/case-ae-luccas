-- models/staging/stg_relatorio_mensal.sql
-- Grão: 1 linha por mês de prestação de contas

SELECT
    mes::VARCHAR AS mes,
    aereas_pct::BIGINT AS aereas_pct,
    varejo_pct::BIGINT AS varejo_pct,
    pix_pct::DOUBLE AS pix_pct,
    pix_reais::DOUBLE AS pix_reais,
    pix_pontos::DOUBLE AS pix_pontos,
    pix_transacoes::DOUBLE AS pix_transacoes,
    emails_enviados::BIGINT AS emails_enviados,
    push_enviados::DOUBLE AS push_enviados
FROM read_csv_auto('dados/relatorio_mensal_cliente.csv')
