{{config(materialized='table')}}
SELECT
a.TRANSACTION_ID,
a.TRANSACTION_DATE,
a.NAME_PERSONAL_ACCOUNT,
a.AMOUNT,
a.TRANSACTION_DESCRIPTION,
a.BENEFICIARY_IBAN,
a.FINANZGURU_CATEGORY_LVL1,
a.FINANZGURU_CATEGORY_LVL2,
a.IS_TRANSFER,
a.SCOPE_OUT,
a.TRANSACTION_TYPE,
a.INCOME_EXPENSE,
a.PERSONAL_IBAN,
a.TXT_CATEGORY_LVL3,
a.RECEIVER_IS_PERSONAL_ACCOUNT_FLAG,
a.BENEFICIARY,
a.beneficiary_iban_masked,
a.beneficiary_account_preferred_category,
a.pair_id,
a.is_self_cancelling_transaction,
a.accounts_are_both_internal_movements
FROM
    {{ref('fact_with_corrections')}} as a
WHERE
    SCOPE_OUT = TRUE
OR
    RECEIVER_IS_PERSONAL_ACCOUNT_FLAG = TRUE
OR
    IS_TRANSFER = TRUE
OR
    TXT_CATEGORY_LVL3 IN ('InternalMovements', 'Autres comptes', 'ScopeOut')
OR accounts_are_both_internal_movements = TRUE
ORDER BY TRANSACTION_DATE ASC
