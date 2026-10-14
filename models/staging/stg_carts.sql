-- models/staging/stg_carts.sql
-- Grão: 1 linha por cart_id

SELECT
    cart_id::BIGINT AS cart_id,
    user_id::BIGINT AS user_id,
    channel::VARCHAR AS channel
FROM read_csv_auto('dados/carts.csv')
