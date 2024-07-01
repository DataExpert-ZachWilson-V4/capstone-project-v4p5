from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'tweets_processing_dag',
    default_args=default_args,
    description='A simple DAG to process tweets and perform sentiment analysis',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Task to run tweets_processor.py
    run_tweets_processor = BashOperator(
        task_id='run_tweets_processor',
        bash_command='python /Users/vaishnaviaienampudi/git/capstone-project-v4p5/src/jobs/tweets_etl_processor.py',
    )

    # Task to run sentiment_analysis.py
    run_sentiment_analysis = BashOperator(
        task_id='run_sentiment_analysis',
        bash_command='python /Users/vaishnaviaienampudi/git/capstone-project-v4p5/src/jobs/tweets_sentiment.py',
    )

    # Define the task dependencies
    run_tweets_processor >> run_sentiment_analysis
