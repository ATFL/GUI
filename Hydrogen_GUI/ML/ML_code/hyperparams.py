import itertools


# MLP parameters
# layers = [[8],[16]]
# learnRate = [0.01]
# activation = ['tanh']
# dropout = [0]
# l2 = [0]
layers = [[8],[16],[32],[8,8],[16,16],[32,32]]
learnRate = [0.001,0.01]
activation = ['tanh']
dropout = [0]
l2 = [0,0.0001,0.001,0.01,0.1]
ANNParamList = list( itertools.product(layers,learnRate,activation,dropout,l2) )


# CNN parameters
n_layers_cnn = [1,2]
filter_length_cnn = [32,64,96]
n_filters_cnn = [8,16,32]
learnRate_cnn = [0.001,0.01]
activation_cnn = ['relu']
dropout_cnn = [0]
l2_cnn = [0,0.0001,0.01]
# n_layers_cnn = [2]
# filter_length_cnn = [96]
# n_filters_cnn = [32]
# learnRate_cnn = [0.01]
# activation_cnn = ['relu']
# dropout_cnn = [0]
# l2_cnn = [0.0001]
CNNParamList = list( itertools.product(n_layers_cnn,filter_length_cnn,n_filters_cnn,learnRate_cnn,activation_cnn,dropout_cnn,l2_cnn) )


# SVM parameters
cList = [0.1,1,10,100,1000,10000,100000]
gammaList = [0.000001,0.00001,0.0001,0.001,0.01,0.1,1,10]
SVMParamList = list( itertools.product( cList,gammaList ) )


# Random forest parameters
n_trees = [800]
max_depth = [3,5,7,9,11]
RFParamList = list( itertools.product( n_trees,max_depth ) )


# KNN parameters
neighbours = [1,3,5]
KNNParamList = neighbours