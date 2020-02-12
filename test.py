import os
import tweepy as tw
import pandas as pd


consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "Birmingham Wholesale Market is ablaze BBC News - Fire breaks out at Birmingham's Wholesale Market http://t.co/irWqCEZWEU"
date_since = "2020-01-30"

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(1)

tweet = api.get_status(629195955506708480)

print(tweet.user.location)
print(tweet)
