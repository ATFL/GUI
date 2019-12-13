import numpy as np
import math
import pandas as pd
import sklearn
import scipy.io
import matplotlib.pyplot as plt
import os
from numpy import genfromtxt

# Constants from measurement circuit
R = 10000
V0 = 5

# All data samples are numbered .csv files, this defines which samples will be imported for the train, validation, and test sets
# trainRange = [943,950,959,981,1022,1023,1028,1036,1040,1041] 
trainRange = [i for i in range(1194, 1318)] 
valRange = [i for i in range(1318, 1358)]
testRange = [i for i in range(1379, 1389)]

valRange.extend( range(1359, 1379) )
valRange.extend( range(1389, 1399) )
valRange.extend( range(1404, 1414) )

testRange.extend( range(1399, 1404) )
testRange.extend( range(1414, 1419) )
testRange.extend( range(1421, 1481) )

# testRange.extend( range(1343, 1348) )
# testRange.extend( range(1353, 1358) )


# This is for importing the temp and humidity data that is at the top of each .csv file
# train_temp_and_humidity = np.zeros(( len(trainRange), 2 ))
# val_temp_and_humidity = np.zeros(( len(valRange), 2 ))
# test_temp_and_humidity = np.zeros(( len(testRange), 2 ))

for i in trainRange:
	print(i)

	# Get each test individually at the specified location
	current = genfromtxt( 'C:/Users/matthew/Desktop/Automation data from Pi/All_N35_2_mfc/' + str(i) + '.csv', delimiter=',' )
	# train_temp_and_humidity[i,:] = current[0,:]

	# Discard time column and reshape data
	current = current[1:,1]
	current = current.reshape((current.shape[0],1))

	# Downsampling parameters
	desiredTimeBetweenSamples = 1
	timeBetweenSamples = 0.1
	samplingRatio = math.floor(desiredTimeBetweenSamples/timeBetweenSamples)

	### Moving average filter (filters noise)
	samples = 5
	smoothedData = np.zeros((current.shape[0],current.shape[1]))

	for j in range(samples, current.shape[0]-samples):
		sum = 0

		for k in range(-1*samples, samples+1):
			sum = sum + current[j+k][0]

		smoothedData[j] = sum/(2*samples+1)

	for j in range(smoothedData.shape[0]):
			if smoothedData[j][0] == 0:
				smoothedData[j][0] = current[j][0]


	# Downsample
	downsampledData = np.zeros((1,1))
	for j in range(smoothedData.shape[0]):
		if (j%samplingRatio == 0):
			if(j == 0):
				downsampledData[0][0] = np.array([[smoothedData[j,0]]])
			else:
				downsampledData = np.vstack((downsampledData,np.array([[smoothedData[j,0]]])))
				
	# Convert from voltage to fractional change in conductance
	# for j in range(downsampledData.shape[0]):
	# 	V = downsampledData[j][0]
	# 	downsampledData[j][0] = V/(R*(V0-V))

	# baseline = downsampledData[0][0]
	# for j in range(downsampledData.shape[0]):
	# 	downsampledData[j][0] = (downsampledData[j][0] - baseline) / baseline

	# Optionally subtract baseline of each curve	
	# Subtract baseline
	# baseline = downsampledData[0][0]
	# for j in range(downsampledData.shape[0]):
	# 	downsampledData[j][0] = downsampledData[j][0] - baseline


	if i == trainRange[0]:
		stacked = downsampledData

	else:
		stacked = np.hstack(( stacked, downsampledData ))

train = stacked

print("train shape: " + str(train.shape))
np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_train_data_raw.csv', train, fmt='%.10f', delimiter=',')

