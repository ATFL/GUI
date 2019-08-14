#feature based model
#trying svm after fit_transorming the data
#SVM needs the data as numpy arrays
import numpy as np
from sklearn import svm
import itertools
from sklearn.svm import SVC

DataLocation = '/home/pi/Desktop/Portable_Class/'
RawDataLocation = '/home/pi/Desktop/Portable_Class/'

def featureProcessing(train, val, test):
    scaler = preprocessing.StandardScaler()

    train = scaler.fit_transform(train)
    val = scaler.fit_transform(val)
    test = scaler.fit_transform(test)

    return train, val, test

def loadData():
    data = np.genfromtxt( DataLocation + 'processed_data.csv', delimiter=',')
    data=np.transpose(data)
    targets = np.genfromtxt( RawDataLocation + 'Targets.csv', delimiter=',')
    return data, targets


def preprocess_data(X_train, X_val, X_test, prep):
    ### Preprocessing method 1 (Squish all values to between 0 and 1, but preserve differences in BL and amplitude)
    if prep == 1:
        X_test = (X_test - np.min(X_train))
        X_val = (X_val - np.min(X_val))
        X_train = (X_train - np.min(X_train))

        X_test = X_test / np.max(X_train)
        X_val = X_val / np.max(X_train)
        X_train = X_train / np.max(X_train)

    ### Preprocessing method 2 (Normalize each curve to between 0 and 1)
    if prep == 2:
        for i in range(X_train.shape[0]):
            X_train[i, :] = X_train[i, :] - X_train[i, 0]
            X_train[i, :] = X_train[i, :] / np.max(X_train[i, :])

        for i in range(X_val.shape[0]):
            X_val[i, :] = X_val[i, :] - X_val[i, 0]
            X_val[i, :] = X_val[i, :] / np.max(X_val[i, :])

        for i in range(X_test.shape[0]):
            X_test[i, :] = X_test[i, :] - X_test[i, 0]
            X_test[i, :] = X_test[i, :] / np.max(X_test[i, :])

    ### Preprocessing method 3 (BL subtract each curve))
    if prep == 3:
        for i in range(X_train.shape[0]):
            X_train[i, :] = X_train[i, :] - X_train[i, 0]

        for i in range(X_val.shape[0]):
            X_val[i, :] = X_val[i, :] - X_val[i, 0]

        for i in range(X_test.shape[0]):
            X_test[i, :] = X_test[i, :] - X_test[i, 0]

    ### Preprocessing method 4 (Z normalize each curve)
    if prep == 4:
        for i in range(X_train.shape[0]):
            mean = np.mean(X_train[i, :])
            stdev = np.std(X_train[i, :])
            X_train[i, :] = (X_train[i, :] - mean) / stdev

        for i in range(X_val.shape[0]):
            mean = np.mean(X_val[i, :])
            stdev = np.std(X_val[i, :])
            X_val[i, :] = (X_val[i, :] - mean) / stdev

        for i in range(X_test.shape[0]):
            mean = np.mean(X_test[i, :])
            stdev = np.std(X_test[i, :])
            X_test[i, :] = (X_test[i, :] - mean) / stdev

    if prep == 5:  # Same as one, but make the mean of the whole dataset zero

        X_test = (X_test - np.min(X_train))
        X_val = (X_val - np.min(X_train))
        X_train = (X_train - np.min(X_train))

        X_test = X_test / np.max(X_train)
        X_val = X_val / np.max(X_train)
        X_train = X_train / np.max(X_train)

        X_test = (X_test - np.mean(X_train))
        X_val = (X_val - np.mean(X_train))
        X_train = (X_train - np.mean(X_train))

    ### Preprocessing method 6 (mean subtract each curve))
    if prep == 6:
        for i in range(X_train.shape[0]):
            X_train[i, :] = X_train[i, :] - np.mean(X_train[i, :])

        for i in range(X_val.shape[0]):
            X_val[i, :] = X_val[i, :] - np.mean(X_val[i, :])

        for i in range(X_test.shape[0]):
            X_test[i, :] = X_test[i, :] - np.mean(X_test[i, :])

    return X_train, X_val, X_test

data, targets = loadData()

train_data = data
train_targets = targets
test_data = data
test_targets = targets

val_data = test_data
val_targets = test_targets

#train_data, val_data, test_data = preprocess_data(train_data, val_data, test_data, )

train_data = np.array(train_data)
train_targets = np.array(train_targets)
val_data = np.array(val_data)
val_targets = np.array(val_targets)
test_data = np.array(test_data)
test_targets = np.array(test_targets)

print("training data and target shapes", train_data.shape, train_targets.shape, type(train_targets))
print("val data and target shapes", val_data.shape, val_targets.shape, type(val_targets))
print("test data and target shapes", test_data.shape, test_targets.shape, type(test_targets))

cList = [1000]
gammaList = [1000]
kern= ['linear']

SVMParamList = list(itertools.product(cList, gammaList, kern))

#Labels at the beginning of the rows:
#print(totit, "iterations")

for i in range(len(SVMParamList)):
    clf = SVC(kernel=SVMParamList[i][2], C=SVMParamList[i][0], gamma=SVMParamList[i][1]).fit(train_data,train_targets[:,3])
    clf.fit(train_data, train_targets[:,3])
    acctrain = clf.score(train_data, train_targets[:,3])
    acctest = clf.score(val_data,val_targets[:,3])
    score = clf.score(test_data, test_targets[:,3])
    print(acctrain, acctest,score)

import pickle
filename = 'Port_Clf1.sav'
pickle.dump(clf, open(DataLocation + filename, 'wb'))


score = clf.score(test_data, test_targets[:,3])
pred_targt = clf.predict(test_data)

tres = np.vstack((np.transpose(test_targets), pred_targt))
