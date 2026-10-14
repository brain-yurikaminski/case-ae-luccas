-- models/staging/stg_points_ledger.sql
-- Grão: 1 linha por movement_id

SELECT
    l.movement_id::BIGINT AS movement_id,
    l.user_id::BIGINT AS user_id,
    l.account_id::BIGINT AS account_id,
    l.operation_code::BIGINT AS operation_code,
    d.operation_name::VARCHAR AS operation_name,
    d.direction::VARCHAR AS direction,
    l.points::DOUBLE AS points,
    l.movement_at::TIMESTAMPTZ AS movement_at,
    l.valid_until::DATE AS valid_until
FROM read_csv_auto('dados/points_ledger.csv') l
LEFT JOIN read_csv_auto('dados/dim_operation.csv') d ON l.operation_code = d.operation_code
