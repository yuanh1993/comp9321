from model.stack import StackClassification
import dbManipulation
import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import learning_curve

def training_model(method = 'drop'):
    db = dbManipulation.get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                cls = line[key]
                if cls > 0:
                    cls = 1
                target.append(cls)
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

def learningCurve(method='drop'):
    db = dbManipulation.get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                cls = line[key]
                if cls > 0:
                    cls = 1
                target.append(cls)
            else:
                line_list.append(line[key])
        db_list.append(line_list)
    X = np.array(db_list)
    y = np.array(target)
    print("Start training...")
    train_sizes, train_scores, valid_scores = learning_curve(
                                                             StackClassification(),
                                                             X,
                                                             y,
                                                             train_sizes = [20, 40, 60, 80, 100,
                                                                            120, 140, 160, 180, 200,
                                                                            220, 240, 260],
                                                             cv = 10,
                                                             scoring='roc_auc')
    print("finish training")
    return train_sizes, np.mean(train_scores, axis = 1), np.mean(valid_scores, axis = 1)