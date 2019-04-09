from model.stack import StackClassification
import dbManipulation
import numpy as np
from sklearn.externals import joblib
from sklearn.preprocessing import normalize
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LogisticRegression

def training_model(method = 'drop', model_type = 'stack'):
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
        db_list.append(line_list)
    X = np.array(db_list)
    X = normalize(X, axis=0, norm='max')
    y = np.array(target)
    if model_type == 'stack':
        clf = StackClassification()
    else:
        clf = LogisticRegression(C=0.01,penalty = 'l2')
    clf.fit(X, y)
    return clf

def saveModel(method = 'drop', model_type = 'stack'):
    if model_type == 'stack':
        filename = 'model.sav'
    else:
        filename = 'model_logit.sav'
    clf = training_model(method)
    joblib.dump(clf, filename)

def readModel(model_type = 'stack'):
    if model_type == 'stack':
        filename = 'model.sav'
    else:
        filename = 'model_logit.sav'
    clf = joblib.load(filename)
    return clf

def learningCurve(method='drop', model_type = 'stack'):
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
        db_list.append(line_list)
    X = np.array(db_list)
    X = normalize(X, axis=0, norm='max')
    y = np.array(target)
    print("Start training...")
    if model_type == 'stack':
        clf = StackClassification()
    else:
        clf = LogisticRegression(C=0.01,penalty = 'l2')
    train_sizes, train_scores, valid_scores = learning_curve(
                                                             clf,
                                                             X,
                                                             y,
                                                             train_sizes = [20, 40, 60, 80, 100,
                                                                            120, 140, 160, 180, 200,
                                                                            220, 240, 260],
                                                             cv = 10,
                                                             scoring='accuracy')
    print("finish training")
    return train_sizes, np.mean(train_scores, axis = 1), np.mean(valid_scores, axis = 1)