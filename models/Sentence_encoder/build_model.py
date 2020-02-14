import os
import tensorflow as tf
import tensorflow_hub as hub
from keras import regularizers
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Input, BatchNormalization
from tensorflow.keras.models import Model, Sequential

from config import PROJECT_PATH

def create_model():
    module_url = os.path.join(PROJECT_PATH, 'models/Sentence_encoder/embedded')
    embedded = hub.KerasLayer(module_url, trainable=False, name='USE_embedding')

    def build_model(embed):
        model = Sequential()
        model.add(Input(shape=[], dtype=tf.string))
        model.add(embed)
        model.add(Dense(256, activation='relu',
                        kernel_regularizer=regularizers.l2(0.01)))
        model.add(BatchNormalization())
        model.add(Dense(128, activation='relu',
                        kernel_regularizer=regularizers.l2(0.03)))
        model.add(BatchNormalization())
        model.add(Dense(32, activation='relu',
                        kernel_regularizer=regularizers.l2(0.05)))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(Adam(lr=0.001), loss='binary_crossentropy',
                    metrics=['accuracy'])

        return model


    model = build_model(embedded)
    return model
