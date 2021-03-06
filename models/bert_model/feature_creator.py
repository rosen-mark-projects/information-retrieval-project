import gc
import re
import string
import operator
from collections import defaultdict
from wordcloud import STOPWORDS

import numpy as np

def create_features(train_data):
    train_data['words'] = train_data['text'].apply(lambda text: len(str(text).split()))

    train_data['unique_words'] = train_data['text'].apply(lambda text: len(set(str(text).split())))

    train_data['stop_words'] = train_data['text'].apply(
        lambda text: len([word for word in str(text).lower().split() if word in STOPWORDS]))

    train_data['urls'] = train_data['text'].apply(
        lambda text: len([word for word in str(text).lower().split() if 'http' in word or 'https' in word]))

    train_data['mean_word_length'] = train_data['text'].apply(
        lambda text: np.mean([len(word) for word in str(text).split()]))

    train_data['hashtags'] = train_data['text'].apply(lambda text: len([char for char in str(text) if char == '#']))

    train_data['mentionings'] = train_data['text'].apply(lambda text: len([char for char in str(text) if char == '@']))

    return train_data
