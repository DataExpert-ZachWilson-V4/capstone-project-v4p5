CREATE OR REPLACE TABLE sandbox.user 
(
    author_id varchar,
    followers bigint,
    processed_date date
)
WITH (
  format = 'PARQUET',
  partitioning = ARRAY['date']
)

