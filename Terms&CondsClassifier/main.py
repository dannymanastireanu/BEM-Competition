import csv
import os
import random

import numpy as np
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
from tensorflow.python.keras.callbacks import ModelCheckpoint

from utils import testing


def info():
    print("Version: ", tf.__version__)
    print("Eager mode: ", tf.executing_eagerly())
    print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")


def get_dataset():
    raw_train_pos = testing.read_data("/home/danny/PycharmProjects/Terms&CondsClassifier/dataset/train/pos/")
    raw_train_neg = testing.read_data("/home/danny/PycharmProjects/Terms&CondsClassifier/dataset/train/neg/")

    positive_labels = np.ones(len(raw_train_neg), np.int)
    negative_labels = np.zeros(len(raw_train_neg), np.int)

    result_label = np.concatenate((positive_labels, negative_labels))

    train_data = np.concatenate((np.asarray(raw_train_pos), np.asarray(raw_train_neg)))

    raw_test_pos = testing.read_data("/home/danny/PycharmProjects/Terms&CondsClassifier/dataset/test/pos/")
    raw_test_neg = testing.read_data("/home/danny/PycharmProjects/Terms&CondsClassifier/dataset/test/neg/")

    test_data = np.concatenate((np.asarray(raw_test_pos), np.asarray(raw_test_neg)))

    # train_dataset = tf.data.Dataset.from_tensor_slices((np.array(raw_train_pos), np.zeros(len(raw_train_pos))))
    train_dataset = tf.data.Dataset.from_tensor_slices((train_data, result_label))
    test_dataset = tf.data.Dataset.from_tensor_slices((test_data, result_label))
    return train_dataset, test_dataset


def create_model(train_dataset, test_dataset):
    # hubies_model = "https://hub.tensorflow.google.cn/google/tf2-preview/gnews-swivel-20dim/1"
    hubies_model = "https://hub.tensorflow.google.cn/google/tf2-preview/nnlm-en-dim128/1"

    hub_layer = hub.KerasLayer(hubies_model, output_shape=[128], input_shape=[],
                               dtype=tf.string, trainable=True)

    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    print(model.summary())

    # inferred from the name of the monitored quantity.
    checkpoint = ModelCheckpoint('./history_model/model-{epoch:03d}.h5',
                                 monitor='val_loss',
                                 verbose=0,
                                 save_best_only=True,
                                 mode='auto')


    model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

    history = model.fit(train_dataset.batch(1024), epochs=200, validation_data=test_dataset.batch(1024), callbacks=[checkpoint],
                        verbose=1)

    return model, history


def get_array_from_file(filename):
    array = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            array.append(row[0])

    return array


def split_data(data):
    index = 0
    stop_index = len(data)

    train = []
    test = []

    for i in range(0, int(0.7 * stop_index)):
        train.append(data[i])
    for i in range(int(0.7 * stop_index), stop_index):
        test.append(data[i])

    return train, test


def create_data_for_xy(data_p, data_n):
    x = []
    y = []

    dicto = []

    for d in data_p:
        dicto.append({'val': d.replace('\'', '').replace('\"', ''), 'n': 1})

    for d in data_n:
        dicto.append({'val': d.replace('\'', '').replace('\"', ''), 'n': 0})

    random.shuffle(dicto)

    for d in dicto:
        x.append(d['val'])
        y.append(d['n'])

    return tf.data.Dataset.from_tensor_slices((np.array(x), np.array(y)))



def get_tf_datasets():
    array_good = get_array_from_file("./tc_datasets/good.csv")
    array_bad = get_array_from_file("./tc_datasets/bad.csv")

    random.shuffle(array_bad)
    random.shuffle(array_good)

    train_good, test_good = split_data(array_good)
    train_bad, test_bad = split_data(array_bad)

    train_dataset = create_data_for_xy(train_good, train_bad)
    test_dataset = create_data_for_xy(test_good, test_bad)


    return train_dataset, test_dataset


def train_model():

    train_dataset, test_dataset = get_tf_datasets()

    # TRAIN THE MODEL

    model, history = create_model(train_dataset, test_dataset)

    results = model.evaluate(test_dataset.batch(20), verbose=2)

    for name, value in zip(model.metrics_names, results):
        print("%s: %.3f" % (name, value))


def load_model(filename):
    hubies_model = "https://hub.tensorflow.google.cn/google/tf2-preview/nnlm-en-dim128/1"
    hub_layer = hub.KerasLayer(hubies_model, output_shape=[128], input_shape=[],
                               dtype=tf.string, trainable=True)

    model = tf.keras.models.load_model(filename, custom_objects={'KerasLayer': hub_layer})

    return model

if __name__ == '__main__':
    info()

    # TRAIN MODEL
    train_model()

    # LOAD MODEL
    # model = load_model("./history_model/model-020.h5")

    print("Done")
