# -*- coding = utf-8 -*-
# @Time:  2:21 下午
# @Author : tt
# @File: SentimentTwitter.py
# @Software: PyCharm


import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


##  STEP1 Get the Twitter API credentials
consumerKey = "*******************"
consumerSecret = "***********************************"
accessToken = "****************************************"
accessTokenSecret = "***********************************"


##  STEP2 Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
#Set the access token and the access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)
#Create the API
api = tweepy.API(authenticate, wait_on_rate_limit= True)

##   STEP3 Extract tweets from the twitter user
posts = api.user_timeline(screen_name = 'elonmusk',count = 200, lang = 'en',tweet_mode = 'extended')
#Create a dataframe with a column called Teets
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


##   STEP4 Clean Data
def cleanTwt(twt):
    twt = re.sub(r'@[A-Za-z0-9]+', '', twt)  # Removes @''
    twt = re.sub('\\n', '', twt)  # Removes the '\'n string
    twt = re.sub(r'https?:\/\/\S+', '', twt)  # Removes any hyperlinks
    twt = re.sub(r'RT[\s]+', '', twt)  # Removes 轉發

    return twt


df['Tweets'] = df['Tweets'].apply(cleanTwt)


##   STEP5 Create a function to get the subjectivity
def getSubjectivity(twt):
  return TextBlob(twt).sentiment.subjectivity
#Create a function to get the polarity
def getPolarity(twt):
  return TextBlob(twt).sentiment.polarity

#Create two new columns called 'Subjectivity' & 'Polarity'
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)


##   STEP6 Create a function to get the text sentiment
def getSentiment(score):
  if score < 0:
    return 'Negative'
  elif score ==0:
    return 'Netural'
  else:
    return 'Positive'

 #Create a column to store the text sentiment
df['Sentiment'] = df['Polarity'].apply(getSentiment)


##   STEP7 KEYWORD SEARCH
d =[]
e=[]
l =['bitcoin','Doge','Tesla']

df2 = pd.DataFrame(columns=['Tweets','Sentiment'])
for i in range(0,df.shape[0]):
  for c in l:
    if( c in  df['Tweets'][i]):
      e.append(df['Tweets'][i])
      d.append(df['Sentiment'][i])

df2['Tweets'] = e
df2['Sentiment'] =d

#Create a bar chart to show the count of Positive, Neutral and Negative sentiments
df2['Sentiment'].value_counts().plot(kind = 'bar')
print(df2['Sentiment'].value_counts())
plt.title('Sentiment Analysis {}'.format('Bitcoin'))

plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')
plt.show()
