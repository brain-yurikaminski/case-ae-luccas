-- models/staging/stg_orders.sql
-- Grão: 1 linha por order_id

SELECT
    order_id::BIGINT AS order_id,
    cart_id::BIGINT AS cart_id,
    user_id::BIGINT AS user_id, -- Nota: user_id vem nulo nesta tabela de origem e é enriquecido via carts
    created_at::TIMESTAMPTZ AS created_at,
    status::VARCHAR AS status,
    status_updated_at::TIMESTAMPTZ AS status_updated_at
FROM read_csv_auto('dados/orders.csv')
