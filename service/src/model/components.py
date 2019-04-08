from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier

def DecisionTreeLayer():
    return DecisionTreeClassifier()


def BoostingLayer():
    return GradientBoostingClassifier(n_estimators=300)


def SVMLayer():
    return SVC(kernel='linear', gamma='auto')
