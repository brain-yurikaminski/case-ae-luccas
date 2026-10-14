-- models/staging/stg_order_items.sql
-- Grão: 1 linha por order_item_id

SELECT
    order_item_id::BIGINT AS order_item_id,
    order_id::BIGINT AS order_id,
    created_at::TIMESTAMPTZ AS created_at,
    status::VARCHAR AS status,
    product_type::VARCHAR AS product_type,
    supplier_name::VARCHAR AS supplier_name,
    supplier_responsible::VARCHAR AS supplier_responsible,
    category_macro::VARCHAR AS category_macro,
    COALESCE(paid_points, 0)::BIGINT AS paid_points,
    COALESCE(paid_currency, 0.0)::DOUBLE AS paid_currency,
    COALESCE(product_value, 0.0)::DOUBLE AS product_value,
    COALESCE(refunded_points, 0)::BIGINT AS refunded_points,
    COALESCE(quantity, 1)::BIGINT AS quantity
FROM read_csv_auto('dados/order_items.csv')
