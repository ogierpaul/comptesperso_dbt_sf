{{config(materialized='table')}}
SELECT
TRANSACTION_ID,
  TRANSACTION_DATE,
  NAME_PERSONAL_ACCOUNT,
  AMOUNT,
  TRANSACTION_DESCRIPTION,
  BENEFICIARY_IBAN,
  FINANZGURU_CATEGORY_LVL1,
  FINANZGURU_CATEGORY_LVL2,
  IS_CONTRACT,
  CONTRACT_RECURRENCE,
  CONTRACT_ID,
  IS_TRANSFER,
  TRANSACTION_TYPE,
  PERSONAL_IBAN,
  TXT_CATEGORY_LVL3,
  BENEFICIARY,
  SPEND
FROM {{ ref('fact_with_spend_from_income_expenses') }}
WHERE SCOPE_OUT = FALSE