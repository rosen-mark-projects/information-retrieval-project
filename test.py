import os

import tweepy as tw
import pandas as pd
from dotenv import load_dotenv


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.env'), override=True)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "Birmingham Wholesale Market is ablaze BBC News - Fire breaks out at Birmingham's Wholesale Market http://t.co/irWqCEZWEU"
date_since = "2020-01-30"

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(1)

tweet = api.get_status(629195955506708480)

print(tweet.id)
print(tweet.text)
print(tweet._json)
