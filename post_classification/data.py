from keras.preprocessing.text import Tokenizer
from pathlib import Path
import numpy as np
import pandas as pd
import os
import pickle
import csv


class data_proc:

    def __init__(self, pos_samples_file='pos_samples.csv', neg_samples_file='neg_samples.csv', saved_tokenizer='token.pkl'):
        cwd = os.getcwd()
        self.pos_samples = None
        self.pos_samples_file = os.path.join(
            cwd, 'post_classification/dataset', pos_samples_file)
        self.neg_samples_file = os.path.join(
            cwd, 'post_classification/dataset', neg_samples_file)
        self.saved_tokenizer = os.path.join(
            cwd, 'post_classification/dataset', saved_tokenizer)

        token_file = Path(self.saved_tokenizer)
        if token_file.is_file():
            # read token file
            with open(self.saved_tokenizer, 'rb') as input:
                self.t = pickle.load(input)
                # self.read_data()
        else:
            self.read_data()
            self.t = Tokenizer()
            samples, labels = self.get_plain_data()
            self.t.fit_on_texts(samples)
            with open(self.saved_tokenizer, 'wb') as output:
                pickle.dump(self.t, output, pickle.HIGHEST_PROTOCOL)

    def read_data(self):
        df = pd.read_csv(self.pos_samples_file, sep=',')
        pos = np.array(df.values)
        # print(pos.shape)

        df = pd.read_csv(self.neg_samples_file, sep=',')
        neg = np.array(df.values)
        # print(neg[1, :])

        self.pos_samples = pos[:, 1:3]
        self.neg_samples = neg[:, 1:3]

        # self.pos_samples = np.array(['{} | {}'.format(
        #     a, b) for a, b in zip(self.pos_samples[:, 0], self.pos_samples[:, 1])])

        # self.neg_samples = np.array(['{} | {}'.format(
        #     a, b) for a, b in zip(self.neg_samples[:, 0], self.neg_samples[:, 1])])

        self.pos_samples = np.array([a for a in self.pos_samples[:, 0]])

        self.neg_samples = np.array([a for a in self.neg_samples[:, 0]])

        # print(self.pos_samples[0:4])

    def get_plain_data(self):
        if self.pos_samples is None:
            self.read_data()

        all_samples = np.concatenate(
            (self.pos_samples, self.neg_samples), axis=0)
        labels = np.concatenate(
            (np.zeros(self.pos_samples.shape[0], dtype=int), np.full(self.neg_samples.shape[0], 1, dtype=int)), axis=0)
        return all_samples, labels

    def get_train_data(self, num_samples=8000):
        if self.pos_samples is None:
            self.read_data()

        balance = num_samples // 2
        pos_count = len(self.pos_samples)
        neg_count = len(self.neg_samples)

        num_pos = balance if balance < pos_count else pos_count
        num_neg = balance if balance < neg_count else neg_count

        plain_texts, labels = self.get_plain_data()
        encoded_docs = self.t.texts_to_matrix(plain_texts, mode='count')

        pos_sampls = encoded_docs[0:pos_count, :]
        neg_sampls = encoded_docs[pos_count:, :]

        res_pos = pos_sampls[np.random.choice(
            pos_sampls.shape[0], num_pos, replace=False)]
        res_neg = neg_sampls[np.random.choice(
            neg_sampls.shape[0], num_neg, replace=False)]

        res = np.concatenate((res_pos, res_neg), axis=0)
        res_labels = np.concatenate(
            (np.zeros(res_pos.shape[0], dtype=int), np.full(res_neg.shape[0], 1, dtype=int)), axis=0)

        s = np.arange(res_labels.shape[0])
        np.random.shuffle(s)
        np.random.shuffle(s)

        res = res[s]
        res_labels = res_labels[s]

        num_train = ((num_pos + num_neg) * 2) // 3
        num_test = num_pos + num_neg - num_train

        train_data = res[0: num_train, :]
        train_labels = res_labels[0: num_train]

        test_data = res[num_train:, :]
        test_labels = res_labels[num_train:]

        return train_data, train_labels, test_data, test_labels

    def texts_to_vecs(self, texts):
        return self.t.texts_to_matrix(texts)


if __name__ == '__main__':
    dat = data_proc()
    train_data, train_labels, _, _ = dat.get_train_data(num_samples=10)
    print(train_data)
    print(train_labels)
    # samples, labels = dat.plain_data()
    # print(samples.shape)
    # print(labels.shape)
