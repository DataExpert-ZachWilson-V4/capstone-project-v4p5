from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import DoubleType
from textblob import TextBlob
import nltk




df = spark.table("sandbox.tweets")

# Define the sentiment analysis function using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Register the function as a UDF
get_sentiment_udf = udf(get_sentiment, DoubleType())

# Apply the UDF to the DataFrame
df_with_sentiment = df.withColumn('sentiment', get_sentiment_udf(col('tweet_text')))

# Show the DataFrame with sentiment scores
display(df_with_sentiment)

#write to a table:
df_with_sentiment.write.mode('overwrite').saveAsTable('tweets_sentiment')