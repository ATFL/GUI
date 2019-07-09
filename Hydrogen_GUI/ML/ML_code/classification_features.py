import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math
from numpy import genfromtxt
import pywt

timeseries_train = genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_train_data.csv', delimiter=',' )
timeseries_val = genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_val_data.csv', delimiter=',' )
timeseries_test = genfromtxt('C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_test_data.csv', delimiter=',' )

num_train = timeseries_train.shape[1]
num_val = timeseries_val.shape[1]
num_test = timeseries_test.shape[1]

timeseries = np.hstack((timeseries_train, timeseries_val, timeseries_test))
# np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/train_val_test_curves.csv', timeseries[:,1:], fmt='%.10f', delimiter=','))

numFeatures = 119
features = np.zeros((timeseries.shape[1],numFeatures))

tFinal = 199
timeBetweenSamples = 1
derivativeDelay = 1
jFinal = int(math.floor(tFinal/timeBetweenSamples))

for i in range(timeseries.shape[1]):
	data = timeseries[:,i]
	data = data.reshape((timeseries.shape[0],1))

	# Subtract baseline
	data = data - data[0][0]

	normalizedData = np.zeros((data.shape[0],data.shape[1]))
	derivative = np.zeros((data.shape[0],data.shape[1]))
	secondDerivative = np.zeros((data.shape[0],data.shape[1]))
	
	# Create derivative vector
	for j in range(derivativeDelay, data.shape[0]-derivativeDelay):
		derivative[j][0] = (data[j][0] - data[ j-derivativeDelay ][0])/( derivativeDelay*timeBetweenSamples )
		
	# Create second derivative vector
	for j in range(derivativeDelay, derivative.shape[0]-derivativeDelay):
		secondDerivative[j][0] = (derivative[j][0] - derivative[ j-derivativeDelay ][0])/( derivativeDelay*timeBetweenSamples )
	
	# Find max value
	maxValue = data[0][0]
	for j in range(data.shape[0]):
		if (data[j][0] > maxValue):
			maxValue = data[j][0]
			jmax = j
			time_to_100_percent = j*timeBetweenSamples

	# Normalize
	for j in range(data.shape[0]):
		normalizedData[j][0] = data[j][0]/maxValue
	normalizedData = normalizedData.reshape((normalizedData.shape[0],1))
	
#------------------------------------------------------------AREA FEATURES----------------------------------------------------#	
	area = 0
	for j in range(data.shape[0]):
		area = area + timeBetweenSamples * data[j][0]
		if data[j] > (0.5 * maxValue):
			areaToHalfMax = area
			break

	area = 0
	for j in range(0, jmax):
		area = area + timeBetweenSamples * data[j][0]
	areaToMax = area

	area = 0
	for j in range(jmax, data.shape[0]):
		area = area + timeBetweenSamples * data[j][0]
		if data[j] < (0.5 * maxValue):
			areaFromMaxToHalf = area
			break

	area = 0
	for j in range(jmax, data.shape[0]):
		area = area + timeBetweenSamples * data[j][0]
	areaFromMaxToEnd = area

	totalArea = areaToMax + areaFromMaxToEnd

#---------------------------------------SLOPE95 AND SLOPEEND-----------------------------------------#

	# Find 95% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0]>0.949):
			v95 = data[j][0]
			t95 = j*timeBetweenSamples
			break
			
	# Find 5% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0]>0.049):
			v5 = data[j][0]
			t5 = j*timeBetweenSamples
			break

	vEnd = data[data.shape[0]-1][0]	
	slope95 = (v95-v5)/(t95-t5)
	slopeEnd = (vEnd - v95) / (data.shape[0]*timeBetweenSamples - t95)
			

