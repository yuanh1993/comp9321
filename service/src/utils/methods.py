import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def Logistic(data, target):
    try:
        n, m = data.shape
    except:
        m = data.shape[0]
        n = -1
    data = data.reshape(m, n)
    clf = LogisticRegression(solver='liblinear')
    scores = cross_val_score(clf, data, target, cv=10, n_jobs=-1)
    return np.mean(scores)

def DecisionTree(data, target):
    clf = DecisionTreeClassifier(criterion="entropy")
    scores = cross_val_score(clf, data, target, cv=10, n_jobs=-1)
    return np.mean(scores)

def KNNCleaner(data, target, test):
    clf = KNeighborsClassifier(weights='distance' ,n_neighbors=3)
    X = pd.DataFrame(data)
    y = np.array(target)
    clf.fit(X, y)
    return clf.predict(np.array(test))

def arrayKNN(X, y, test):
    clf = KNeighborsClassifier(weights='distance', n_neighbors=3)
    clf.fit(X, y)
    return clf.predict(test)