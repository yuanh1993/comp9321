import numpy as np
import pandas as pd

class processData:
    def __init__(self, data_path = 'dataset/',
                       data_file = 'processed.cleveland.data',

                 ):
        self.path = data_path + data_file

    def readData(self):
        self.data = pd.read_csv(self.path, header=None)
        return self.data

    def cleanData(self):
        try:
            for index, row in self.data.iterrows():
                for col in self.data:
                    if str(row[col]) == '?':
                        print(row)
        except:
            pass

if __name__ == '__main__':
    dataContainer = processData()
    dataContainer.readData()
    dataContainer.cleanData()

