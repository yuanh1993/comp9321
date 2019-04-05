from sklearn.tree import DecisionTreeClassifier
import numpy as np

X = np.array([1, 10, 30, 60, 85, 86])
X = np.reshape(X, (6, 1))
# X = (X - np.mean(X))/(np.std(X))

# print(X)
# X = np.reshape(X, (6, 1))
y = np.array([0, 0, 0, 1, 1, 1])
# print(np.cov(X, y))
clf = DecisionTreeClassifier(random_state=0)
clf = clf.fit(X, y)
print(clf)