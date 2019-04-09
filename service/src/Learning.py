from model.stack import StackClassification
from dbManipulation import get_cleaned_data_from_DB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import normalize
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np

def test_learning(method = 'drop'):
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
                cls = line[key]
                if cls > 0:
                    cls = 1
                if i < 270:
                    target.append(cls)
                else:
                    y_test.append(cls)
            elif key == 'thal':
                if line[key] == 3:
                    line_list += [1.0, 0.0, 0.0]
                elif line[key] == 6:
                    line_list += [0.0, 1.0, 0.0]
                else:
                    line_list += [0.0, 0.0, 1.0]
            elif key == 'pain_type':
                pain_type = [0.0, 0.0, 0.0, 0.0]
                pain_type[int(line[key]) - 1] = 1.0
                line_list += pain_type
            elif key == 'electrocardiographic':
                el = [0.0, 0.0, 0.0, 0.0]
                el[int(line[key])] = 1.0
                line_list += el
            else:
                line_list.append(line[key])
        if i < 270:
            db_list.append(line_list)
        else:
            test.append(line_list)
        i += 1
    X = np.array(db_list)
    # X = X / X.max(axis=0)
    X = normalize(X, axis=0, norm='max')
    y = np.array(target)
    test = np.array(test)
    # test = test / test.max(axis=0)
    test = normalize(test, axis=0, norm='max')
    clf = StackClassification()
    print(X.shape, y.shape)
    clf.fit(X, y)
    print(clf.predict(test))
    for n in y_test:
        print(n, end=' ')

if __name__ == '__main__':
    test_learning(method='drop')