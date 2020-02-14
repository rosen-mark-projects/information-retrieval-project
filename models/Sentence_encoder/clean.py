import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem.porter import *
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')


def clean_text(train):
    def clean(text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)

        stp = set(stopwords.words("english"))
        st = WordNetLemmatizer()
        stemmer = PorterStemmer()
        text = text.split()
        text = [w for w in text if not w in stp]
        text = [st.lemmatize(w) for w in text]
        text = [stemmer.stem(word) for word in text if len(word) > 3]
        text = " ".join(text)

        text = text.translate(str.maketrans("", "", string.punctuation))
        return text

    train['text'] = train['text'].apply(lambda x: clean(x))
    return train
