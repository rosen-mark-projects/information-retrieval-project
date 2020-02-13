import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow_hub as hub

from feature_creator import create_features
from tweet_cleaner import clean
from tweet_relabeler import relabel_tweets

import tokenization


def bert_encode(text, tokenizer, max_len=512):
    all_tokens = []
    all_masks = []
    all_segments = []

    text = tokenizer.tokenize(text)

    text = text[:max_len - 2]
    input_sequence = ["[CLS]"] + text + ["[SEP]"]
    pad_len = max_len - len(input_sequence)

    tokens = tokenizer.convert_tokens_to_ids(input_sequence)
    tokens += [0] * pad_len
    pad_masks = [1] * len(input_sequence) + [0] * pad_len
    segment_ids = [0] * max_len

    all_tokens.append(tokens)
    all_masks.append(pad_masks)
    all_segments.append(segment_ids)

    return np.array(all_tokens), np.array(all_masks), np.array(all_segments)


def build_model(bert_layer, max_len=512):
    input_word_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_word_ids")
    input_mask = Input(shape=(max_len,), dtype=tf.int32, name="input_mask")
    segment_ids = Input(shape=(max_len,), dtype=tf.int32, name="segment_ids")

    _, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
    clf_output = sequence_output[:, 0, :]
    out = Dense(1, activation='sigmoid')(clf_output)

    model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=out)
    model.compile(Adam(lr=2e-6), loss='binary_crossentropy', metrics=['accuracy'])

    return model

module_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"
bert_layer = hub.KerasLayer(module_url, trainable=True)

train = pd.read_csv("./../train.csv")
test = pd.read_csv("./../test.csv")

train['keyword'] = train['keyword'].fillna('no_keyword')
test['keyword'] = test['keyword'].fillna('no_keyword')

train = train.fillna(0)
test = test.fillna(0)

train = train[0:1]
test = test[:1]

dfs = create_features(train, test)

train = dfs[0]
test = dfs[1]

train['text_cleaned'] = train['text'].apply(lambda s : clean(s))
test['text_cleaned'] = test['text'].apply(lambda s : clean(s))

train = relabel_tweets(train)

vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

all_train_input = []
all_test_input = []

for index, row in train.iterrows():
    train_input = bert_encode(row.text_cleaned, tokenizer, max_len=160)
    train_input_keywords = bert_encode(row.keyword, tokenizer, max_len=160)
    all_train_input.append(train_input)
    all_train_input.append(train_input_keywords)
    all_train_input.append(row.word_count)
    all_train_input.append(row.unique_word_count)
    all_train_input.append(row.stop_word_count)
    all_train_input.append(row.url_count)
    all_train_input.append(row.mean_word_length)
    all_train_input.append(row.char_count)
    all_train_input.append(row.punctuation_count)
    all_train_input.append(row.hashtag_count)
    all_train_input.append(row.mention_count)

for index, row in test.iterrows():
    test_input = bert_encode(row.text_cleaned, tokenizer, max_len=160)
    test_input_keywords = bert_encode(row.keyword, tokenizer, max_len=160)
    all_test_input.append(test_input)
    all_test_input.append(test_input_keywords)
    all_test_input.append(row.word_count)
    all_test_input.append(row.unique_word_count)
    all_test_input.append(row.stop_word_count)
    all_test_input.append(row.url_count)
    all_test_input.append(row.mean_word_length)
    all_test_input.append(row.char_count)
    all_test_input.append(row.punctuation_count)
    all_test_input.append(row.hashtag_count)
    all_test_input.append(row.mention_count)


train_labels = train.target.values


model = build_model(bert_layer, max_len=160)
model.summary()

# train_history = model.fit(
#     all_train_input, train_labels,
#     validation_split=0.2,
#     epochs=3,
#     batch_size=16
# )
#
# test_pred = model.predict(test_input)