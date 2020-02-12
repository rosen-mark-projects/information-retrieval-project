from flask import Flask, request, jsonify
import psycopg2

conn = psycopg2.connect(database="tweet_db", user="postgres", password="postgres", host="127.0.0.1", port="5432")


app = Flask(__name__)

@app.route('/tweets', methods=['GET'])
def get_tweets():
    keyword = request.args['text']
    print(keyword)
    tweets = get_tweets_from_db(keyword)
    respData = convert_to_dicts(tweets)
    response = jsonify(respData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def get_tweets_from_db(keyword):
    cur = conn.cursor()
    cur.execute(f'SELECT text, keyword, link FROM disaster_tweets WHERE keyword={keyword}')
    data = cur.fetchall()
    return data
    # TODO

def convert_to_dicts(tweets):
    dicts = []
    for tweet in tweets:
        dict = {}
        dict['text'] = tweet[1]
        dict['keyword'] = tweet[2]
        dict['link'] = tweet[3]
        dict['target'] = 0

    dicts.append(dict)
    return dicts

app.run()
