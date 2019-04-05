import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

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


def logistic_train(data, target):
    clf = LogisticRegression(random_state=0, solver='lbfgs',
                             multi_class='multinomial').fit(data, target)
    return clf

def pred(clf, data):
    return clf.predict(data)

X = [1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1, 1]
y = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
X = np.array(X).reshape(26, 1)
y = np.array(y)

clf = LogisticRegression(random_state=0, solver='lbfgs',
                             multi_class='multinomial')
scores = cross_val_score(clf, X, y, cv=6)
print(scores)
# test = np.array([3, 4, 5, 12, 23, 111]).reshape(6, 1)
# print(pred(clf, test))