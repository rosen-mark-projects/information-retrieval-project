import os

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow_hub as hub

from models.bert_model.feature_creator import create_features
from models.bert_model.create_bert_model import create_bert_model, load_bert
from models.bert_model import tokenization

from config import PROJECT_PATH


def process_data(training):
    training['keyword'] = training['keyword'].fillna('no_keyword')
    training = training.fillna(0)

    training = create_features(training)

    return training


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
        current_tokens += [row.words, row.unique_words, row.stop_words,
                           row.urls, row.mean_word_length, row.hashtags, row.mentionings]
        pad_length -= meta_features_count  # decrement with meta features count
        current_tokens += [0] * pad_length
        pad_masks = [1] * len(inputs) + [1] * \
            meta_features_count + [0] * pad_length
        segment_ids = [0] * max_length

        tokens.append(current_tokens)
        masks.append(pad_masks)
        segments.append(segment_ids)

    return np.array(tokens), np.array(masks), np.array(segments)


if __name__ == '__main__':
    training_data = pd.read_csv(os.path.join(PROJECT_PATH, "models/train.csv"))

    training_data = training_data[:10]

    training_data = process_data(training_data)

    bert_layer, full_tokenizer = load_bert()

    training_input = encode_tweets(
        training_data, full_tokenizer, max_length=160)

    training_targets = training_data.target.values

    bert_model = create_bert_model(bert_layer, max_length=160)
    bert_model.summary()

    train_history = bert_model.fit(
        training_input, training_targets,
        validation_split=0.2,
        epochs=3,
        batch_size=16
    )

    bert_model.save_weights(os.path.join(
        PROJECT_PATH, 'models/bert_model/bert_weights.h5'))
