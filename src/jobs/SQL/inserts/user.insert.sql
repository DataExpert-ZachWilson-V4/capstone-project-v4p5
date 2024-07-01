INSERT OVERWRITE sandbox.user
select author_id,
       followers,
       processed_date
from sandbox.dim_tweets