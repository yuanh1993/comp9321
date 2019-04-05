import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

def entropy(data):
    base = np.log(data.shape[0])
    prob = data/(np.sum(data))
    log_prob = []
    for p in prob:
        if p != 0.0:
            log_prob.append(np.log(p))
        else:
            log_prob.append(0.0)
    print(log_prob)
    log_prob = np.array(log_prob)
    H_x = prob * (log_prob/base)
    return -np.sum(H_x)

def Logistic(data, target):
    n, m = data.shape
    data = target.reshape(m, n)
    clf = LogisticRegression(solver='liblinear')
    scores = cross_val_score(clf, data, target, cv=10)
    return np.mean(scores)

def DecisionTree(data, target):
    clf = DecisionTreeClassifier(criterion="entropy")
    scores = cross_val_score(clf, data, target, cv=10)
    return np.mean(scores)
