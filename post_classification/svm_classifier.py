# https: // machinelearningcoban.com / 2017 / 08 / 08 / nbc/
from sklearn import svm
from sklearn.metrics import accuracy_score
import numpy as np
from data import data_proc
import sys
from pathlib import Path
from sklearn.externals import joblib
import os


class Classifier:
    def __init__(self, model_path='svm_model.pkl'):
        cwd = os.getcwd()
        self.model_path = os.path.join(
            cwd, 'post_classification/dataset', model_path)
        model_file = Path(self.model_path)

        if model_file.is_file():
            self.model = joblib.load(self.model_path)
        else:
            self.model = svm.SVC()
        self.dat = data_proc()

    def train(self):

        dat = self.dat
        train_data, train_label, test_data, test_label = dat.get_train_data(
            num_samples=4000)
        # training
        print('training...')
        self.model.fit(train_data, train_label)
        joblib.dump(self.model, self.model_path)
        print('training finished. predicting...')
        pred = self.model.predict(test_data)
        print('Accuracy: {}'.format(accuracy_score(test_label, pred)))

    def classify(self, texts):
        dat = self.dat
        vecs = dat.texts_to_vecs(texts)
        return self.model.predict(vecs)


if __name__ == '__main__':
    clf = Classifier()
    clf.train()
