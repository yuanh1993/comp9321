import sqlite3, progressbar, sys
import DataEngineer

def feature_map():
    return {
        0: 'index',
        1: 'age',
        2: 'sex',
        3: 'pain_type',
        4: 'blood_pressure',
        5: 'cholestoral',
        6: 'blood_sugar',
        7: 'electrocardiographic',
        8: 'heart_rate',
        9: 'angina',
        10: 'oldpeak',
        11: 'ST_segment',
        12: 'vessels',
        13: 'thal',
        14: 'target integer'
    }

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_db(db_name='heart_disease.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute("select * from rawData")
    except:
        c.execute('''
                    create table rawData (
                    id integer primary key autoincrement,
                    age real,
                    sex real,
                    pain_type real,
                    blood_pressure real,
                    cholestoral real,
                    blood_sugar real,
                    electrocardiographic real,
                    heart_rate real,
                    angina real,
                    oldpeak real,
                    ST_segment real,
                    vessels real,
                    thal real,
                    target integer
                    )
                ''')
        conn.commit()
    conn.close()

def loadRawData(db_name='heart_disease.db'):
    dataContainer = DataEngineer.processData()
    raw_data = dataContainer.readData()
    nrows, ncols = raw_data.shape
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print("Start: load data.")
    bar = progressbar.ProgressBar(maxval=nrows, widgets=[progressbar.Bar('#', 'loading data: [', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for index, row in raw_data.iterrows():
        col_values = []
        for col in range(ncols):
            col_values.append(row[col])
        c.execute("insert into rawData (age, sex, pain_type, blood_pressure, cholestoral, blood_sugar,"
                  "electrocardiographic, heart_rate, angina, oldpeak, ST_segment, vessels, thal, target)"
                  " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", col_values)
        conn.commit()
        bar.update(index+1)
    bar.finish()
    print("Done: load data.")
    conn.close()

def write_db():
    create_db()
    loadRawData()

def get_slicedData(data_type, db_name='heart_disease.db'):
    features = feature_map()
    feature = features[data_type]
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from rawData")
    raw_data = c.fetchall()
    sliced_data = [{'data_type': feature,
                    'missing':[],
                    'missing_sign':'?'}]
    for i, row in enumerate(raw_data):
        if row[feature] == '?':
            sliced_data[0]["missing"].append(i)
        sliced_data.append({
            'age': row['age'],
            'sex': row['sex'],
            'value': row[feature],
        })
    conn.close()
    return sliced_data

if __name__ == '__main__':
    create_db()
    loadRawData()