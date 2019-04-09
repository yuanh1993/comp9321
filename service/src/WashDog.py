from dbManipulation import (read_rawData, insert_clean_drop, get_cleaned_data_from_DB, feature_map)
from utils.methods import KNNCleaner, arrayKNN
import numpy as np
from sklearn.preprocessing import normalize

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

def cleanInput(inputX):
    cleanData = get_cleaned_data_from_DB(method = 'drop')
    cleaned_List = []
    for data in cleanData:
        line_list = []
        for key in data:
            if key == 'target' or key == 'id':
                continue
            else:
                line_list.append(data[key])
        cleaned_List.append(line_list)
    cleaned_List = np.array(cleaned_List)
    mean_vals = np.mean(cleaned_List, axis=0)
    key_map = feature_map()
    input_list = []
    for i in range(1, 14):
        if inputX[key_map[i]] != '?':
            il = float(inputX[key_map[i]])
        input_list.append(il)
    missing_index = []
    for i in range(len(input_list)):
        if input_list[i] == '?':
            input_list[i] = mean_vals[i]
            missing_index.append(i)
    for i in missing_index:
        X = np.concatenate((cleaned_List[:, :i], cleaned_List[:, i + 1:]), axis=1)
        y = cleaned_List[:, i:i + 1].reshape(1, -1)[0]
        test = np.array(input_list[:i] + input_list[i + 1:]).reshape(1, -1)
        input_list[i] = arrayKNN(X, y, test)[0]
    cleandict = {}
    for i in range(1, 14):
        cleandict[key_map[i]] = input_list[i-1]
    line_list = []
    for key in cleandict:
        if key == 'thal':
            if cleandict[key] == 3:
                line_list += [1.0, 0.0, 0.0]
            elif cleandict[key] == 6:
                line_list += [0.0, 1.0, 0.0]
            else:
                line_list += [0.0, 0.0, 1.0]
        elif key == 'pain_type':
            pain_type = [0.0, 0.0, 0.0, 0.0]
            pain_type[int(cleandict[key]) - 1] = 1.0
            line_list += pain_type
        elif key == 'electrocardiographic':
            el = [0.0, 0.0, 0.0, 0.0]
            el[int(cleandict[key])] = 1.0
            line_list += el
        else:
            line_list.append(cleandict[key])
    InputX = np.array(line_list)
    db = get_cleaned_data_from_DB(method = 'drop')
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
    concat = np.concatenate((X, InputX.reshape(1, -1)), axis=0)
    concat = normalize(concat, axis=0, norm='max')
    return concat[-1,:].reshape(1,-1)