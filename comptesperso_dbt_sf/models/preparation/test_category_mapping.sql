
with child as (
    select FINANZGURU_CATEGORY_LVL2 as from_field
    from {{ref('formatstage')}}
    where FINANZGURU_CATEGORY_LVL2 is not null
),

parent as (
    select TXT_CATEGORY_LVL3 as to_field
    from {{ref('categorytree')}}
)

select
    from_field,
    COUNT(*) as count
from child
left join parent
    on child.from_field = parent.to_field
where parent.to_field is null
GROUP BY 1
ORDER BY 2 DESC