SELECT
TRANSACTION_ID,
txt_category_lvl3,
try_to_boolean(scope_out) AS scope_out,
try_to_boolean(is_transfer) AS is_transfer
FROM {{source('staging_corrections', 'transaction_id_details')}}