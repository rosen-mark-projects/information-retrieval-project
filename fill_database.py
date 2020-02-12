import os
import psycopg2
import tweepy as tw

from dotenv import load_dotenv
from create_database import loadSession

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.env'), override=True)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

def read_keywords():
    with open('keywords.txt', 'r') as keywords_file:
        keywords = keywords_file.read()
        for keyword in keywords:
            tweets = get_tweets_for_keyword(keyword)
            fill_tweets_in_db(tweets)

def get_tweets_for_keyword(keyword):
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(api.search, q=keyword, lang="en", since="2020-02-01").items(10)
    dicts = []
    for tweet in tweets:
        dict = {}
        dict['text'] = tweet.text
        dict['tweet_id'] = tweet.id
        dict['keyword'] = keyword
        dict['url'] = stitch(tweet.user.screen_name, tweet.id_str)
        dicts.append(dict)

    return dicts

def fill_tweets_in_db(tweets):
    pass

def stitch(screen_name, tweet_id):
    base = 'https://twitter.com/{}/status/{}'.format(screen_name, tweet_id)
    return base

if __name__ == '__main__':
    read_keywords()