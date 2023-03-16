SELECT
    c.pair_id,
    count(c.transaction_id)  as pair_count,
    ROUND(sum(c.amount), 2) as pair_sum
FROM
    (SELECT
            a.transaction_id, a.amount, b.pair_id
    FROM {{ref('formatstage')}} as a
    LEFT JOIN {{ref('prepare_self_cancelling_transactions')}} as b ON a.transaction_id = b.transaction_id
    WHERE b.pair_id IS NOT NULL
    ) as c
GROUP BY c.pair_id