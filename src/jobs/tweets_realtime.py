import tweepy
import time
from datetime import datetime

def get_recent_tweets(client, keyword1, keyword2, max_results=100, next_token=None):
    query = f'({keyword1} OR #{keyword1} OR {keyword2} OR #{keyword2}) -is:retweet'
    tweets = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=['created_at', 'text', 'public_metrics', 'geo', 'author_id'],
        user_fields=['public_metrics'],
        expansions=['author_id'],
        next_token=next_token
    )
    return tweets

def write_tweets_to_file(tweets, users, filename):
    user_dict = {user['id']: user for user in users}
    with open(filename, 'a', encoding='utf-8') as file:
        for tweet in tweets:
            tweet_text = tweet.get('text', '')
            created_at = tweet.get('created_at', '')
            public_metrics = tweet.get('public_metrics', {})
            likes = public_metrics.get('like_count', 0)
            retweets = public_metrics.get('retweet_count', 0)
            replies = public_metrics.get('reply_count', 0)
            geo = tweet.get('geo', {})
            geo_info = geo.get('place_id', '') if geo else 'N/A'
            author_id = tweet.get('author_id', 'N/A')
            author_info = user_dict.get(author_id, {})
            followers_count = author_info.get('public_metrics', {}).get('followers_count', 'N/A')

            file.write(f"{tweet.id}. {tweet_text}\n")
            file.write(f"   Created at: {created_at}\n")
            file.write(f"   Author ID: {author_id}\n")
            file.write(f"   Followers: {followers_count}\n")
            file.write(f"   Likes: {likes}\n")
            file.write(f"   Retweets: {retweets}\n")
            file.write(f"   Replies: {replies}\n")
            file.write(f"   Geo: {geo_info}\n\n")
    print(f"Tweets have been written to {filename}")

def main():
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPdEuQEAAAAA5%2FI7IwqoiW7J%2FjIf4ZR94h9TpYY%3DGM5gzophFPbGadPwUugM4bQDpIchSA9pwgoAQnq1QrAsHsQHqp'
    keyword1 = input("Enter the first keyword to search for tweets: ")
    keyword2 = input("Enter the second keyword to search for tweets: ")
    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"tweets_{current_timestamp}.txt"

    #filename = "tweets_3.txt"
    max_tweets = 10000

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    next_token = None
    total_tweets = 0

    # Clear the file before writing new tweets
    open(filename, 'w').close()

    while total_tweets < max_tweets:
        try:
            tweets_response = get_recent_tweets(client, keyword1, keyword2, next_token=next_token)
            if tweets_response.data:
                users = tweets_response.includes['users']
                write_tweets_to_file(tweets_response.data, users, filename)
                total_tweets += len(tweets_response.data)
                next_token = tweets_response.meta.get('next_token')
                if not next_token:
                    print("No more tweets found.")
                    break
            else:
                print("No tweets found for the given query.")
                break

            # Wait for a short time before making the next request to avoid hitting rate limits
            time.sleep(1)

        except tweepy.TweepyException as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait for a minute before trying again

    print(f"Total tweets fetched: {total_tweets}")

if __name__ == "__main__":
    main()
