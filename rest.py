import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.env'), override=True)

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASS = os.environ.get('POSTGRES_PASS')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'tweet_db')
conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER,
                        password=POSTGRES_PASS, host=POSTGRES_HOST)


app = Flask(__name__)
CORS(app)


@app.route('/tweets', methods=['GET'])
def get_tweets():
    keyword = request.args['text']
    print(keyword)
    tweets = get_tweets_from_db(keyword)
    respData = convert_to_dicts(tweets)
    response = jsonify(respData)
    return response


def get_tweets_from_db(keyword):
    cur = conn.cursor()
    cur.execute(
        f"SELECT text, keyword, url FROM disaster_tweets WHERE keyword='{keyword}'")
    data = cur.fetchall()
    return data
    # TODO


def convert_to_dicts(tweets):
    dicts = []
    for tweet in tweets:
        dict = {}
        dict['text'] = tweet[0]
        dict['keyword'] = tweet[1]
        dict['url'] = tweet[2]
        dict['target'] = 0
        dicts.append(dict)

    return dicts


app.run()
