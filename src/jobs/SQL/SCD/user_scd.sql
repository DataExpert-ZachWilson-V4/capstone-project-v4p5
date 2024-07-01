CREATE OR REPLACE TABLE sandbox.user_scd
(
    author_id varchar, --unique id for user/author
    followers bigint, -- number of followers at the time of processing the latest tweet for the author_id
    start_date date, -- start date will be the processed_date
    end_date date, --for the first row, the end date will be 9999-12-31. When we get the second row we use prev_start_date-1 and updaate the previous row
    current_flag boolean --indicates the current_row

)
WITH (
  format = 'PARQUET',
  partitioning = ARRAY['start_date']
)
