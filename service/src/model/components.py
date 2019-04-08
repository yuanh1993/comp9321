from sklearn.tree import DecisionTreeClassifier
import numpy as np


def Faker():
    li_x = [
        [1, 2, 3],
        [4, 5, 6]
    ]
    li_y = [1, 0]
    li_test = [4, 4, 5]
    X = np.array(li_x)
    y = np.array(li_y)
    test = np.array(li_test)
    return X, y, test


def DecisionTreeLayer(X, y, test):
    clf = DecisionTreeClassifier()
