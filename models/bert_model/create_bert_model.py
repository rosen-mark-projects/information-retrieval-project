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
from models.bert_model import tokenization

def load_bert():
    # module_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"
    module_url = os.path.join(PROJECT_PATH, 'models/bert_model/bert')
    bert_layer = hub.KerasLayer(module_url, trainable=False, name='USE_embedding')

    vocabulary = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    lowercase = bert_layer.resolved_object.do_lower_case.numpy()
    full_tokenizer = tokenization.FullTokenizer(vocabulary, lowercase)

    return (bert_layer, full_tokenizer)

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

