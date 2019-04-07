from dbManipulation import (read_rawData, insert_clean_drop)
from utils.methods import KNNCleaner
import numpy as np

def sweep():
    raw_data = read_rawData()
    drop_clean = []
    for data in raw_data:
        if '?' not in data:
            drop_clean.append(data)
    return insert_clean_drop(np.array(drop_clean))