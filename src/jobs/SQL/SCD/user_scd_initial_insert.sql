INSERT OVERWRITE user_scd
with authors as (
    select author_id, followers, processed_date
    from sandbox.tweets
),
calculate_next_processed_date as (
    select *, lead(processed_date,1) over (partition by author_id order by processed_date) as next_processed_date
    from authors
),

select author_id, 
       followers, 
       processed_date as start_date,  
        case when next_processed_date is null then '9999-12-31' 
             when next_processed_date is not null then (next_processed_date - 1) 
             end as end_date, 
        case when next_processed_date is null then 'Y' else 'N' end as current_flag
