--I have used NLP to determine whether the sentiment of the tweet is positive, negative or  neutral. 
-- If sentiment = 0, it means neutral, if it is <0 then it is negative and if sentiment >0 then positive
with sentiment as (
    select author_id, sentiment, 
    case when sentiment > 0 then 'positive'
         when sentiment < 0 then 'negative'
         when sentiment = 0 then 'neutral'
    end as sentiment_value
    from sandbox.tweets 
),
select sentiment_value, count(distinct tweets) as tweet_count
from sentiment
group by sentiment_value