# Same for validation data
for i in valRange:
	print(i)
	current = genfromtxt( 'C:/Users/matthew/Desktop/Automation data from Pi/All_N35_2_mfc/' + str(i) + '.csv', delimiter=',' )
	current = current[1:,1]
	current = current.reshape((current.shape[0],1))

	# val_temp_and_humidity[i,:] = current[0,:]

	# Downsampling parameters
	desiredTimeBetweenSamples = 1
	timeBetweenSamples = 0.1
	samplingRatio = math.floor(desiredTimeBetweenSamples/timeBetweenSamples)

	### Moving average filter (filters noise)
	samples = 5
	smoothedData = np.zeros((current.shape[0],current.shape[1]))

	for j in range(samples, current.shape[0]-samples):
		sum = 0

		for k in range(-1*samples, samples+1):
			sum = sum + current[j+k][0]

		smoothedData[j] = sum/(2*samples+1)

	for j in range(smoothedData.shape[0]):
			if smoothedData[j][0] == 0:
				smoothedData[j][0] = current[j][0]


	# Downsample
	downsampledData = np.zeros((1,1))
	for j in range(smoothedData.shape[0]):
		if (j%samplingRatio == 0):
			if(j == 0):
				downsampledData[0][0] = np.array([[smoothedData[j,0]]])
			else:
				downsampledData = np.vstack((downsampledData,np.array([[smoothedData[j,0]]])))

				
	# Convert from voltage to fractional change in conductance
	# for j in range(downsampledData.shape[0]):
	# 	V = downsampledData[j][0]
	# 	downsampledData[j][0] = V/(R*(V0-V))

	# baseline = downsampledData[0][0]
	# for j in range(downsampledData.shape[0]):
	# 	downsampledData[j][0] = (downsampledData[j][0] - baseline) / baseline
		

	# Optionally subtract baseline of each curve	
	# Subtract baseline
	# baseline = smoothedData[0][0]
	# for j in range(smoothedData.shape[0]):
	# 	smoothedData[j][0] = smoothedData[j][0] - baseline

	if i == valRange[0]:
		stacked = downsampledData

	else:
		stacked = np.hstack(( stacked, downsampledData ))

val = stacked

print("val shape: " + str(val.shape))
np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_val_data_raw.csv', val, fmt='%.10f', delimiter=',')

for i in testRange:
	print(i)
	current = genfromtxt( 'C:/Users/matthew/Desktop/Automation data from Pi/All_N35_2_mfc/' + str(i) + '.csv', delimiter=',' )
	current = current[1:,1]
	current = current.reshape((current.shape[0],1))

	# test_temp_and_humidity[i,:] = current[0,:]

	# Downsampling parameters
	desiredTimeBetweenSamples = 1
	timeBetweenSamples = 0.1
	samplingRatio = math.floor(desiredTimeBetweenSamples/timeBetweenSamples)

	### Moving average filter (filters noise)
	samples = 5
	smoothedData = np.zeros((current.shape[0],current.shape[1]))

	for j in range(samples, current.shape[0]-samples):
		sum = 0

		for k in range(-1*samples, samples+1):
			sum = sum + current[j+k][0]

		smoothedData[j] = sum/(2*samples+1)

	for j in range(smoothedData.shape[0]):
			if smoothedData[j][0] == 0:
				smoothedData[j][0] = current[j][0]


	# Downsample
	downsampledData = np.zeros((1,1))
	for j in range(smoothedData.shape[0]):
		if (j%samplingRatio == 0):
			if(j == 0):
				downsampledData[0][0] = np.array([[smoothedData[j,0]]])
			else:
				downsampledData = np.vstack((downsampledData,np.array([[smoothedData[j,0]]])))

				
	# Convert from voltage to fractional change in conductance
	for j in range(downsampledData.shape[0]):
		V = downsampledData[j][0]
		downsampledData[j][0] = V/(R*(V0-V))

	baseline = downsampledData[0][0]
	for j in range(downsampledData.shape[0]):
		downsampledData[j][0] = (downsampledData[j][0] - baseline) / baseline
		

	if i == testRange[0]:
		stacked = downsampledData

	else:
		stacked = np.hstack(( stacked, downsampledData ))

test = stacked

print("test shape: " + str(test.shape))
np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_arbitrary_mix/data_and_targets/processed_test_data.csv', test, fmt='%.10f', delimiter=',')

# np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_natural_gas/data_and_targets/train_temp_humidity.csv', train_temp_and_humidity, fmt='%.10f', delimiter=',')
# np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_natural_gas/data_and_targets/val_temp_humidity.csv', val_temp_and_humidity, fmt='%.10f', delimiter=',')
# np.savetxt(r'C:/Users/matthew/Desktop/Testing_algorithms_on_natural_gas/data_and_targets/test_temp_humidity.csv', test_temp_and_humidity, fmt='%.10f', delimiter=',')
