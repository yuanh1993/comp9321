from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

def DecisionTreeLayer():
    return DecisionTreeClassifier()


def BoostingLayer():
    return GradientBoostingClassifier(n_estimators=500)


def SVMLayer():
    return SVC(kernel='linear', gamma='auto')

def LogisticLayer():
    return LogisticRegression(C=0.01,penalty = 'l2')