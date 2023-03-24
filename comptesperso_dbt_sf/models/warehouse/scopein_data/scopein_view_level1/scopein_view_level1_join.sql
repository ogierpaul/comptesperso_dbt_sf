SELECT
TO_VARCHAR(transaction_date, 'yyyy-MM') AS YEAR_MONTH,
TXT_CATEGORY_LVL1,
SUM(SPEND) AS SPEND
FROM
    {{ref('scopein_fact_transactions')}} as a
LEFT JOIN {{ref('scopein_dim_category')}} b USING(TXT_CATEGORY_LVL3)
GROUP BY 1, 2
ORDER BY 1, 2 ASC