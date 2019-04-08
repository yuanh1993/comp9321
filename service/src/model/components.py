from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

def DecisionTreeLayer():
    return DecisionTreeClassifier()


def BoostingLayer():
    return GradientBoostingClassifier(n_estimators=300)


def SVMLayer():
    return SVC(kernel='linear', gamma='auto')

print(np.array([1,2]).shape)