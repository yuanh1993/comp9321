from model.stack import StackClassification
from dbManipulation import get_cleaned_data_from_DB
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, SpectralClustering
import numpy as np

def test_learning(method = 'drop'):
    db = get_cleaned_data_from_DB(method)
    db_list = []
    target = []
    test = []
    y_test = []
    i = 0
    for line in db:
        line_list = []
        for key in line:
            if key == 'id':
                continue
            elif key == 'target':
                cls = line[key]
                if cls > 0:
                    cls = 1
                if i < 270:
                    target.append(cls)
                else:
                    y_test.append(cls)
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
        if i < 270:
            db_list.append(line_list)
        else:
            test.append(line_list)
        i += 1
    X = np.array(db_list)
    X = normalize(X, axis=0, norm='max')
    y = np.array(target)
    test = np.array(test)
    test = normalize(test, axis=0, norm='max')
    clf = StackClassification()
    print(X.shape, y.shape)
    clf.fit(X, y)
    print(clf.predict(test))
    for n in y_test:
        print(n, end=' ')

def clustering(cluster_method = 'kmeans'):
    db = get_cleaned_data_from_DB(method='drop')
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
    pca = PCA(n_components=2)
    pca.fit(X.T)
    X = pca.components_.T
    if cluster_method == 'spectral':
        clustering = SpectralClustering(n_clusters=2,
                                        assign_labels="discretize",
                                        random_state = 0).fit(X)
    else:
        clustering = KMeans(n_clusters=2, random_state=0).fit(X)
    return X, clustering.labels_, y

if __name__ == '__main__':
    # test_learning(method='drop')
    clustering(cluster_method = 'kmeans')