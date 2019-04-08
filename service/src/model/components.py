from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import numpy as np


def Faker():
    li_x = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    li_y = [1, 0]
    li_test = [[4, 4, 5]]
    X = np.array(li_x)
    y = np.array(li_y)
    test = np.array(li_test).reshape(-1, 3)
    return X, y, test


def DecisionTreeLayer(X, y, test):
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    return clf.predict(test)

def NeuralNetworkLayer(X, y, test):
    clf = MLPClassifier(solver='adam', alpha=1e-5,
                        hidden_layer_sizes = (8,), max_iter= 10000)
    clf.fit(X, y)
    return clf.predict(test)

def SVMLayer(X, y, test):
    clf = SVC(kernel='rbf', gamma='auto')
    clf.fit(X, y)
    return clf.predict(test)

X, y, test = Faker()
result = NeuralNetworkLayer(X, y, test)
print(result)
