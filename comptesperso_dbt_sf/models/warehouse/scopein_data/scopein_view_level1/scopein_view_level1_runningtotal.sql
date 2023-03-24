SELECT
YEAR_MONTH, INCOME, EXPENSES, SAVINGS, BALANCE, NET_INCOME,
sum(savings) over (order by YEAR_MONTH asc rows between unbounded preceding and current row) AS CUMULATIVE_SAVINGS,
sum(balance) over (order by YEAR_MONTH asc rows between unbounded preceding and current row) AS CUMULATIVE_BALANCE,
sum(net_income) over (order by YEAR_MONTH asc rows between unbounded preceding and current row) AS CUMULATIVE_NET_INCOME
FROM {{ref('scopein_view_level1_pivot')}}
