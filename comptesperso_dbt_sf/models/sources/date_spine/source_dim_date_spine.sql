{{ dbt_utils.date_spine(
    datepart="day",
    start_date="to_date('01/01/2019', 'mm/dd/yyyy')",
    end_date="DATEADD(DAY, 31, current_date())")

}}
