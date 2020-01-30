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
from sklearn.neighbors import NearestNeighbors, KNeighborsRegressor
from keras.utils import np_utils
from keras.layers import Dense, Dropout, BatchNormalization, Conv1D, MaxPooling1D, UpSampling1D, Input, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from keras import regularizers
from sklearn.svm import SVC, SVR
from sklearn.decomposition import PCA
from keras.layers.recurrent import LSTM, SimpleRNN
from perform_curve_representations import preprocess
from keras.optimizers import RMSprop
from keras import backend as K
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from matplotlib.colors import Normalize
from hyperparams import ANNParamList, SVMParamList, RFParamList, KNNParamList, CNNParamList


def MSError(y1,y2):
	sum = 0
	for i in range(y1.shape[0]):
		for j in range(y1.shape[1]):
			sum = sum + (y1[i][j] - y2[i][j])**2
	sum = sum/(y1.shape[0]*y1.shape[1])
	return sum

def MAError(y1,y2):
	sum = 0
	for i in range(y1.shape[0]):
		for j in range(y1.shape[1]):
			sum = sum + abs(y1[i][j] - y2[i][j])
	sum = sum/(y1.shape[0]*y1.shape[1])
	return sum

def MAPError(y_pred,y_ref):
	sum = 0
	zero_sum = 0
	for i in range(y_pred.shape[0]):
		for j in range(y_pred.shape[1]):
			if y_ref[i][j] != 0:
				sum = sum + ( abs(y_pred[i][j] - y_ref[i][j]) / y_ref[i][j] )
			else:
				zero_sum = zero_sum + abs(y_pred[i][j])
	sum = sum/(y_pred.shape[0]*y_pred.shape[1]-40)
	zero_sum = zero_sum/40

	return sum, zero_sum


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
				classifier.add(Dense(layers[j], input_shape = (x_train.shape[1],),activation = activation,kernel_regularizer = regularizers.l2(l2)))
			else:
				classifier.add(Dense(layers[j],activation = activation, kernel_regularizer = regularizers.l2(l2)))
		classifier.add(Dense(2, activation = 'tanh'))
		
		adam = Adam(lr=learnRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.001)
		classifier.compile(loss = 'mse', optimizer = adam, metrics = ['accuracy'])
		
	
	if algorithm == 'SVM':
		svm = SVR( kernel='rbf', C = params[0], gamma = params[1] )
		classifier = MultiOutputRegressor(svm)

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
	# classifier.add(Dropout(0.5))
	classifier.add(Dense(32, activation = 'relu'))
	# classifier.add(Dropout(0.5))		
	classifier.add(Dense(2, activation = 'tanh'))
	
	adam = Adam(lr=learnRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.001)
	classifier.compile(loss = 'mse', optimizer = adam, metrics = ['accuracy'])
		
	return classifier
	

def featureProcessing(train, test):
	scaler = preprocessing.StandardScaler().fit(train)
	train = scaler.transform(train)
	test = scaler.transform(test)
	
	return train, test


# Load data
x_train = np.transpose( genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_train_data.csv', delimiter=',') )
x_test = np.transpose( genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_test_data.csv', delimiter=',') )

# Concentration targets
y_train = genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/targets_train.csv', delimiter=',')
y_test = genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/targets_test.csv', delimiter=',')

# Scale regression targets
scaler = MinMaxScaler(feature_range=(-0.95, 0.95))
# scaler = MinMaxScaler(feature_range=(-5, 5))
scaler.fit(y_train)
y_train = scaler.transform(y_train)
y_test = scaler.transform(y_test)


##############################################
# Test params
post_p = False
alg = 'CNN'
prep = 1


# KNN
K = 1

# RF
n_trees = 800
max_depth = 7

# SVM
C = 10
gamma = 1

# ANN
layers = [32,32]
learnRate = 0.01
activation = 'tanh'
dropout = 0
l2 = 0
epochs = 1971

# CNN
n_layers_cnn = 1
filter_length_cnn = 32
n_filters_cnn = 32
learnRate_cnn = 0.01
activation_cnn = 'relu'
dropout_cnn = 0
l2_cnn = 0.0001
epochs_cnn = 1604

##############################################

x_train, x_test = preprocess(x_train, x_test, prep)

RFparams = [ n_trees,max_depth ]
SVMparams = [ C,gamma ]
ANNparams = [ layers,learnRate,activation,dropout,l2,epochs ]
CNNparams = [ n_layers_cnn,filter_length_cnn,n_filters_cnn,learnRate_cnn,activation_cnn,dropout_cnn,l2_cnn,epochs ]


if post_p == True:
		x_train, x_test = featureProcessing(x_train, x_test)


if alg == 'KNN':

	clf = KNeighborsRegressor(n_neighbors = K, algorithm = 'brute')
	clf.fit(x_train, y_train)

	y_pred = clf.predict(x_test)


if alg == 'RF':

	clf = RandomForestRegressor(n_estimators = RFparams[0], max_depth = RFparams[1])
	clf.fit(x_train, y_train)

	y_pred = clf.predict(x_test)


if alg == 'SVM':

	clf = initializeClassifier('SVM', x_train, SVMparams)
	print(x_train.shape)
	print(y_train.shape)
	clf.fit(x_train, y_train)
	
	y_pred = clf.predict(x_test)


if alg == 'ANN':

	clf = initializeClassifier('ANN', x_train, ANNparams)
	history = clf.fit(x_train, y_train, epochs=ANNparams[5], verbose = 0, validation_data = (x_test, y_test))
	
	plt.plot(history.history['val_loss'], 'k', label='Validation loss')
	plt.xlabel('number of epochs')
	legend = plt.legend(loc='upper center', fontsize='x-large')
	plt.ylim(0,1.5)
	plt.show()
	
	y_pred = clf.predict(x_test)


if alg == 'CNN':

	x_train = x_train.reshape(( x_train.shape[0], x_train.shape[1], 1 ))
	x_test = x_test.reshape(( x_test.shape[0], x_test.shape[1], 1 ))

	clf = initializeFCN( x_train, CNNparams )
	history = clf.fit(x_train, y_train, epochs = CNNparams[7], verbose = 0, validation_data = (x_test,y_test))

	plt.plot(history.history['val_loss'], 'k', label='Validation loss')
	plt.xlabel('number of epochs')
	legend = plt.legend(loc='upper center', fontsize='x-large')
	plt.ylim(0,1.5)
	plt.show()

	y_pred = clf.predict(x_test)



print("Results for alg %s and post_p %s" % ( alg, post_p ))


print("MSE Error:")
print( MSError(scaler.inverse_transform(y_pred), scaler.inverse_transform(y_test)) )
print("MAE Error:")
print( MAError(scaler.inverse_transform(y_pred), scaler.inverse_transform(y_test)) )
print("MAPE Error:")
mape, zero_sum = MAPError(scaler.inverse_transform(y_pred), scaler.inverse_transform(y_test))
print(mape)
print("zero-sum Error:")
print( zero_sum )

# print("MSE Error:")
# print( MSError(y_pred, y_test) )
# print("MAE Error:")
# print( MAError(y_pred, y_test) )
# print("MAPE Error:")
# mape, zero_sum = MAPError(y_pred, y_test)
# print(mape)
# print("zero-sum Error:")
# print( zero_sum )