#----------------------------TIME FEATURES----------------------------------#

	# Find time to 10%
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.099):
			time_to_10_percent = j*timeBetweenSamples
			break
			
	# Find time to 20% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.199):
			time_to_20_percent = j*timeBetweenSamples
			break
		
	# Find time to 30% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.299):
			time_to_30_percent = j*timeBetweenSamples
			break
		
	# Find time to 40% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.399):
			time_to_40_percent = j*timeBetweenSamples
			break
		
	# Find time to 50% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.499):
			time_to_50_percent = j*timeBetweenSamples
			break
		
	# Find time to 60% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.599):
			time_to_60_percent = j*timeBetweenSamples
			break
			
	# Find time to 70% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.699):
			time_to_70_percent = j*timeBetweenSamples
			break
		
	# Find time to 80% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.799):
			time_to_80_percent = j*timeBetweenSamples
			break
		
	# Find time to 90% value
	for j in range(normalizedData.shape[0]):
		if (normalizedData[j][0] > 0.899):
			time_to_90_percent = j*timeBetweenSamples
			break
			
	# Find 90% downslope value
	for j in range( jmax,  normalizedData.shape[0]):
		if (normalizedData[j][0] < 0.901):
			time_to_90_percent_ds = j*timeBetweenSamples
			break
			
	# Find 80% downslope value
	for j in range( jmax,  normalizedData.shape[0]):
		if (normalizedData[j][0] < 0.801):
			time_to_80_percent_ds = j*timeBetweenSamples
			break
			
	# Find 70% downslope value
	for j in range( jmax,  normalizedData.shape[0]):
		if (normalizedData[j][0] < 0.701):
			time_to_70_percent_ds = j*timeBetweenSamples
			break
					
	# Find 60% downslope value
	for j in range( jmax,  normalizedData.shape[0]):
		if (normalizedData[j][0] < 0.601):
			time_to_60_percent_ds = j*timeBetweenSamples
			break
			
	# Find 50% downslope value
	for j in range( jmax,  normalizedData.shape[0]):
		if (normalizedData[j][0] < 0.501):
			time_to_50_percent_ds = j*timeBetweenSamples
			break

	# Find 40% downslope value
	for j in range( jmax,  normalizedData.shape[0]):
		if (normalizedData[j][0] < 0.401):
			time_to_40_percent_ds = j*timeBetweenSamples
			break

#------------------------------------CURVE VALUE FEATURES-----------------------------------#
	
	t10_value = data[int(10/timeBetweenSamples)][0]
	t20_value = data[int(20/timeBetweenSamples)][0]
	t30_value = data[int(30/timeBetweenSamples)][0]
	t40_value = data[int(40/timeBetweenSamples)][0]
	t50_value = data[int(50/timeBetweenSamples)][0]
	t60_value = data[int(60/timeBetweenSamples)][0]
	t70_value = data[int(70/timeBetweenSamples)][0]
	t80_value = data[int(80/timeBetweenSamples)][0]
	t90_value = data[int(90/timeBetweenSamples)][0]
	t100_value = data[int(100/timeBetweenSamples)][0]
	t110_value = data[int(110/timeBetweenSamples)][0]
	t120_value = data[int(120/timeBetweenSamples)][0]
	t130_value = data[int(130/timeBetweenSamples)][0]
	t140_value = data[int(140/timeBetweenSamples)][0]
	t150_value = data[int(150/timeBetweenSamples)][0]
	t160_value = data[int(160/timeBetweenSamples)][0]
	t170_value = data[int(170/timeBetweenSamples)][0]

#------------------------------------NORMALIZED CURVE VALUE FEATURES-----------------------------------#
	
	t10_value_norm = data[int(10/timeBetweenSamples)][0] / maxValue
	t20_value_norm = data[int(20/timeBetweenSamples)][0] / maxValue
	t30_value_norm = data[int(30/timeBetweenSamples)][0] / maxValue
	t40_value_norm = data[int(40/timeBetweenSamples)][0] / maxValue
	t50_value_norm = data[int(50/timeBetweenSamples)][0] / maxValue
	t60_value_norm = data[int(60/timeBetweenSamples)][0] / maxValue
	t70_value_norm = data[int(70/timeBetweenSamples)][0] / maxValue
	t80_value_norm = data[int(80/timeBetweenSamples)][0] / maxValue
	t90_value_norm = data[int(90/timeBetweenSamples)][0] / maxValue
	t100_value_norm = data[int(100/timeBetweenSamples)][0] / maxValue
	t110_value_norm = data[int(110/timeBetweenSamples)][0] / maxValue
	t120_value_norm = data[int(120/timeBetweenSamples)][0] / maxValue
	t130_value_norm = data[int(130/timeBetweenSamples)][0] / maxValue
	t140_value_norm = data[int(140/timeBetweenSamples)][0] / maxValue
	t150_value_norm = data[int(150/timeBetweenSamples)][0] / maxValue
	t160_value_norm = data[int(160/timeBetweenSamples)][0] / maxValue
	t170_value_norm = data[int(170/timeBetweenSamples)][0] / maxValue

