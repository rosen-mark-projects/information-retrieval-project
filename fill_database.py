import os
import psycopg2
import tweepy as tw

from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert

from create_database import loadSession, Tweets
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def read_keywords():
    with open('keywords.txt', 'r') as keywords_file:
        for line in ['wildfire', 'earthquake']:
            for keyword in line.split():
                print(keyword)
                tweets = get_tweets_for_keyword(keyword)
                fill_tweets_in_db(tweets)

def get_tweets_for_keyword(keyword):
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(api.search, q=keyword + ' -filter:retweets', lang="en", since="2020-02-01", 
                        tweet_mode="extended", exclude_replies=True).items(10)
    dicts = []
    for tweet in tweets:
        dict = {}
        dict['user_id'] = tweet.user.id
        dict['datetime'] = tweet.created_at
        dict['text'] = tweet.full_text
        dict['tweet_id'] = tweet.id
        dict['keyword'] = keyword
        dict['url'] = stitch(tweet.user.screen_name, tweet.id_str)
        dicts.append(dict)

    return dicts

def fill_tweets_in_db(result):
    # write to db
    print(result[0])
    insert_stmt = insert(Tweets).values(result)

    do_update_stmt = insert_stmt.on_conflict_do_update(
        constraint='tweet_id_datetime_uc',
        set_=dict(insert_stmt.excluded)
    )

    session = loadSession()
    session.execute(do_update_stmt)
    session.commit()

def stitch(screen_name, tweet_id):
    base = 'https://twitter.com/{}/status/{}'.format(screen_name, tweet_id)
    return base

if __name__ == '__main__':
    read_keywords()
