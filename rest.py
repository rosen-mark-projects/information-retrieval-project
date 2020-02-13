import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import conn


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
        "SELECT text, keyword, url FROM disaster_tweets WHERE keyword='{}'".format(keyword))
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