#------------------------------------DERIVATIVE FEATURES------------------------------------#
	
	derivative10 = derivative[int(10/timeBetweenSamples)][0]
	derivative20 = derivative[int(20/timeBetweenSamples)][0]
	derivative30 = derivative[int(30/timeBetweenSamples)][0]
	derivative40 = derivative[int(40/timeBetweenSamples)][0]
	derivative50 = derivative[int(50/timeBetweenSamples)][0]
	derivative60 = derivative[int(60/timeBetweenSamples)][0]
	derivative70 = derivative[int(70/timeBetweenSamples)][0]
	derivative80 = derivative[int(80/timeBetweenSamples)][0]
	derivative90 = derivative[int(90/timeBetweenSamples)][0]
	derivative100 = derivative[int(100/timeBetweenSamples)][0]
	derivative110 = derivative[int(110/timeBetweenSamples)][0]
	derivative120 = derivative[int(120/timeBetweenSamples)][0]
	derivative130 = derivative[int(130/timeBetweenSamples)][0]
	derivative140 = derivative[int(140/timeBetweenSamples)][0]
	derivative150 = derivative[int(150/timeBetweenSamples)][0]
	derivative160 = derivative[int(160/timeBetweenSamples)][0]
	derivative170 = derivative[int(170/timeBetweenSamples)][0]

