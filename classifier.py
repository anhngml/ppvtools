# https: // machinelearningcoban.com / 2017 / 08 / 08 / nbc/
from sklearn.naive_bayes import BernoulliNB
import numpy as np
from data import data_proc
import sys


class Classifier:
    def __init__(self):
        self.model = BernoulliNB()

    def train(self):

        # train data
        d1 = [1, 1, 1, 0, 0, 0, 0, 0, 0]
        d2 = [1, 1, 0, 1, 1, 0, 0, 0, 0]
        d3 = [0, 1, 0, 0, 1, 1, 0, 0, 0]
        d4 = [0, 1, 0, 0, 0, 0, 1, 1, 1]

        # test data
        d5 = np.array([[1, 0, 0, 1, 0, 0, 0, 1, 0]])
        d6 = np.array([[0, 1, 0, 0, 0, 0, 0, 1, 1]])

        train_data = np.array([d1, d2, d3, d4])
        label = np.array(['B', 'B', 'B', 'N'])  # 0 - B, 1 - N

        self.model.fit(train_data, label)

        # test
        print('Predicting class of d5:', str(self.model.predict(d5)))
        print('Probability of d6 in each class:', self.model.predict_proba(d6))

        sys.exit()
        # ==========================================================

        dat = data_proc('', '')
        train_data, train_label = dat.get_train_data()
        test_data, test_label = dat.get_test_data()

        # training
        self.model.fit(train_data, train_label)

        self.model.predict(test_data)
        self.model.predict_proba(test_data)

        # ==========================================================

    def classify(self):
        pass


if __name__ == '__main__':
    clf = Classifier()
    clf.train()
