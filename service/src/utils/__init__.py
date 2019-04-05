from methods import Logistic, DecisionTree
import numpy as np
import pandas as pd


discrete_data = [

]

continuous_data = [

]


# def discrete_analysis(data, target, data_type):
#     is_dicrete = data_type in discrete_data
#     if is_dicrete:
#         positive_data = {}
#         for i in range(len(data)):
#             if target[i] != 0:
#                 try:
#                     positive_data[data[i]] += 1
#                 except:
#                     positive_data[data[i]] = 1
#         data_distribution = []
#         for key in positive_data:
#             data_distribution.append(positive_data[key])
#         np_data = np.array(data_distribution)
#         score =  entropy(np_data)
#         return score
#     else:
#         return -1

def discrete_analysis(data, target, data_type, interpreter = {}):
    is_dicrete = data_type in discrete_data
    if is_dicrete:
        one_hot_raw ={}
        for key in interpreter:
            one_hot_raw[key] = []
        for x in data:
            for key in one_hot_raw:
                if key == x:
                    one_hot_raw[key].append(1)
                else:
                    one_hot_raw[key].append(0)
        y = np.array(target)
        X = pd.DataFrame(map)
        return DecisionTree(X, y)
    else:
        return -1

def continous_analysis(data, target, data_type):
    is_continous = data_type in continuous_data
    if not is_continous:
        return -1
    X = np.array(data)
    y = np.array(target)
    return Logistic(X, y)
