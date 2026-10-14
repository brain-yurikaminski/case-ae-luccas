-- models/staging/stg_crm_events.sql
-- Grão: 1 linha por evento de engajamento

SELECT
    event_ts::TIMESTAMP AS event_ts,
    user_id::BIGINT AS user_id,
    device_id::VARCHAR AS device_id,
    event_name::VARCHAR AS event_name,
    campaign_type::VARCHAR AS campaign_type,
    campaign_id::VARCHAR AS campaign_id,
    control_group::VARCHAR AS control_group,
    event_properties::VARCHAR AS event_properties
FROM read_csv_auto('dados/crm_events.csv')