#------------------------------------SECOND DERIVATIVE FEATURES------------------------------------#
	
	secondDerivative10 = secondDerivative[int(10/timeBetweenSamples)][0]
	secondDerivative20 = secondDerivative[int(20/timeBetweenSamples)][0]
	secondDerivative30 = secondDerivative[int(30/timeBetweenSamples)][0]
	secondDerivative40 = secondDerivative[int(40/timeBetweenSamples)][0]
	secondDerivative50 = secondDerivative[int(50/timeBetweenSamples)][0]
	secondDerivative60 = secondDerivative[int(60/timeBetweenSamples)][0]
	secondDerivative70 = secondDerivative[int(70/timeBetweenSamples)][0]
	secondDerivative80 = secondDerivative[int(80/timeBetweenSamples)][0]
	secondDerivative90 = secondDerivative[int(90/timeBetweenSamples)][0]
	secondDerivative100 = secondDerivative[int(100/timeBetweenSamples)][0]
	secondDerivative110 = secondDerivative[int(110/timeBetweenSamples)][0]
	secondDerivative120 = secondDerivative[int(120/timeBetweenSamples)][0]
	secondDerivative130 = secondDerivative[int(130/timeBetweenSamples)][0]
	secondDerivative140 = secondDerivative[int(140/timeBetweenSamples)][0]
	secondDerivative150 = secondDerivative[int(150/timeBetweenSamples)][0]
	secondDerivative160 = secondDerivative[int(160/timeBetweenSamples)][0]
	secondDerivative170 = secondDerivative[int(170/timeBetweenSamples)][0]

	# Wavelet features
	waveletData = data.reshape((data.shape[0],))
	coeffs = pywt.wavedec(waveletData, 'db6', level = 4)
	coeffs0 = coeffs[0]

	# Fourier features
	fftTrans = np.fft.fft(waveletData)
	fftTrans = np.abs(fftTrans)**2
	fftTrans = fftTrans[0:7]

	# Stack features
	features[i][0] = maxValue

	features[i][1] = areaToHalfMax
	features[i][2] = areaToMax
	features[i][3] = areaFromMaxToHalf
	features[i][4] = areaFromMaxToEnd
	features[i][5] = totalArea

	features[i][6] = slope95
	features[i][7] = slopeEnd

	features[i][8] = time_to_10_percent
	features[i][9] = time_to_20_percent
	features[i][10] = time_to_30_percent
	features[i][11] = time_to_40_percent
	features[i][12] = time_to_50_percent
	features[i][13] = time_to_60_percent
	features[i][14] = time_to_70_percent
	features[i][15] = time_to_80_percent
	features[i][16] = time_to_90_percent
	features[i][17] = time_to_100_percent
	features[i][18] = time_to_90_percent_ds
	features[i][19] = time_to_80_percent_ds
	features[i][20] = time_to_70_percent_ds
	features[i][21] = time_to_60_percent_ds
	features[i][22] = time_to_50_percent_ds
	features[i][23] = time_to_40_percent_ds

	features[i][24] = t10_value
	features[i][25] = t20_value
	features[i][26] = t30_value
	features[i][27] = t40_value
	features[i][28] = t50_value
	features[i][29] = t60_value
	features[i][30] = t70_value
	features[i][31] = t80_value
	features[i][32] = t90_value
	features[i][33] = t100_value
	features[i][34] = t110_value
	features[i][35] = t120_value
	features[i][36] = t130_value
	features[i][37] = t140_value
	features[i][38] = t150_value
	features[i][39] = t160_value
	features[i][40] = t170_value

	features[i][41] = derivative20
	features[i][42] = derivative30
	features[i][43] = derivative40
	features[i][44] = derivative50
	features[i][45] = derivative60
	features[i][46] = derivative70
	features[i][47] = derivative80
	features[i][48] = derivative90
	features[i][49] = derivative100
	features[i][50] = derivative110
	features[i][51] = derivative120
	features[i][52] = derivative130
	features[i][53] = derivative140
	features[i][54] = derivative150
	features[i][55] = derivative160
	features[i][56] = derivative170

	features[i][57] = secondDerivative20
	features[i][58] = secondDerivative30
	features[i][59] = secondDerivative40
	features[i][60] = secondDerivative50
	features[i][61] = secondDerivative60
	features[i][62] = secondDerivative70
	features[i][63] = secondDerivative80
	features[i][64] = secondDerivative90
	features[i][65] = secondDerivative100
	features[i][66] = secondDerivative110
	features[i][67] = secondDerivative120
	features[i][68] = secondDerivative130
	features[i][69] = secondDerivative140
	features[i][70] = secondDerivative150
	features[i][71] = secondDerivative160
	features[i][72] = secondDerivative170

	features[i][73] = t10_value_norm
	features[i][74] = t20_value_norm
	features[i][75] = t30_value_norm
	features[i][76] = t40_value_norm
	features[i][77] = t50_value_norm
	features[i][78] = t60_value_norm
	features[i][79] = t70_value_norm
	features[i][80] = t80_value_norm
	features[i][81] = t90_value_norm
	features[i][82] = t100_value_norm
	features[i][83] = t110_value_norm
	features[i][84] = t120_value_norm
	features[i][85] = t130_value_norm
	features[i][86] = t140_value_norm
	features[i][87] = t150_value_norm
	features[i][88] = t160_value_norm
	features[i][89] = t170_value_norm

	features[i][90:112] = coeffs0
	features[i][112:] = fftTrans

print(features.shape)
train_features = features[ 0:num_train, : ]
val_features = features[ num_train:num_train+num_val, : ]
test_features = features[ num_train+num_val: , : ]

print(train_features.shape)
print(val_features.shape)
print(test_features.shape)

np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/train_features.csv', train_features, fmt='%.10f', delimiter=',')
np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/val_features.csv', val_features, fmt='%.10f', delimiter=',')
np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/test_features.csv', test_features, fmt='%.10f', delimiter=',')