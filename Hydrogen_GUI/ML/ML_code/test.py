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


X = genfromtxt('/home/adiravishankara/Documents/ATFL/gui/Hydrogen_GUI/ML/training/class_training_X.csv', delimiter=',')
Y = genfromtxt('/home/adiravishankara/Documents/ATFL/gui/Hydrogen_GUI/ML/training/class_training_Y.csv', delimiter=',')
X = np.transpose(X)
rs = ShuffleSplit(n_splits=5, test_size=5, random_state=0)
rs.get_n_splits(X)
for train_index, test_index in rs.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
