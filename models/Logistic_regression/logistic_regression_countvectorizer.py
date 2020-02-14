import os
import pickle

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from config import conn, PROJECT_PATH

print(conn)
train_df = pd.read_csv(os.path.join(PROJECT_PATH, "models/train.csv"))

vectorizer = CountVectorizer()
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(train_df['text'].values[:11])
print(vectorizer.get_feature_names())
print(len(vectorizer.get_feature_names()))

vectorizer.get_stop_words

X = vectorizer.fit_transform(train_df['text'].values)
X_test = vectorizer.transform(test_df['text'].values)

X_train, X_test, y_train, y_test = train_test_split(
    X, train_df['target'], test_size=0.33, random_state=42)
clf = LogisticRegression().fit(X_train, y_train)

print(clf.score(X_train, y_train))
print(clf.score(X_test, y_test))

scores = cross_val_score(clf, X_train, y_train, cv=5)
print(scores)

lasso = Lasso(0.001).fit(X_train, y_train)
print(cross_val_score(lasso, X_train, y_train, cv=3))

with open(os.path.join(PROJECT_PATH, "models/simple_LR_model.pkl"), 'wb') as file:
    pickle.dump(clf, file)

with open(os.path.join(PROJECT_PATH, 'models/simple_LR_model.pkl'), 'rb') as file:
    clf = pickle.load(file)


keyword = 'earthquake'
cur = conn.cursor()
cur.execute(
    "SELECT text, keyword, url FROM disaster_tweets WHERE keyword='{}'".format(keyword))
data = cur.fetchall()

tweets = [tweet[0] for tweet in data]
X_test = vectorizer.transform(tweets)

print(clf.predict(X_test))

print(tweets[0])
print(tweets[1])
