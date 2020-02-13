import gc
import re
import string
import operator
from collections import defaultdict
from wordcloud import STOPWORDS

import numpy as np


def create_features(df_train, df_test):
    # word_count
    df_train['word_count'] = df_train['text'].apply(lambda x: len(str(x).split()))
    df_test['word_count'] = df_test['text'].apply(lambda x: len(str(x).split()))

    # unique_word_count
    df_train['unique_word_count'] = df_train['text'].apply(lambda x: len(set(str(x).split())))
    df_test['unique_word_count'] = df_test['text'].apply(lambda x: len(set(str(x).split())))

    # stop_word_count
    df_train['stop_word_count'] = df_train['text'].apply(
        lambda x: len([w for w in str(x).lower().split() if w in STOPWORDS]))
    df_test['stop_word_count'] = df_test['text'].apply(
        lambda x: len([w for w in str(x).lower().split() if w in STOPWORDS]))

    # url_count
    df_train['url_count'] = df_train['text'].apply(
        lambda x: len([w for w in str(x).lower().split() if 'http' in w or 'https' in w]))
    df_test['url_count'] = df_test['text'].apply(
        lambda x: len([w for w in str(x).lower().split() if 'http' in w or 'https' in w]))

    # mean_word_length
    df_train['mean_word_length'] = df_train['text'].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
    df_test['mean_word_length'] = df_test['text'].apply(lambda x: np.mean([len(w) for w in str(x).split()]))

    # char_count
    df_train['char_count'] = df_train['text'].apply(lambda x: len(str(x)))
    df_test['char_count'] = df_test['text'].apply(lambda x: len(str(x)))

    # punctuation_count
    df_train['punctuation_count'] = df_train['text'].apply(
        lambda x: len([c for c in str(x) if c in string.punctuation]))
    df_test['punctuation_count'] = df_test['text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))

    # hashtag_count
    df_train['hashtag_count'] = df_train['text'].apply(lambda x: len([c for c in str(x) if c == '#']))
    df_test['hashtag_count'] = df_test['text'].apply(lambda x: len([c for c in str(x) if c == '#']))

    # mention_count
    df_train['mention_count'] = df_train['text'].apply(lambda x: len([c for c in str(x) if c == '@']))
    df_test['mention_count'] = df_test['text'].apply(lambda x: len([c for c in str(x) if c == '@']))

    return [df_train, df_test]
