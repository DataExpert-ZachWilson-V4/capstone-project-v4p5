[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/1lXY_Wlg)

# US Election Pulse from Twitter

## Problem We Want to Solve
I am trying to get the pulse on what people are sharing about the leaders from both the parties democrats and republicans. How many tweets are being shared for each of them with likes, comments, reshares, etc.. I am also trying to analyse the sentiment of the tweets whether they are positive or negative. 

## Data Sources:
Using Twitter API V2. The version that allows us to extract tweets from twitter is not free. 
There are 2 versions of the API. One that allows to retrieve historical tweets and other that allows to retrieve tweets real time. 
Documentation on Twitter API - https://developer.x.com/en/docs/twitter-api/tweets/search/introduction

Open AI API - Used to generate some dummy tweets.

## Conceptual Data Model:
    +------------+        +-----------+        +-----------------+
    |   User     |        |   Tweet   |        |  Sentiment      |
    +------------+        +-----------+        +-----------------+
    | Author_id  |<-----+ | Tweet_id  | <----+ | Tweet_id        |
    | Followers  |        | Tweet_txt |        | Sentiment_Score |
    +------------+        | Created_At|        | Sentiment_Label |
                          | Author_id |        +-----------------+
                          | Followers | 
                          | Likes     |
                          | Retweets  |
                          | Replies   |
                          | Geo       |
                          |load_date  |
                          | Sentiment |
                          +-----------+

SCD Table: 

    +------------------+
    |   User_SCD       |
    +------------------+
    | Surrogate_Key    |
    | Author_id        |
    | Followers        |
    | Start_Date       |
    | End_Date         |
    | Current_Flag     |
    +------------------+
                               
## Dataset:
By using twitter V2 API, I have extracted tweets that contain either Biden or Trump in the tweet.
My code will search for either of the keywords and writes them to a file. 
Because twitter API is not for free, I have also generated few fake tweets by using Open AI API
The goal is to perform data analysis on high volume which is partially realtime. 
The dataset contains the following fields: 
Tweet_id - This is a unique identifier for each tweet.
Tweet_txt - Contains the actual tweet with original text and/or special characters.
Created_At - This is a timestamp field, that contains the timestamp at which the tweets has been posted.
Author_id - Contains an long int numeric value that is tied to a tweet/user. 
Followers - The number of followers, the user have at the time the tweet is extracted.
Likes - Number of likes the tweet has when the tweet is extracted.
Retweets - Number of retweets on the tweet when the tweet is extracted.
Replies - Number of replies on the tweet when the tweet is extracted.
Geo - The Geo location from where the tweets have been posted. 
Sentiment - This is a created field using NLP library (nltk). It has both negative and positive values. 
filter_keyword - This is a created field that contains the leader of either parties. The value which the tweet contains. 
processed_date - This contains a date value from the filename from which the data is extracted.

## Desired Insights: 
As stated previously, we are trying to achieve the pulse of people posting on twitter regarding the upcoming US elections. 
We are also trying to achieve if any of the users are consistent on posting/tweeting daily on the similar topics. 
The above data set helps to achieve the following: 
 - Most engaged user.
 - Most popular tweet. 
 - Number of tweets based on sentiment.

Below are the tables that have been created from the data set. 

Tweets: This is the master dataset that contains all the above columns extracted from twitter v2 API and the date on which the data is extracted. The source for this table are the .txt files that have been extracted. 

Below are the SCD tables that have been created. The idea of creating SCD tables is trying to depict the original data engineering space and how the SCD tables add more value and support reporting historically. It helps to give and idea of the data over a period of time. 

User_SCD: This SCD table tracks the number of followers the user has. If the user is active regularly,the possibility of increase in followers everyday is high. Because we are not tracking the user activity regukarly, we can only track the activity based on the tweets, the user has posted. 

## Data Flow: 
![data flow](https://github.com/DataExpert-ZachWilson-V4/capstone-project-v4p5/blob/capstone_vaishnavi5054/blob/Screenshot%202024-06-30%20at%2016.46.32.png)

Note:
This is just a sample data and do not depict any realtime conclusions. This is not intended to mislead anyone. 

## Dashboard results:

### Likes_retweets_by_leader:
![Likes_retweets_by_leader](https://github.com/DataExpert-ZachWilson-V4/capstone-project-v4p5/blob/capstone_vaishnavi5054/blob/Likes%2Cretweets%2Ccomments_by_leader.png)

### Tweets with more than million likes, retweets per each leader along with the tweets sentiment

![pic2](https://github.com/DataExpert-ZachWilson-V4/capstone-project-v4p5/blob/capstone_vaishnavi5054/blob/tweets_with_more_than_million_likes_retweets_by_each_leader_along_with_sentiment.png)

### Total sentiment, likes, retweets for each leader:

![pic3](https://github.com/DataExpert-ZachWilson-V4/capstone-project-v4p5/blob/capstone_vaishnavi5054/blob/Total_sentiment_for_each_leader.png)
