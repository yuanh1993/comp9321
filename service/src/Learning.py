from model.stack import StackClassification
from dbManipulation import get_cleaned_data_from_DB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np

def stack_learning(method = 'drop'):
    db = get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    test = []
    y_test = []
    i = 0
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                if i < 270:
                    target.append(line[key])
                else:
                    y_test.append(line[key])
            else:
                line_list.append(line[key])
        if i < 270:
            db_list.append(line_list)
        else:
            test.append(line_list)
        i += 1
    X = np.array(db_list)
    y = np.array(target)
    test = np.array(test)
    clf = StackClassification()
    clf.fit(X, y)
    print(clf.predict(test))
    for n in y_test:
        print(n, end=' ')


def DecisionTreeLayer(method = 'drop'):
    db = get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    test = []
    y_test = []
    i = 0
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                if i < 270:
                    target.append(line[key])
                else:
                    y_test.append(line[key])
            else:
                line_list.append(line[key])
        if i < 270:
            db_list.append(line_list)
        else:
            test.append(line_list)
        i += 1
    X = np.array(db_list)
    y = np.array(target)
    test = np.array(test)
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    print(clf.predict(test))
    for n in y_test:
        print(n, end=' ')


def RandomForest(method = 'drop'):
    db = get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    test = []
    y_test = []
    i = 0
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                if i < 270:
                    target.append(line[key])
                else:
                    y_test.append(line[key])
            else:
                line_list.append(line[key])
        if i < 270:
            db_list.append(line_list)
        else:
            test.append(line_list)
        i += 1
    X = np.array(db_list)
    y = np.array(target)
    test = np.array(test)
    clf = GradientBoostingClassifier(n_estimators=300)
    clf.fit(X, y)
    print(clf.predict(test))
    for n in y_test:
        print(n, end=' ')

def SVMLayer(method = 'drop'):
    db = get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    test = []
    y_test = []
    i = 0
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                if i < 270:
                    target.append(line[key])
                else:
                    y_test.append(line[key])
            else:
                line_list.append(line[key])
        if i < 270:
            db_list.append(line_list)
        else:
            test.append(line_list)
        i += 1
    X = np.array(db_list)
    y = np.array(target)
    test = np.array(test)
    clf = SVC(kernel='linear', gamma='auto')
    clf.fit(X, y)
    print(clf.predict(test))
    for n in y_test:
        print(n, end=' ')

# stack_learning(method='knn')
stack_learning(method='drop')