from model.stack import StackClassification
from dbManipulation import get_cleaned_data_from_DB
import numpy as np
from sklearn.externals import joblib

def training_model(method = 'drop'):
    db = get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                target.append(line[key])
            else:
                line_list.append(line[key])
        db_list.append(line_list)
    X = np.array(db_list)
    y = np.array(target)
    clf = StackClassification()
    clf.fit(X, y)
    return clf

def saveModel(method = 'drop', filename = 'model.sav'):
    clf = training_model(method)
    joblib.dump(clf, filename)

def readModel(filename = 'model.sav'):
    clf = joblib.load(filename)
    return clf

data = np.array([[52.0,1.0,4.0,125.0,212.0,0.0,0.0,168.0,0.0,1.0,1.0,2.0,7.0],
                 [62.0,1.0,2.0,128.0,208.0,1.0,2.0,140.0,0.0,0.0,1.0,0.0,3.0]])
clf = readModel()
print(clf.predict(data))