import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow_hub as hub

from feature_creator import create_features
from tweet_cleaner import clean_tweet
from tweet_relabeler import relabel_tweets

import tokenization


def process_data(training, test):
    training['keyword'] = training['keyword'].fillna('no_keyword')
    test['keyword'] = test['keyword'].fillna('no_keyword')
    training = training.fillna(0)
    test = test.fillna(0)

    dfs = create_features(training, test)
    training = dfs[0]
    test = dfs[1]

    training['clean_text'] = training['text'].apply(lambda tweet: clean_tweet(tweet))
    test['clean_text'] = test['text'].apply(lambda tweet: clean_tweet(tweet))

    training = relabel_tweets(training)

    return [training, test]

def encode_tweets(tweets, tokenizer, max_length=512):
    tokens = []
    masks = []
    segments = []
    meta_features_count = 7

    for index, row in tweets.iterrows():
        tweet = tokenizer.tokenize(row.text)
        keyword = tokenizer.tokenize(row.keyword)

        tweet = tweet[:max_length - 2]
        inputs = ["[CLS]"] + keyword + tweet + ["[SEP]"]
        pad_length = max_length - len(inputs)

        current_tokens = tokenizer.convert_tokens_to_ids(inputs)
        current_tokens += [row.words, row.unique_words, row.stop_words, row.urls, row.mean_word_length, row.hashtags, row.mentionings]
        pad_length -= meta_features_count # decrement with meta features count
        current_tokens += [0] * pad_length
        pad_masks = [1] * len(inputs) + [1] * meta_features_count + [0] * pad_length
        segment_ids = [0] * max_length

        tokens.append(current_tokens)
        masks.append(pad_masks)
        segments.append(segment_ids)

    return np.array(tokens), np.array(masks), np.array(segments)


def create_bert_model(layer, max_length=512):
    ids = Input(shape=(max_length,), dtype=tf.int32, name="input_word_ids")
    mask = Input(shape=(max_length,), dtype=tf.int32, name="input_mask")
    segments = Input(shape=(max_length,), dtype=tf.int32, name="segment_ids")

    _, output = layer([ids, mask, segments])
    clf_output = output[:, 0, :]
    out = Dense(1, activation='sigmoid')(clf_output)

    result_model = Model(inputs=[ids, mask, segments], outputs=out)
    result_model.compile(Adam(lr=2e-6), loss='binary_crossentropy', metrics=['accuracy'])

    return result_model

bert_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"
bert_layer = hub.KerasLayer(bert_url, trainable=True)

training_data = pd.read_csv("./../train.csv")
test_data = pd.read_csv("./../test.csv")
training_data = training_data[:10]
test_data = test_data[:10]

processed_data = process_data(training_data, test_data)
training_data = processed_data[0]
test_data = processed_data[1]

vocabulary = bert_layer.resolved_object.vocab_file.asset_path.numpy()
lowercase = bert_layer.resolved_object.do_lower_case.numpy()
full_tokenizer = tokenization.FullTokenizer(vocabulary, lowercase)

training_input = encode_tweets(training_data, full_tokenizer, max_length=160)
test_input = encode_tweets(test_data, full_tokenizer, max_length=160)

training_targets = training_data.target.values

bert_model = create_bert_model(bert_layer, max_length=160)
bert_model.summary()

train_history = bert_model.fit(
    training_input, training_targets,
    validation_split=0.2,
    epochs=3,
    batch_size=16
)

prediction = bert_model.predict(test_input)

print(prediction)