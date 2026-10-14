-- models/staging/stg_cards.sql
-- Grão: 1 linha por account_id

SELECT
    account_id::BIGINT AS account_id,
    user_id::BIGINT AS user_id,
    card_class::VARCHAR AS card_class,
    card_flag::VARCHAR AS card_flag,
    created_at::TIMESTAMPTZ AS created_at,
    is_most_recent::BOOLEAN AS is_most_recent
FROM read_csv_auto('dados/cards.csv')
