import glob
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType

# Initialize Spark session
#spark = SparkSession.builder.appName("TweetsData").getOrCreate()

# Define the schema for the DataFrame
schema = StructType([
    StructField("TweetID", StringType(), True),
    StructField("Text", StringType(), True),
    StructField("CreatedAt", StringType(), True),
    StructField("AuthorID", StringType(), True),
    StructField("Followers Count", LongType(), True),
    StructField("Likes", LongType(), True),
    StructField("Retweets", LongType(), True),
    StructField("Replies", LongType(), True),
    StructField("Geo", StringType(), True)
])

# Define the directory containing the tweet files
file_pattern = '/dbfs/FileStore/shared_uploads/vaienampudi@expediagroup.com/*tweets*.txt'

# Find all files matching the pattern
file_paths = glob.glob(file_pattern)

# Initialize list to store all tweet data
data = []

# Read and parse each file
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            try:
                tweet_id_str = lines[i].split('.')[0].strip()
                tweet_id = int(tweet_id_str) if tweet_id_str.isdigit() else None
                
                # Extracting the text correctly
                tweet_text = lines[i].split('.', 1)[1].strip() if len(lines[i].split('.', 1)) > 1 else None
                if tweet_text and not lines[i+1].startswith("   Created at:"):
                    tweet_text += " " + lines[i+1].strip()
                    i += 1
                
                created_at = lines[i+1].split(': ', 1)[1].strip() if i+1 < len(lines) and lines[i+1].startswith("   Created at:") else None
                author_id_str = lines[i+2].split(': ', 1)[1].strip() if i+2 < len(lines) and lines[i+2].startswith("   Author ID:") else None
                author_id = int(author_id_str) if author_id_str and author_id_str.isdigit() else None
                followers_count_str = lines[i+3].split(': ', 1)[1].strip() if i+3 < len(lines) and lines[i+3].startswith("   Followers:") else None
                followers_count = int(followers_count_str) if followers_count_str and followers_count_str.isdigit() else None
                likes_str = lines[i+4].split(': ', 1)[1].strip() if i+4 < len(lines) and lines[i+4].startswith("   Likes:") else None
                likes = int(likes_str) if likes_str and likes_str.isdigit() else None
                retweets_str = lines[i+5].split(': ', 1)[1].strip() if i+5 < len(lines) and lines[i+5].startswith("   Retweets:") else None
                retweets = int(retweets_str) if retweets_str and retweets_str.isdigit() else None
                replies_str = lines[i+6].split(': ', 1)[1].strip() if i+6 < len(lines) and lines[i+6].startswith("   Replies:") else None
                replies = int(replies_str) if replies_str and replies_str.isdigit() else None
                geo = lines[i+7].split(': ', 1)[1].strip() if i+7 < len(lines) and lines[i+7].startswith("   Geo:") else None
                
                data.append((tweet_id, tweet_text, created_at, author_id, followers_count, likes, retweets, replies, geo))
                i += 8  # Move to the next record
            except (IndexError, ValueError) as e:
                print(f"Error parsing lines around line {i} in file {file_path}: {e}")
                i += 8  # Move to the next record, skipping the faulty one

# Filter out any rows where tweet_id is None
data = [row for row in data if row[0] is not None]



# Create a DataFrame
df = spark.createDataFrame(data, schema)
df = df.withColumnRenamed("Text", "tweet_text")\
       .withColumnRenamed("TweetID", "tweet_id")\
       .withColumnRenamed("CreatedAt", "created_at")\
       .withColumnRenamed("AuthorID", "author_id")\
       .withColumnRenamed("FollowersCount", "followers_count")
# create a table
df.write.mode('overwrite').saveAsTable('sandbox.tweets')
