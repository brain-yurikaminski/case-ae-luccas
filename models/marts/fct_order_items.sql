-- models/marts/fct_order_items.sql
-- Grão: 1 linha por order_item_id

WITH items AS (
    SELECT * FROM stg_order_items
),
orders AS (
    SELECT * FROM stg_orders
),
carts AS (
    SELECT * FROM stg_carts
),
cards AS (
    SELECT * FROM stg_cards WHERE is_most_recent = TRUE
)

SELECT
    i.order_item_id,
    i.order_id,
    o.cart_id,
    c.user_id,
    c.channel,
    cd.card_class,
    cd.card_flag,
    i.created_at,
    strftime(i.created_at, '%Y-%m') AS mes,
    i.status AS item_status,
    o.status AS order_status,
    i.product_type,
    i.supplier_name,
    i.supplier_responsible,
    i.category_macro,
    CASE 
        WHEN i.category_macro = 'Cashback' AND i.product_type = 'TRANSFERENCIA' THEN 'Pix'
        WHEN i.category_macro = 'Cashback' AND i.product_type = 'COMPRA_PONTOS' THEN 'Compra Pontos'
        ELSE i.category_macro
    END AS categoria_consolidada,
    i.paid_points,
    i.paid_currency,
    i.product_value,
    i.refunded_points,
    i.quantity,
    CASE 
        WHEN i.status IN ('APROVADO', 'FINALIZADO_COM_SUCESSO') THEN TRUE 
        ELSE FALSE 
    END AS is_approved,
    CASE 
        WHEN i.category_macro = 'Cashback' AND i.product_type = 'TRANSFERENCIA' THEN TRUE 
        ELSE FALSE 
    END AS is_pix,
    CASE 
        WHEN i.paid_points > 0 THEN i.product_value / i.paid_points 
        ELSE NULL 
    END AS reais_por_ponto
FROM items i
JOIN orders o ON i.order_id = o.order_id
LEFT JOIN carts c ON o.cart_id = c.cart_id
LEFT JOIN cards cd ON c.user_id = cd.user_id
