# https://machinelearningcoban.com/2017/08/08/nbc/
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from pathlib import Path
import numpy as np
from data import data_proc
import sys
import os


class Classifier:
    def __init__(self, model_path='nb_model.pkl'):
        cwd = os.getcwd()
        self.model_path = os.path.join(
            cwd, 'post_classification/dataset', model_path)
        model_file = Path(self.model_path)

        if model_file.is_file():
            self.model = joblib.load(self.model_path)
        else:
            self.model = BernoulliNB()
        self.dat = data_proc()

    def train(self):
        dat = self.dat
        train_data, train_label, test_data, test_label = dat.get_train_data(
            num_samples=18000)

        # training
        self.model.fit(train_data, train_label)
        joblib.dump(self.model, self.model_path)

        pred = self.model.predict(test_data)
        # self.model.predict_proba(test_data)
        print('Accuracy: {}'.format(accuracy_score(test_label, pred)))

    def classify(self, texts):
        dat = self.dat
        vecs = dat.texts_to_vecs(texts)
        return self.model.predict(vecs)

    def classify_proba(self, texts):
        dat = self.dat
        vecs = dat.texts_to_vecs(texts)
        res = self.model.predict_proba(vecs)
        res = [[round(100 * a / (a + b)), round(100 * b / (a + b))]
               for [a, b] in res]
        return res


if __name__ == '__main__':
    clf = Classifier()
    clf.train()
