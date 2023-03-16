SELECT
transaction_id,
pair_id
FROM {{source('staging_corrections', 'self_cancelling_transactions')}}