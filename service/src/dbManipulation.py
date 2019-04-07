import sqlite3, progressbar, sys
import DataEngineer
from utils import One_Hot_All, discrete_analysis, continous_analysis
from joblib import Parallel, delayed

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
        14: 'target'
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

def read_rawData(db_name='heart_disease.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from rawData")
    raw_data = c.fetchall()
    list_data = []
    for data in raw_data:
        list_line = []
        for key in data:
            if key == 'id':
                continue
            else:
                list_line.append(data[key])
        list_data.append(list_line)
    conn.close()
    return list_data


def get_slicedData(data_type, bucket_size = 10, db_name='heart_disease.db'):
    features = feature_map()
    feature = features[data_type]
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from rawData")
    raw_data = c.fetchall()
    if data_type in discrete_data:
        d_t = 'discrete'
    else:
        d_t = 'continuous'
    data_bucket_age = {
        'min_val': 1000,
        'max_val': 0,
        'group_count': 0
    }
    age_bucket = {}
    bucket_key_set = []
    sliced_data = [{'data_name': feature,
                    'data_type': d_t,
                    'interpreter': interpreter[data_type],
                    'missing':[],
                    'missing_sign':'?',
                    'data_length':0}]
    for i, row in enumerate(raw_data):
        if row[feature] == '?':
            sliced_data[0]["missing"].append(i)
        age_buck = int(row['age']//bucket_size) * bucket_size
        sliced_data.append({
            'age': row['age'],
            'sex': row['sex'],
            'value': row[feature],
        })
        if row[feature] not in bucket_key_set:
            bucket_key_set.append(row[feature])
        if age_buck > data_bucket_age['max_val']:
            data_bucket_age['max_val'] = age_buck
        if age_buck < data_bucket_age['min_val']:
            data_bucket_age['min_val'] = age_buck
        if age_buck in age_bucket:
            if row[feature] in age_bucket[age_buck]:
                age_bucket[age_buck][row[feature]] += 1
            else:
                age_bucket[age_buck][row[feature]] = 1
        else:
            age_bucket[age_buck] = {
                row[feature]: 1
            }
        sliced_data[0]['data_length'] += 1
    data_bucket_age['group_count'] = len(age_bucket)
    for each_age in age_bucket:
        for i in bucket_key_set:
            if i not in age_bucket[each_age]:
                age_bucket[each_age][i] = 0
        age_bucket[each_age] = dict(sorted(age_bucket[each_age].items()))
    data_bucket_age['bucket_data'] = dict(sorted(age_bucket.items()))
    sliced_data[0]['age_10'] = data_bucket_age
    context = {
        'Info': sliced_data[0],
        'data': sliced_data[1:]
    }
    conn.close()
    return context

def get_spec_feature(data_type, fix_method = 'drop', db_name='heart_disease.db'):
    features = feature_map()
    feature = features[data_type]
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select * from rawData")
    raw_data = c.fetchall()
    means = c.execute("select avg(age), avg(sex), avg(pain_type),"
                      " avg(blood_pressure), avg(cholestoral), avg(blood_sugar),"
                      " avg(electrocardiographic), avg(heart_rate), avg(angina), "
                      "avg(vessels), avg(thal), avg(target) from rawData").fetchone()
    if fix_method =='knn':
        patch = One_Hot_All(raw_data, data_type, features, means)
    X, y = [], []
    index = 0
    for data in raw_data:
        if data[feature] == '?':
            if fix_method == 'drop':
                continue
            else:
                X.append(patch[index])
                index += 1
        else:
            X.append(data[feature])
        y.append(data['target'])
    return X, y

def single_task(feature_points, i, method):
    X, y = get_spec_feature(i, fix_method=method)
    if i in discrete_data:
        feature_points[i] = discrete_analysis(X, y, i)
    else:
        feature_points[i] = continous_analysis(X, y, i)
    return feature_points


def RankFeatures(method):
    feature_points = {}
    feature_points = Parallel(n_jobs=1)(delayed(single_task)(feature_points, i, method) for i in range(1, 14))[0]
    features = [x for x in range(1, 14)]
    features.sort(key=lambda x: feature_points[x], reverse=True)
    context = {}
    feature_m = feature_map()
    for feature in features:
        context[feature_m[feature]] = feature_points[feature]
    return context

def FeatureRankDB(method, db_name = 'heart_disease.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute("select * from featureRank")
    except:
        c.execute('''
                       create table featureRank (
                       method text primary key,
                       rank_1 text,
                       rank_1_score real,
                       rank_2 text,
                       rank_2_score real,
                       rank_3 text,
                       rank_3_score real,
                       rank_4 text,
                       rank_4_score real,
                       rank_5 text,
                       rank_5_score real,
                       rank_6 text,
                       rank_6_score real,
                       rank_7 text,
                       rank_7_score real,
                       rank_8 text,
                       rank_8_score real,
                       rank_9 text,
                       rank_9_score real,
                       rank_10 text,
                       rank_10_score real,
                       rank_11 text,
                       rank_11_score real,
                       rank_12 text,
                       rank_12_score real,
                       rank_13 text,
                       rank_13_score real                      
                       )
                   ''')
        conn.commit()
    context = RankFeatures(method)
    exist = c.execute("select * from featureRank where method = '%s'" % method).fetchone()
    data_update = [method]
    for key in context:
        data_update.append(key)
        data_update.append(context[key])
    if exist == None:
        c.execute("insert into featureRank values "
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  data_update)
    else:
        data_updated = data_update[1:]
        data_updated.append(method)
        c.execute("update featureRank set "
                  "rank_1 = ?, rank_1_score = ?,"
                  "rank_2 = ?, rank_2_score = ?,"
                  "rank_3 = ?, rank_3_score = ?,"
                  "rank_4 = ?, rank_4_score = ?,"
                  "rank_5 = ?, rank_5_score = ?,"
                  "rank_6 = ?, rank_6_score = ?,"
                  "rank_7 = ?, rank_7_score = ?,"
                  "rank_8 = ?, rank_8_score = ?,"
                  "rank_9 = ?, rank_9_score = ?,"
                  "rank_10 = ?, rank_10_score = ?,"
                  "rank_11 = ?, rank_11_score = ?,"
                  "rank_12 = ?, rank_12_score = ?,"
                  "rank_13 = ?, rank_13_score = ?"
                  " where method = ?", data_updated)
    conn.commit()
    conn.close()
    return context

def readFeatureRank(method, db_name = 'heart_disease.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute("select * from featureRank where method = '%s'" % method).fetchone()
    except:
        conn.close()
        return FeatureRankDB(method)
    result = c.fetchone()
    if result == None:
        conn.close()
        return FeatureRankDB(method)
    context = {}
    i = 0
    prev = ''
    for key in result:
        if i == 0:
            i += 1
        else:
            if i % 2 == 1:
                context[result[key]] = 0.0
                prev = result[key]
            else:
                context[prev] = result[key]
            i += 1
    conn.close()
    return context

def create_clean_db(db_name='heart_disease.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    try:
        c.execute("select * from cleanData_drop")
    except:
        c.execute('''
                    create table cleanData_drop (
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
        c.execute('''
                    create table cleanData_knn (
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

def insert_clean_drop(cleaned_data, method = 'drop',db_name='heart_disease.db', replace = True):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if method == 'knn':
        table_name = 'cleanData_knn'
    else:
        table_name = 'cleanData_drop'
    if replace:
        try:
            c.execute("DROP TABLE " + table_name)
            conn.commit()
        except:
            print("Warning: recommend use create clean table instead of replace")
        if method == 'knn':
            c.execute('''
                        create table cleanData_knn (
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
        else:
            c.execute('''
                        create table cleanData_drop (
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
    nrows, ncols = cleaned_data.shape
    print(cleaned_data.shape)
    print("Start: update cleaned data:")
    bar = progressbar.ProgressBar(maxval=nrows,
                                  widgets=[progressbar.Bar('#', 'update cleaned data: [', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for index, col_values in enumerate(cleaned_data):
        c.execute("insert into " + table_name + " (age, sex, pain_type, blood_pressure, cholestoral, blood_sugar,"
                    "electrocardiographic, heart_rate, angina, oldpeak, ST_segment, vessels, thal, target)"
                    " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", col_values)
        conn.commit()
        bar.update(index + 1)
    # for index, row in cleaned_data.iterrows():
    #     col_values = []
    #     for col in range(ncols):
    #         col_values.append(row[col])
    #     c.execute("insert into " + table_name + " (age, sex, pain_type, blood_pressure, cholestoral, blood_sugar,"
    #               "electrocardiographic, heart_rate, angina, oldpeak, ST_segment, vessels, thal, target)"
    #               " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", col_values)
    #     conn.commit()
    #     bar.update(index+1)
    bar.finish()
    print("Done: update cleaned data.")
    conn.close()

def write_db():
    create_db()
    loadRawData()
    create_clean_db()