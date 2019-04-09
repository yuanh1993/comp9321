from .components import DecisionTreeLayer, BoostingLayer, SVMLayer, LogisticLayer
import numpy as np

class StackClassification:
    def __init__(self, train_ratio = 0.5):
        self.DecisionTree = DecisionTreeLayer()
        self.SVM = SVMLayer()
        self.Boost = BoostingLayer()
        self.train_ratio = train_ratio

    def fit(self, X, y):
        n_sample = X.shape[0]
        n_stack = int(self.train_ratio * n_sample)
        X1 = X[n_stack:, :]
        y1 = y[n_stack:]
        X2 = X[:n_stack, :]
        y2 = y[:n_stack]
        self.clf1 = self._fit(X1, y1, X2, y2)
        self.clf2 = self._fit(X2, y2, X1, y1)
        self.SVM.fit(X, y)
        self.Boost.fit(X, y)
        self.DecisionTree.fit(X, y)

    def _fit(self, X, y, test, ans):
        y_tree = self.DecisionTree.fit(X, y).predict(test).reshape(-1, 1)
        y_b = self.Boost.fit(X, y).predict(test).reshape(-1, 1)
        y_svm = self.SVM.fit(X, y).predict(test).reshape(-1, 1)
        X_stacked = np.concatenate((y_tree, y_b, y_svm), axis=1)
        clf = LogisticLayer()
        clf.fit(X_stacked, ans)
        return clf

    def predict(self, test):
        y_tree = self.DecisionTree.predict(test).reshape(-1, 1)
        y_Boost = self.Boost.predict(test).reshape(-1, 1)
        y_svm = self.SVM.predict(test).reshape(-1, 1)
        X_stacked = np.concatenate((y_tree, y_Boost, y_svm), axis=1)
        prob1 = self.clf1.predict_proba(X_stacked)
        prob2 = self.clf2.predict_proba(X_stacked)
        probs = prob1 + prob2
        clsfy = []
        for p in probs:
            if p[0] >= p[1]:
                clsfy.append(0)
            else:
                clsfy.append(1)
        return np.array(clsfy)

    def predict_proba(self, test):
        y_tree = self.DecisionTree.predict(test).reshape(-1, 1)
        y_Boost = self.Boost.predict(test).reshape(-1, 1)
        y_svm = self.SVM.predict(test).reshape(-1, 1)
        X_stacked = np.concatenate((y_tree, y_Boost, y_svm), axis=1)
        prob1 = self.clf1.predict_proba(X_stacked)
        prob2 = self.clf2.predict_proba(X_stacked)
        probs = prob1 + prob2
        return probs/2

    def get_params(self, deep=False):
        return {'train_ratio': self.train_ratio}
