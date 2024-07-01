#does historical search for tweets
import tweepy

def get_recent_tweets(keyword, max_results=10000):
    # Replace these values with your own keys and tokens
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPdEuQEAAAAAYoq2An%2BcyIbFLWd58aUCws1UDcg%3DZTPxYYqr22NwhpD8iTm6DbCwDtf2xSpG5AgHXZ26EGzMGaolTg'
    # Set up the Tweepy client
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    # Fetch recent tweets
    query = f'{keyword} -is:retweet'
    tweets = []
    next_token = None

    while len(tweets) < max_results:
        response = client.search_recent_tweets(
            query=query,
            max_results=min(100, max_results - len(tweets)),
            tweet_fields=['created_at', 'text', 'public_metrics', 'geo'],
            next_token=next_token
        )
        if 'data' in response:
            tweets.extend(response.data)
            print(f"Fetched {len(response.data)} tweets, total fetched: {len(tweets)}")
        else:
            print("No more tweets found.")
            break

        next_token = response.meta.get('next_token', None)
        if not next_token:
            break

    tweet_list = []
    for tweet in tweets:
        tweet_info = {
            "text": tweet.text,
            "created_at": tweet.created_at,
            "likes": tweet.public_metrics['like_count'],
            "retweets": tweet.public_metrics['retweet_count'],
            "replies": tweet.public_metrics['reply_count'],
            "geo": tweet.geo
        }
        tweet_list.append(tweet_info)

    return tweet_list

def write_tweets_to_file(tweets, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for idx, tweet in enumerate(tweets):
            file.write(f"{idx+1}. {tweet['text']}\n")
            file.write(f"   Created at: {tweet['created_at']}\n")
            file.write(f"   Likes: {tweet['likes']}\n")
            file.write(f"   Retweets: {tweet['retweets']}\n")
            file.write(f"   Replies: {tweet['replies']}\n")
            file.write(f"   Geo: {tweet['geo']}\n\n")
    print(f"Tweets have been written to {filename}")

if __name__ == "__main__":
    keyword = input("Enter keyword to search for tweets: ")
    max_results = int(input("Enter number of tweets to retrieve (max 10000): "))  # Adjust the max value to 10000

    tweets = get_recent_tweets(keyword, max_results)
    
    filename = "tweets.txt"
    write_tweets_to_file(tweets, filename)
    
    for idx, tweet in enumerate(tweets):
        print(f"{idx+1}. {tweet['text']}")
        print(f"   Created at: {tweet['created_at']}")
        print(f"   Likes: {tweet['likes']}")
        print(f"   Retweets: {tweet['retweets']}")
        print(f"   Replies: {tweet['replies']}")
        print(f"   Geo: {tweet['geo']}\n")
