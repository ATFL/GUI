import numpy as np
import os
import time
import matplotlib.pyplot as plt
from sklearn import preprocessing
import itertools
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from numpy import genfromtxt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib 
from sklearn.model_selection import LeaveOneOut, StratifiedKFold
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from keras.utils import np_utils
from keras.layers import Dense, Dropout, Conv1D, MaxPooling1D, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras import regularizers
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.optimizers import RMSprop
import pywt


def preprocess(X_train, X_test, prep, Y_train=None):

	### Preprocessing method 1 (Squish all values to between 0 and 1, but preserve differences in BL and amplitude)
	if prep == 1:
		X_test = ( X_test - np.min(X_train) )
		X_train = ( X_train - np.min(X_train) )

		X_test = X_test / np.max(X_train)
		X_train = X_train / np.max(X_train)


	### Preprocessing method 2 (Normalize each curve to between 0 and 1)
	if prep == 2:
		for i in range(X_train.shape[0]):
			X_train[i,:] = X_train[i,:] - X_train[i,0]
			X_train[i,:] = X_train[i,:] / np.max(X_train[i,:])

		for i in range(X_test.shape[0]):
			X_test[i,:] = X_test[i,:] - X_test[i,0]
			X_test[i,:] = X_test[i,:] / np.max(X_test[i,:])


	### Preprocessing method 3 (BL subtract each curve))
	if prep == 3:
		for i in range(X_train.shape[0]):
			X_train[i,:] = X_train[i,:] - X_train[i,0]

		for i in range(X_test.shape[0]):
			X_test[i,:] = X_test[i,:] - X_test[i,0]


	### Preprocessing method 4 (Z normalize each curve)
	if prep == 4:
		for i in range(X_train.shape[0]):
			mean = np.mean(X_train[i,:])
			stdev = np.std(  X_train[i,:] )
			X_train[i,:] = ( X_train[i,:] - mean ) / stdev

		for i in range(X_test.shape[0]):
			mean = np.mean(X_test[i,:])
			stdev = np.std(  X_test[i,:] )			
			X_test[i,:] = ( X_test[i,:] - mean ) / stdev

	if prep == 5:
		pca1 = PCA(n_components = 8)
		pca1.fit(X_train)
		X_train = pca1.transform(X_train)
		X_test = pca1.transform(X_test)


	if prep == 6:
		pca1 = PCA(n_components = 8, whiten = True)
		pca1.fit(X_train)
		X_train = pca1.transform(X_train)
		X_test = pca1.transform(X_test)

	if prep == 9:
		lda = LinearDiscriminantAnalysis()
		lda.fit(X_train, Y_train)
		X_train = lda.transform(X_train)
		X_test = lda.transform(X_test)


	if prep == 7: # Same as one, but make the mean of the whole dataset zero

		X_test = ( X_test - np.min(X_train) )
		X_train = ( X_train - np.min(X_train) )

		X_test = X_test / np.max(X_train)
		X_train = X_train / np.max(X_train)

		X_test = ( X_test - np.mean(X_train) )
		X_train = ( X_train - np.mean(X_train) )

	### Preprocessing method 3 (mean subtract each curve))
	if prep == 8:
		for i in range(X_train.shape[0]):
			X_train[i,:] = X_train[i,:] - np.mean(X_train[i,:])

		for i in range(X_test.shape[0]):
			X_test[i,:] = X_test[i,:] - np.mean(X_test[i,:])

	return X_train, X_test


def DW_transform(X_train, X_test, prep):

	coeffs_train = pywt.wavedec(X_train, 'db6', level = 4)
	coeffs_test = pywt.wavedec(X_test, 'db6', level = 4)

	X_train_enc = coeffs_train[0]
	X_test_enc = coeffs_test[0]

	return X_train_enc, X_test_enc


def DF_transform(X_train, X_test, prep):

	return X_trans


def LDA_transform(X_train, X_test, prep):

	return X_train_enc, X_test_enc


def PCA_transfom(X_train, X_test, prep):

	return X_train_enc, X_test_enc
	

def AE_transform(X_train, X_test, prep):
	input_dim = 200

	autoencoder1 = Sequential()
	# autoencoder1.add( Dense(128, input_shape= (input_dim,), activation = 'relu') )
	autoencoder1.add( Dense(64, input_shape= (input_dim,), activation = 'relu') )
	autoencoder1.add( Dense(8, activation = 'relu') )
	autoencoder1.add( Dense(64, activation = 'relu') )
	# autoencoder1.add( Dense(128, activation = 'relu') )
	if prep == 0 or prep == 3:
		autoencoder1.add( Dense(input_dim, activation = 'relu') )
	if prep == 1 or prep == 2:
		autoencoder1.add( Dense(input_dim, activation = 'sigmoid') )
	if prep == 4 or prep == 7 or prep == 8:
		autoencoder1.add( Dense(input_dim, activation = 'linear') )

	autoencoder1.compile(optimizer='adam', loss = 'mse')
	autoencoder1.fit( X_train, X_train, epochs=500, verbose=0 )
		

	encoder1 = Sequential()
	encoder1.add(Dense(128, input_shape = (200,), weights = autoencoder1.layers[0].get_weights(), activation = 'relu'))
	encoder1.add(Dense(32, weights = autoencoder1.layers[1].get_weights(), activation = 'relu'))
	encoder1.add(Dense(6, weights = autoencoder1.layers[2].get_weights(), activation = 'relu'))


	X_train_enc = encoder1.predict(X_train)
	X_test_enc = encoder1.predict(X_test)


	return X_train_enc, X_test_enc


def conv_AE_transform(X_train, X_test, prep):
	input_dim = 200

	X_train = X_train.reshape((X_train.shape[0], X_train.shape[1],1))
	X_test = X_test.reshape((X_test.shape[0], X_test.shape[1],1))
	X_train_humidity = X_train_humidity.reshape((X_train_humidity.shape[0], X_train_humidity.shape[1],1))
	X_test_humidity = X_test_humidity.reshape((X_test_humidity.shape[0], X_test_humidity.shape[1],1))	

	autoencoder1 = Sequential()
	autoencoder1.add( Conv1D(16, 64, input_shape= (input_dim,1), activation = 'relu', padding = 'same') )
	if prep == 0 or prep == 3:
		autoencoder1.add( Conv1D(1, 1, activation = 'relu') )
	if prep == 1 or prep == 2:
		autoencoder1.add( Conv1D(1, 1, activation = 'sigmoid') )
	if prep == 4 or prep == 7:
		autoencoder1.add( Conv1D(1, 1, activation = 'linear') )


	autoencoder1.compile(optimizer='adam', loss = 'mse')
	autoencoder1.fit( X_train, X_train, epochs=500, verbose=0 )
		

	encoder1 = Sequential()
	encoder1.add( Conv1D(16, 64, input_shape= (input_dim,1), weights = autoencoder1.layers[0].get_weights(), activation = 'relu'))
	encoder1.add(Flatten())


	X_train_enc = encoder1.predict(X_train)
	X_test_enc = encoder1.predict(X_test)


	return X_train_enc, X_test_enc




