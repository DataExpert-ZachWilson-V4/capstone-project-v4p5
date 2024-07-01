# tweets_processor.py

import glob
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType

class TweetsProcessor:
    def __init__(self, spark, file_pattern):
        self.spark = spark
        self.file_pattern = file_pattern
        self.schema = StructType([
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
        self.data = []

    def read_files(self):
        # Find all files matching the pattern
        file_paths = glob.glob(self.file_pattern)
        
        # Read and parse each file
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                self.parse_lines(lines, file_path)
        
        # Filter out any rows where tweet_id is None
        self.data = [row for row in self.data if row[0] is not None]

    def parse_lines(self, lines, file_path):
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
                
                self.data.append((tweet_id, tweet_text, created_at, author_id, followers_count, likes, retweets, replies, geo))
                i += 8  # Move to the next record
            except (IndexError, ValueError) as e:
                print(f"Error parsing lines around line {i} in file {file_path}: {e}")
                i += 8  # Move to the next record, skipping the faulty one

    def create_dataframe(self):
        # Create a DataFrame from the data
        df = self.spark.createDataFrame(self.data, self.schema)
        df = df.withColumnRenamed("Text", "tweet_text")\
               .withColumnRenamed("TweetID", "tweet_id")\
               .withColumnRenamed("CreatedAt", "created_at")\
               .withColumnRenamed("AuthorID", "author_id")\
               .withColumnRenamed("Followers Count", "followers_count")
        return df


# Example usage
if __name__ == "__main__":
    # Initialize Spark session
    spark = SparkSession.builder.appName("TweetsData").getOrCreate()

    # Define the directory containing the tweet files
    file_pattern = '/dbfs/FileStore/shared_uploads/vaienampudi@expediagroup.com/*tweets*.txt'

    # Initialize the processor
    processor = TweetsProcessor(spark, file_pattern)

    # Read files and parse data
    processor.read_files()

    # Create DataFrame
    df = processor.create_dataframe()

    # Show the DataFrame
    df.show()
