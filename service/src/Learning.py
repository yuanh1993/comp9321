from model.stack import StackClassification
from dbManipulation import get_cleaned_data_from_DB
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
                if i < 290:
                    target.append(line[key])
                else:
                    y_test.append(line[key])
            else:
                line_list.append(line[key])
        if i < 290:
            db_list.append(line_list)
        else:
            test.append(line_list)
    X = np.array(db_list)
    y = np.array(target)
    clf = get_cleaned_data_from_DB()
    clf.fit(X, y)
    print(clf.predict(test))
    print(y_test)

stack_learning(method='knn')