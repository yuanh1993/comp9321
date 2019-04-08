from .components import DecisionTreeLayer, BoostingLayer, SVMLayer
from sklearn.linear_model import LogisticRegression
import numpy as np

class StackClassification:
    def __init__(self, train_ratio = 0.8):
        self.DecisionTree = DecisionTreeLayer()
        self.SVM = SVMLayer()
        self.NN = BoostingLayer()
        self.clf = LogisticRegression(solver='lbfgs',multi_class='multinomial')
        self.train_ratio = train_ratio

    def fit(self, X, y):
        n_sample = X.shape[0]
        n_stack = int(self.train_ratio * n_sample)
        X_test = X[n_stack:, :]
        y_true = y[n_stack:]
        X_train = X[:n_stack, :]
        y_train = y[:n_stack]
        y_tree = self.DecisionTree.fit(X_train, y_train).predict(X_test).reshape(-1,1)
        y_b = self.NN.fit(X_train, y_train).predict(X_test).reshape(-1,1)
        y_svm = self.SVM.fit(X_train, y_train).predict(X_test).reshape(-1,1)
        X_stacked = np.concatenate((y_tree, y_b, y_svm), axis=1)
        self.clf.fit(X_stacked, y_true)


    def predict(self, test):
        y_tree = self.DecisionTree.predict(test).reshape(-1, 1)
        y_nn = self.NN.predict(test).reshape(-1, 1)
        y_svm = self.SVM.predict(test).reshape(-1, 1)
        X_stacked = np.concatenate((y_tree, y_nn, y_svm), axis=1)
        return self.clf.predict(X_stacked)

    def predict_proba(self, test):
        y_tree = self.DecisionTree.predict(test).reshape(-1, 1)
        y_b = self.NN.predict(test).reshape(-1, 1)
        y_svm = self.SVM.predict(test).reshape(-1, 1)
        X_stacked = np.concatenate((y_tree, y_b, y_svm), axis=1)
        return self.clf.predict_proba(X_stacked)

    def get_params(self, deep=False):
        return {'train_ratio': self.train_ratio}
