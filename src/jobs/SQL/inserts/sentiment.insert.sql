INSERT OVERWRITE sandbox.sentiment
select tweet_id,
       sentiment_score,
       sentiment_value,
       processed_date
from sandbox.dim_tweets