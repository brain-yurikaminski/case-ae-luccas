-- models/marts/fct_crm_attribution.sql
-- Grão: 1 linha por usuário que resgatou Pix (user_id)

WITH pix_users AS (
    SELECT 
        user_id,
        MIN(created_at) AS first_pix_at,
        MAX(created_at) AS last_pix_at,
        COUNT(DISTINCT order_id) AS total_pix_orders,
        SUM(paid_points) AS total_pix_points,
        SUM(product_value) AS total_pix_reais
    FROM fct_order_items
    WHERE is_pix = TRUE AND is_approved = TRUE
    GROUP BY 1
),
email_events AS (
    SELECT
        user_id,
        MIN(CASE WHEN event_name = 'Notification Sent' THEN event_ts END) AS email_sent_ts,
        MIN(CASE WHEN event_name = 'Notification Viewed' THEN event_ts END) AS email_viewed_ts,
        MIN(CASE WHEN event_name = 'Notification Clicked' THEN event_ts END) AS email_clicked_ts
    FROM stg_crm_events
    WHERE campaign_id = 'CMP_LANCAMENTO_PIX_4dbee001e6aba1eb57b512c3'
    GROUP BY 1
),
push_events AS (
    SELECT
        user_id,
        MIN(CASE WHEN event_name = 'Notification Sent' THEN event_ts END) AS push_sent_ts,
        MIN(CASE WHEN event_name IN ('Notification Viewed', 'Push Impressions') THEN event_ts END) AS push_viewed_ts,
        MIN(CASE WHEN event_name = 'Notification Clicked' THEN event_ts END) AS push_clicked_ts
    FROM stg_crm_events
    WHERE campaign_id IN ('CMP_cde3c1b2f2e76a6ea2e641d6', 'CMP_cb21c575fee7cf8fb08bed6b')
    GROUP BY 1
)

SELECT
    u.user_id,
    u.first_pix_at,
    u.total_pix_orders,
    u.total_pix_points,
    u.total_pix_reais,
    
    -- Resgatou antes de qualquer comunicação de lançamento
    CASE WHEN u.first_pix_at < '2026-05-27 23:15:00-03:00' THEN TRUE ELSE FALSE END AS resgatou_antes_de_qualquer_comunicacao,
    CASE WHEN u.first_pix_at < '2026-05-28 13:00:00-03:00' THEN TRUE ELSE FALSE END AS resgatou_antes_do_email,
    
    -- Interações com o Email
    CASE WHEN e.email_sent_ts IS NOT NULL THEN TRUE ELSE FALSE END AS recebeu_email,
    CASE WHEN e.email_viewed_ts IS NOT NULL THEN TRUE ELSE FALSE END AS visualizou_email,
    CASE WHEN e.email_clicked_ts IS NOT NULL THEN TRUE ELSE FALSE END AS clicou_email,
    
    -- Interações com Pushes
    CASE WHEN p.push_sent_ts IS NOT NULL THEN TRUE ELSE FALSE END AS recebeu_push,
    CASE WHEN p.push_viewed_ts IS NOT NULL THEN TRUE ELSE FALSE END AS visualizou_push,
    CASE WHEN p.push_clicked_ts IS NOT NULL THEN TRUE ELSE FALSE END AS clicou_push,
    
    -- Classificação de Atribuição
    CASE 
        WHEN u.first_pix_at < '2026-05-27 23:15:00-03:00' THEN 'Pre-Campaign Organic'
        WHEN COALESCE(e.email_clicked_ts, p.push_clicked_ts) IS NOT NULL 
             AND LEAST(COALESCE(e.email_clicked_ts, '2099-01-01'), COALESCE(p.push_clicked_ts, '2099-01-01')) <= u.first_pix_at THEN 'Direct Click Attribution'
        WHEN COALESCE(e.email_viewed_ts, p.push_viewed_ts) IS NOT NULL 
             AND LEAST(COALESCE(e.email_viewed_ts, '2099-01-01'), COALESCE(p.push_viewed_ts, '2099-01-01')) <= u.first_pix_at THEN 'View-Through Attribution'
        ELSE 'Organic / App Discovery'
    END AS canal_atribuicao
FROM pix_users u
LEFT JOIN email_events e ON u.user_id = e.user_id
LEFT JOIN push_events p ON u.user_id = p.user_id
