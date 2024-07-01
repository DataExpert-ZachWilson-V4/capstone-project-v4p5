# sentiment_analysis.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType
from textblob import TextBlob
from tweets_processor import TweetsProcessor

# Define the sentiment analysis function using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Register the function as a UDF
get_sentiment_udf = udf(get_sentiment, DoubleType())

def perform_sentiment_analysis(df):
    # Apply the UDF to the DataFrame
    df_with_sentiment = df.withColumn('sentiment', get_sentiment_udf(col('tweet_text')))
    
    # Show the DataFrame with sentiment scores
    df_with_sentiment.show()

    # Write to a table
    df_with_sentiment.write.mode('overwrite').saveAsTable('sandbox.tweets_sentiment')

    return df_with_sentiment


# Example usage
if __name__ == "__main__":
    # Initialize Spark session
    spark = SparkSession.builder.appName("SentimentAnalysis").getOrCreate()

    # Define the directory containing the tweet files
    file_pattern = '/dbfs/FileStore/shared_uploads/vaienampudi@expediagroup.com/*tweets*.txt'

    # Initialize the processor
    processor = TweetsProcessor(spark, file_pattern)

    # Read files and parse data
    processor.read_files()

    # Create DataFrame
    df = processor.create_dataframe()

    # Save DataFrame as a table
    df.write.mode('overwrite').saveAsTable('sandbox.dim_tweets')

    # Perform sentiment analysis
    df_with_sentiment = perform_sentiment_analysis(df)
