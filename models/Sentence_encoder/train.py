import os

import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import train_test_split

from config import conn, PROJECT_PATH
from models.Sentence_encoder.clean import clean_text
from models.Sentence_encoder.build_model import create_model

train_df = pd.read_csv(os.path.join(PROJECT_PATH, "models/train.csv"))

train_df = clean_text(train_df)

X_train, X_test, y_train, y_test = train_test_split(
    train_df['text'], train_df['target'], test_size=0.3, random_state=42)

model = create_model()

checkpoint = ModelCheckpoint(
    'weights.best.hdf5', monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001)

history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=15,
                    callbacks=[checkpoint, reduce_lr], batch_size=16)

scores = model.evaluate(X_test, y_test, verbose=0)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
