SELECT
account_iban AS PERSONAL_IBAN,
account_name  AS PERSONAL_ACCOUNT_NAME
FROM {{ref('accounts')}}