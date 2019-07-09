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
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def initializeClassifier(algorithm, x_train, params):
	if algorithm == 'ANN':
		classifier = Sequential()
		layers = params[0]
		learnRate = params[1]
		activation = params[2]
		dropout = params[3]
		l2 = params[4]
		
		for j in range(len(layers)):
			if j == 0:
				classifier.add(Dense(layers[j], input_shape = (x_train.shape[1],), activation = activation, kernel_regularizer = regularizers.l2(l2)))
			else:
				classifier.add(Dense(layers[j],activation = activation, kernel_regularizer = regularizers.l2(l2)))
		classifier.add(Dense(3, activation = 'softmax'))
		
		adam = Adam(lr=learnRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.001)
		classifier.compile(loss = 'categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])
		
	
	if algorithm == 'SVM':
		classifier = SVC( kernel='rbf', C = params[0], gamma = params[1] )

	return classifier


def initializeFCN(x_train, params):
	classifier = Sequential()
	n_layers = params[0]
	filter_length = params[1]
	n_filters = params[2]
	learnRate = params[3]
	activation = params[4]
	dropout = params[5]
	l2 = params[6]
	
	for j in range(n_layers):
		if j == 0:
			classifier.add(Conv1D( n_filters, filter_length, input_shape = (x_train.shape[1],1), activation = activation, kernel_regularizer = regularizers.l2(l2), padding = 'valid' ))
			classifier.add( MaxPooling1D(2) )
		else:
			classifier.add(Conv1D( n_filters, int(filter_length/(2**j)), activation = activation, kernel_regularizer = regularizers.l2(l2), padding = 'valid' ))
			classifier.add( MaxPooling1D(2) )
	
	classifier.add( Flatten() )
	classifier.add(Dense(32, activation = 'relu'))		
	classifier.add(Dense(3, activation = 'softmax'))
	
	adam = Adam(lr=learnRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.001)
	classifier.compile(loss = 'categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])
		
	return classifier
	

def featureProcessing(train, test):
	scaler = preprocessing.StandardScaler().fit(train)
	train = scaler.transform(train)
	test = scaler.transform(test)
	
	return train, test


# Load data
x_train = np.transpose( genfromtxt('C:/Users/barr_mt/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_train_data.csv', delimiter=','))
x_test = np.transpose( genfromtxt('C:/Users/barr_mt/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_test_data.csv', delimiter=','))

# Concentration targets
y_train = genfromtxt('C:/Users/barr_mt/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/targets_train_binary.csv', delimiter=',')
y_test = genfromtxt('C:/Users/barr_mt/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/targets_test_binary.csv', delimiter=',')
y_train_enc = np_utils.to_categorical(y_train)
y_test_enc = np_utils.to_categorical(y_test)



##############################################
# Test params
post_p = False
alg = 'CNN'
prep = 4


# KNN
K = 1

# RF
n_trees = 800
max_depth = 5

# SVM
C = 10000
gamma = 0.1

# ANN
layers = [32]
learnRate = 0.001 ####
activation = 'tanh'
dropout = 0
l2 = 0
epochs = 1944

# CNN
n_layers_cnn = 2
filter_length_cnn = 96
n_filters_cnn = 32
learnRate_cnn = 0.01
activation_cnn = 'relu'
dropout_cnn = 0
l2_cnn = 0.0001
epochs_cnn = 2000

##############################################

x_train, x_test = preprocess(x_train, x_test, prep)

RFparams = [ n_trees,max_depth ]
SVMparams = [ C,gamma ]
ANNparams = [ layers,learnRate,activation,dropout,l2,epochs ]
CNNparams = [ n_layers_cnn,filter_length_cnn,n_filters_cnn,learnRate_cnn,activation_cnn,dropout_cnn,l2_cnn,epochs ]


if post_p == True:
		x_train, x_test = featureProcessing(x_train, x_test)


if alg == 'KNN':

	clf = KNeighborsClassifier(n_neighbors = K, algorithm = 'brute')
	clf.fit(x_train, y_train)

	y_pred = clf.predict(x_test)


if alg == 'RF':

	clf = RandomForestClassifier(n_estimators = RFparams[0], max_depth = RFparams[1])
	clf.fit(x_train, y_train)

	y_pred = clf.predict(x_test)


if alg == 'SVM':

	clf = initializeClassifier('SVM', x_train, SVMparams)
	clf.fit(x_train, y_train)
	
	y_pred = clf.predict(x_test)


if alg == 'ANN':

	clf = initializeClassifier('ANN', x_train, ANNparams)
	history = clf.fit(x_train, y_train_enc, epochs=ANNparams[5], verbose = 1, validation_data = (x_test, y_test_enc))
	#history1 = clf.fit(x_train, y_train_enc, epochs=5000, verbose = 1, validation_data = (x_test, y_test_enc))
	
	plt.plot(history.history['val_loss'], 'k', label='Test loss')
	plt.plot(history.history['val_acc'], 'k:', label='Test accuracy')
	plt.xlabel('number of epochs')
	legend = plt.legend(loc='upper center', fontsize='x-large')
	plt.ylim(0,1.5)
	plt.show()
	
	y_pred = clf.predict_classes(x_test)


if alg == 'CNN':

	x_train = x_train.reshape(( x_train.shape[0], x_train.shape[1], 1 ))
	x_test = x_test.reshape(( x_test.shape[0], x_test.shape[1], 1 ))

	clf = initializeFCN( x_train, CNNparams )
	history = clf.fit(x_train, y_train_enc, epochs = CNNparams[7], verbose = 0, validation_data = (x_test,y_test_enc))

	plt.plot(history.history['val_loss'], 'k', label='Test loss')
	plt.plot(history.history['val_acc'], 'k:', label='Test accuracy')
	plt.xlabel('number of epochs')
	legend = plt.legend(loc='upper center', fontsize='x-large')
	plt.ylim(0,1.5)
	plt.show()

	y_pred = clf.predict_classes(x_test)



q = 0
for i in range(len(y_test)):
	if y_test[i] == y_pred[i]:
		q = q + 1

acc = q / len(y_test)

print(f'Results for {alg}: {acc}')