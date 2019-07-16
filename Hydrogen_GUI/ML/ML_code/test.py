import numpy as np
import os
import time
import matplotlib.pyplot as plt
from sklearn import preprocessing
import itertools
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split,ShuffleSplit
from numpy import genfromtxt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from keras.utils import np_utils
from keras.layers import Dense, Dropout, BatchNormalization, Conv1D, MaxPooling1D, UpSampling1D, Input, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras import regularizers
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from keras.layers.recurrent import LSTM, SimpleRNN
from perform_curve_representations import preprocess
from keras.optimizers import RMSprop
from keras import backend as K
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputRegressor
from matplotlib.colors import Normalize
from hyperparams import ANNParamList, SVMParamList, RFParamList, KNNParamList, CNNParamList


X = genfromtxt('/home/adiravishankara/Documents/ATFL/gui/Hydrogen_GUI/ML/clf_data.csv', delimiter=',')
Y = genfromtxt('/home/adiravishankara/Documents/ATFL/gui/Hydrogen_GUI/ML/clf_Y.csv', delimiter=',')
X = np.transpose(X)
rs = ShuffleSplit(n_splits=5, test_size=5, random_state=0)
rs.get_n_splits(X)
for train_index, test_index in rs.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
print('Original Shape X: ',X.shape, 'Original Shape Y: ', Y.shape)
# X_test = np.column_stack((X[:,53],X[:,33],X[:,48],X[:,26],X[:,11]))
# X_train = np.delete(X,[53,33,48,26,11],1)
# Y_test = np.array([Y[53,],Y[33,],Y[48,],Y[26,],Y[11,]])
# Y_train = np.delete(Y,[53,33,48,26,11],0)
# print('Modified Shape X_train: ',X_train.shape,' Modified Shape X_test: ',X_test.shape)
# print('Modified Shape Y_train: ',Y_train.shape,' Modified Shape Y_test: ',Y_test.shape)
# np.savetxt('X_test.csv',X_test, fmt='%.10f', delimiter=',')
# np.savetxt('X_train.csv',X_train, fmt='%.10f', delimiter=',')
# np.savetxt('Y_test.csv',Y_test, fmt='%.10f', delimiter=',')
# np.savetxt('Y_train.csv',Y_train, fmt='%.10f', delimiter=',')
