SELECT
TO_VARCHAR(transaction_date, 'yyyy-MM') AS YEAR_MONTH,
SUM(SPEND) AS SPEND
FROM
    {{ref('scopein_fact_transactions')}} as a
WHERE PERSONAL_IBAN = 'DE****3827'
GROUP BY 1
ORDER BY 1 ASC