from dbManipulation import (read_rawData, insert_clean_drop)
from utils.methods import KNNCleaner, arrayKNN
import numpy as np

def sweep():
    raw_data = read_rawData()
    drop_clean = []
    for data in raw_data:
        if '?' not in data:
            drop_clean.append(data)
    return insert_clean_drop(np.array(drop_clean))

def decoration():
    raw_data = read_rawData()
    drop_clean = []
    dirty_data = []
    for data in raw_data:
        if '?' not in data:
            drop_clean.append(data)
        else:
            dirty_data.append(data)
    drop_clean = np.array(drop_clean)
    mean_vals = np.mean(drop_clean, axis = 0)
    for data in dirty_data:
        dirty_idx = []
        for i in range(len(data)):
            if data[i] == '?':
                dirty_idx.append(i)
                data[i] = mean_vals[i]
        for i in dirty_idx:
            X = np.concatenate((drop_clean[:, :i], drop_clean[:, i+1:]), axis=1)
            y = drop_clean[:,i:i+1].reshape(1,-1)[0]
            test = np.array(data[:i] + data[i+1:]).reshape(1, -1)
            data[i] = arrayKNN(X, y, test)[0]
        drop_clean = np.concatenate((drop_clean, np.array(data).reshape(1, -1)), axis=0)
    return insert_clean_drop(drop_clean,  method = 'knn')