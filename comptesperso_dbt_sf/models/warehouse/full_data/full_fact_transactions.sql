{{config(materialized='table')}}
SELECT
    {{dbt_utils.star(ref('fact_with_spend_from_income_expenses'))}}
FROM {{ ref('fact_with_spend_from_income_expenses') }}