SELECT
    {{dbt_utils.star(ref('joinaccounts'))}}
FROM
    {{ ref('joinaccounts') }}