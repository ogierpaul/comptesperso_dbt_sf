SELECT
a.TRANSACTION_ID,
c.pair_id,
CASE when c.pair_id IS NOT NULL
    THEN 'ScopeOut'
ELSE
    CASE WHEN b.txt_category_lvl3 IS NOT NULL
        THEN b.txt_category_lvl3
    ELSE
        a.txt_category_lvl3
    END
END AS TXT_CATEGORY_LVL3,
CASE when c.pair_id IS NOT NULL
    THEN TRUE
ELSE
    CASE WHEN b.scope_out IS NOT NULL
        THEN b.scope_out
    ELSE
        a.scope_out
    END
END AS scope_out,
CASE when c.pair_id IS NOT NULL
    THEN TRUE
ELSE
    CASE WHEN b.is_transfer IS NOT NULL
        THEN b.is_transfer
    ELSE
        a.is_transfer
    END
END AS is_transfer,
  a.TRANSACTION_DATE,
  a.NAME_PERSONAL_ACCOUNT,
  a.AMOUNT,
  a.ACCOUNT_BALANCE,
  a.TRANSACTION_DESCRIPTION,
  a.BENEFICIARY_IBAN,
  a.FINANZGURU_CATEGORY_LVL1,
  a.FINANZGURU_CATEGORY_LVL2,
  a.IS_CONTRACT,
  a.CONTRACT_RECURRENCE,
  a.CONTRACT_ID,
  a.TRANSACTION_TYPE,
  a.INCOME_EXPENSE,
  a.PERSONAL_IBAN,
  a.FILENAME,
  a.PROCESSING_DATE,
  a.RECEIVER_IS_PERSONAL_ACCOUNT_FLAG,
  a.BENEFICIARY,
a.beneficiary_iban_masked,
(c.pair_id IS NOT NULL) AS is_self_cancelling_transaction,
CASE WHEN d.preferred_category = 'InternalMovements' AND e.preferred_category = 'InternalMovements' THEN TRUE ELSE FALSE END AS accounts_are_both_internal_movements,
d.preferred_category as beneficiary_account_preferred_category
FROM {{ref('fact_with_receiver_is_account_flag')}} a
LEFT JOIN {{ref('prepare_transaction_id_details')}} b USING(transaction_id)
LEFT JOIN {{ref('prepare_self_cancelling_transactions')}} c USING(transaction_id)
LEFT JOIN {{ref('accounts')}} as d ON a.beneficiary_iban_masked = d.account_iban
LEFT JOIN {{ref('accounts')}} as e on a.personal_iban = e.account_iban