import os

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import keras

from config import conn, PROJECT_PATH
from models.Sentence_encoder.clean import clean_text
from models.Sentence_encoder.build_model import create_model
from models.bert_model.bert_model import process_data
from models.bert_model.create_bert_model import load_bert, create_bert_model

app = Flask(__name__)
CORS(app)

model = create_model()
model.load_weights(os.path.join(PROJECT_PATH, "models/Sentence_encoder/weights.best.hdf5"))

# for bert model
# bert_layer, full_tokenizer = load_bert()
# model = create_bert_model(bert_layer, max_length=160)
# model = keras.models.load_model(os.path.join(PROJECT_PATH, "models/bert_model/bert_weights.h5"))

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
    tweets_df = pd.DataFrame(tweets, columns=['text', 'keyword', 'url'])
    tweets_prediction = clean_text(tweets_df)
    pred_Y = model.predict(tweets_prediction['text'])
    tweets_df['target'] = pred_Y.round().astype(int)
    print(pred_Y)

    # for bert prediction
    # tweets_df = pd.DataFrame(tweets, columns=['text', 'keyword', 'url'])
    # tweets_data = process_data(tweets_df)
    # tweets_data = encode_tweets(tweets_df, full_tokenizer, max_length=160)
    # pred_Y = model.predict(tweets_data)
    # tweets_df['target'] = pred_Y.round().astype(int)
    return tweets_df.to_dict(orient='records')


app.run()
