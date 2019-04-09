from .methods import Logistic, DecisionTree, KNNCleaner
import numpy as np
import pandas as pd
import json


discrete_data = [
    2, 3, 6, 7, 9, 13, 14
]

continuous_data = [
    1, 4, 5, 8, 10, 11, 12
]

interpreter = {
    1: {}, 4: {}, 5: {}, 8: {}, 10: {}, 11: {}, 12:{},
    2: {1: 'male', 2: 'female'},
    3: {1: 'typical angin', 2: 'atypical angina', 3: 'non-anginal pain', 4: 'asymptomatic'},
    6: {0: False, 1: True},
    7: {0: 'normal', 1: 'having ST-T wave abnormality', 2: 'Estes'},
    9: {0: False, 1: True},
    13: {3: 'normal', 6: 'fixed defect', 7: 'reversable defect'},
    14: {0: False, 1: True}
}

def discrete_analysis(data, target, data_type):
    is_dicrete = data_type in discrete_data
    if is_dicrete:
        one_hot_raw ={}
        for key in interpreter[data_type]:
            one_hot_raw[float(key)] = []
        for x in data:
            for key in one_hot_raw:
                if key == x:
                    one_hot_raw[key].append(1)
                else:
                    one_hot_raw[key].append(0)
        for i in range(len(target)):
            if target[i] > 0:
                target[i] = 1
        y = np.array(target)
        X = pd.DataFrame(one_hot_raw)
        return DecisionTree(X, y)
    else:
        return -1

def continous_analysis(data, target, data_type):
    is_continous = data_type in continuous_data
    if not is_continous:
        return -1
    for i in range(len(target)):
        if target[i] > 0:
            target[i] = 1
    X = np.array(data)
    y = np.array(target)
    return Logistic(X, y)

def One_Hot_Line(data, target_col, features, means):
    line = []
    for i in range(1, len(features)):
        if i == target_col:
            continue
        if i in discrete_data:
            for key in interpreter[i]:
                if data[features[i]] == '?':
                    line.append(0)
                elif float(data[features[i]]) == key:
                    line.append(1)
                else:
                    line.append(0)
        else:
            if data[features[i]] == '?':
                key = 'avg(' + features[i] + ')'
                line.append(means[key])
            else:
                line.append(data[features[i]])
    return line

def One_Hot_All(raw_data, target_col, features, means):
    feature_toInt = {}
    for key in features:
        feature_toInt[features[key]] = key
    y = []
    test = []
    X = []
    for row in raw_data:
        if row[features[target_col]] == '?':
            test.append(One_Hot_Line(row, target_col, features, means))
        else:
            y.append(row[features[target_col]])
            X.append(One_Hot_Line(row, target_col, features, means))
    if len(test) == 0:
        return []
    return KNNCleaner(X, y, test)