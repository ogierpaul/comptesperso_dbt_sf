SELECT
a.TRANSACTION_ID ,
a.TRANSACTION_DATE,
COALESCE(b.account_name,  a.NAME_PERSONAL_ACCOUNT ) AS NAME_PERSONAL_ACCOUNT,
a.AMOUNT,
a.ACCOUNT_BALANCE,
a.TRANSACTION_DESCRIPTION ,
a.BENEFICIARY_IBAN,
a.FINANZGURU_CATEGORY_LVL1,
a.FINANZGURU_CATEGORY_LVL2,
a.IS_CONTRACT,
a.CONTRACT_RECURRENCE,
a.CONTRACT_ID,
a.IS_TRANSFER ,
a.SCOPE_OUT,
a.TRANSACTION_TYPE,
a.INCOME_EXPENSE,
a.PERSONAL_IBAN,
a.FILENAME,
a.PROCESSING_DATE,
a.TXT_CATEGORY_LVL3,
a.beneficiary_iban_masked,
a.beneficiary
FROM
    {{ref('translate_to_english')}} as a
LEFT JOIN
    {{ref('accounts')}} as b ON a.personal_iban = b.account_iban