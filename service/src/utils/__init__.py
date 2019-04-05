from methods import entropy
import numpy as np


discrete_data = [

]

continuous_data = [

]


def discrete_analysis(data, target, data_type):
    is_dicrete = data_type in discrete_data
    if is_dicrete:
        positive_data = {}
        for i in range(len(data)):
            if target[i] != 0:
                try:
                    positive_data[data[i]] += 1
                except:
                    positive_data[data[i]] = 1
        data_distribution = []
        for key in positive_data:
            data_distribution.append(positive_data[key])
        np_data = np.array(data_distribution)
        score =  entropy(np_data)
        return score
    else:
        return -1

