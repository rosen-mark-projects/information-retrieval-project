from flask import Flask, request, jsonify
import psycopg2

conn = psycopg2.connect(database="tweetdb", user="postgres", password="test", host="127.0.0.1", port="5432")


api = Flask(__name__)

@api.route('/tweets', methods=['GET'])
def get_tweets():
    text = request.args['text']
    print(text)
    # tweets = get_tweets_from_db()
    tweets = [['1', 'Test test'], ['2', 'test 2']]
    response = jsonify(tweets)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def get_tweets_from_db():
    pass
    # TODO


api.run()