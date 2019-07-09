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



class MidpointNormalize(Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


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
	classifier.add(Dense(32, activation = 'relu'))
	classifier.add(Dense(3, activation = 'softmax'))

	adam = Adam(lr=learnRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.001)
	classifier.compile(loss = 'categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])

	return classifier


def standard_scaler(train, test):
	scaler = preprocessing.StandardScaler().fit(train)
	train = scaler.transform(train)
	test = scaler.transform(test)

	return train, test

# Load data
X = genfromtxt('/home/adiravishankara/Documents/ATFL/gui/Hydrogen_GUI/ML/training/class_training_X.csv', delimiter=',')
Y = genfromtxt('/home/adiravishankara/Documents/ATFL/gui/Hydrogen_GUI/ML/training/class_training_Y.csv', delimiter=',')

X_test = np.column_stack((X[:,53],X[:,33],X[:,48],X[:,26],X[:,11]))
X_train = np.delete(X,[53,33,48,26,11],1)
Y_test = np.array([Y[53,],Y[33,],Y[48,],Y[26,],Y[11,]])
#Y_test = np.column_stack((Y_test))
Y_train = np.delete(Y,[53,33,48,26,11],0)
#Y_train = np.column_stack((Y_train))

x_train = np.transpose(X_train)
x_val = np.transpose(X_test)



# Concentration targets
# y_train = np.transpose(Y_train)
# y_val = np.transpose(Y_test)
y_train = Y_train
y_val = Y_test

print('Original Shape X: ',X.shape, 'Original Shape Y: ', Y.shape)
print('Modified Shape X_train: ',x_train.shape,' Modified Shape X_test: ',x_val.shape)
print('Modified Shape Y_train: ',y_train.shape,' Modified Shape Y_test: ',y_val.shape)
np.savetxt('X_test1.csv',X_test, fmt='%.10f', delimiter=',')
np.savetxt('X_train1.csv',X_train, fmt='%.10f', delimiter=',')
np.savetxt('Y_test1.csv',y_val, fmt='%.10f', delimiter=',')
np.savetxt('Y_train1.csv',y_train, fmt='%.10f', delimiter=',')
y_train_enc = np_utils.to_categorical(y_train)
y_val_enc = np_utils.to_categorical(y_val)


##############################################
# Test params
post_p = False
alg = 'ANN'
prep = 4
##############################################

x_train, x_val = preprocess(x_train, x_val, prep)

if post_p == True:
	x_train, x_val = standard_scaler(x_train, x_val)

scores = []

# MLP only
best_epochs=[]
best_Acces=[]
best_Losses=[]

if alg == 'SVM':
	ParamList = SVMParamList

if alg == 'RF':
	ParamList = RFParamList

if alg == 'KNN':
	ParamList = KNNParamList

if alg == 'ANN':
	ParamList = ANNParamList

if alg == 'CNN':
	ParamList = CNNParamList

k = 0
for params in ParamList:

	if alg == 'KNN':
		clf = KNeighborsClassifier(n_neighbors = params, algorithm = 'brute')
		clf.fit(x_train, y_train)

		y_pred = clf.predict(x_val)


	if alg == 'RF':
		clf = RandomForestClassifier(n_estimators = params[0], max_depth = params[1])
		clf.fit(x_train, y_train)

		y_pred = clf.predict(x_val)

		q = 0
		for i in range(len(y_val)):
			if y_val[i] == y_pred[i]:
				q = q + 1


	if alg == 'SVM':
		clf = initializeClassifier('SVM', x_train, params)
		clf.fit(x_train, y_train)

		y_pred = clf.predict(x_val)


	if alg == 'ANN':
		clf = initializeClassifier('ANN', x_train, params)
		history = clf.fit(x_train, y_train_enc, epochs = 2000, verbose = 0, validation_data = (x_val,y_val_enc))

		bestValAcc = np.max( history.history['val_acc'] )
		bestValLoss = np.min( history.history['val_loss'] )
		bestValAccEpoch = np.argmax( history.history['val_acc'] )
		bestValLossEpoch = np.argmin( history.history['val_loss'] )

		# plt.plot(history.history['val_loss'], 'k', label='Validation loss')
		# plt.plot(history.history['val_acc'], 'k:', label='Validation accuracy')
		# plt.xlabel('number of epochs')
		# legend = plt.legend(loc='upper center', fontsize='x-large')
		# plt.ylim(0,1.5)
		# plt.show()

		y_pred = clf.predict_classes(x_val)


	if alg == 'CNN':
		x_train = x_train.reshape(( x_train.shape[0], x_train.shape[1], 1 ))
		x_val = x_val.reshape(( x_val.shape[0], x_val.shape[1], 1 ))

		clf = initializeFCN( x_train, params )
		history = clf.fit(x_train, y_train_enc, epochs = 2000, verbose = 0, validation_data = (x_val,y_val_enc))

		bestValAcc = np.max( history.history['val_acc'] )
		bestValLoss = np.min( history.history['val_loss'] )
		bestValAccEpoch = np.argmax( history.history['val_acc'] )
		bestValLossEpoch = np.argmin( history.history['val_loss'] )

		# plt.plot(history.history['val_loss'], 'k', label='Validation loss')
		# plt.plot(history.history['val_acc'], 'k:', label='Validation accuracy')
		# plt.xlabel('number of epochs')
		# legend = plt.legend(loc='upper center', fontsize='x-large')
		# plt.ylim(0,1.5)
		# plt.show()

		y_pred = clf.predict_classes(x_val)


	if K.backend() == 'tensorflow':
		K.clear_session()
	print(k)
	k += 1

	q = 0
	for i in range(len(y_val)):
		if y_val[i] == y_pred[i]:
			q = q + 1

	scores.append(q / len(y_val))

	# For SVM heatmap
	# SVMScoreMatrix[cPos][gammaPos] = q / len(y_val)
	# gammaPos += 1
	# if gammaPos == 8:
	# 	cPos += 1
	# 	gammaPos = 0

	if alg == 'ANN' or alg == 'CNN':
		best_epochs.append(bestValLossEpoch)
		best_Acces.append(bestValAcc)
		best_Losses.append(bestValLoss)
		print(bestValLoss)
		print(bestValAcc)
		print(bestValLossEpoch)

print(scores)
bestScore = np.max(scores)
bestScoreIndex = np.argmax(scores)

if alg == 'SVM':
	bestSVMParams = SVMParamList[bestScoreIndex]
	print("Best results for SVM: %s with %s" % ( bestScore, bestSVMParams ))

if alg == 'RF':
	bestRFParams = RFParamList[bestScoreIndex]
	print("Best results for RF : %s with %s" % ( bestScore, bestRFParams ))

if alg == 'KNN':
	bestKNNParams = KNNParamList[bestScoreIndex]
	print("Best results for KNN: %s with %s" % ( bestScore, bestKNNParams ))

if alg == 'ANN':
	bestScore = np.max(best_Acces)
	bestScoreIndex = np.argmax(best_Acces)
	bestANNEpochs = best_epochs[bestScoreIndex]
	bestANNParams = ANNParamList[bestScoreIndex]
	print("Best results for MLP: %s with %s and %s epochs" % (  bestScore, bestANNParams, bestANNEpochs ))

if alg == 'CNN':
	bestScore = np.max(best_Acces)
	bestScoreIndex = np.argmax(best_Acces)
	bestCNNEpochs = best_epochs[bestScoreIndex]
	bestCNNParams = CNNParamList[bestScoreIndex]
	print("Best results for CNN: %s with %s and %s epochs" % (  bestScore, bestCNNParams, bestCNNEpochs ))
