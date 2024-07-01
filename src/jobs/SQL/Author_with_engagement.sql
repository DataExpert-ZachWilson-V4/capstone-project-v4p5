--User with more enagagement/popularity. We are taking sum of followers, likes, retweets, replies for each author_id and adding them. 
-- The author with more score gets row_number = 1

with author_details as(
select author_id, sum(followers) as followers, sum(likes) as likes, sum(retweets) as retweets, sum(replies) as replies
from sandbox.tweets
group by author_id ),

total_activity as (
    select author_id, (followers+likes+retweets+replies) as activity_details
    from author_details
)

select * row_number() over (partition by author_id order by activity_details desc)rn
from total_activity