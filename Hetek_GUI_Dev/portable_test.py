import numpy as np


# def processing(data):
#
#     # Moving average filter (filters noise)
#     samples = 5
#     smoothedData = np.zeros((data.shape[0], data.shape[1]))
#
#     for j in range(samples, data.shape[0] - samples):
#         sum = 0
#         for k in range(-1 * samples,samples + 1):
#             sum = sum + data[j + k][0] #delete [0]
#
#         smoothedData[j] = sum / (2 * samples + 1)
#
#     for j in range(smoothedData.shape[0]):
#         if smoothedData[j][0] == 0:
#             smoothedData[j][0] = data[j]
#
#     # Downsample - takes the values at time samples of multiples of 1 sec only, so one point from each 10
#     downsampledData = np.zeros((1, 1))
#     for j in range(smoothedData.shape[0]):
#         if (j % 10 == 0):
#             if (j == 0):
#                 downsampledData[0][0] = np.array(
#                     [[smoothedData[j, 0]]])
#             else:
#                 downsampledData = np.vstack((downsampledData, np.array(
#                     [[smoothedData[j, 0]]])))
#
#     return downsampledData


data = np.loadtxt("Data1.csv",delimiter=",")
# portable_class_1 = "Clf_Port.sav"
# portable_class_2 = "Mix_Clf_Port.sav"

#data = processing(data)

# loaded_model1 = pickle.load(open(portable_class_1,'rb'))
# loaded_model2 = pickle.load(open(portable_class_2,'rb'))
#
# print(data.shape)
# data = data.reshape((1, data.shape[0]))
#
# print(data.shape)
#
# '''
# predictor1 = loaded_model1.predict(data)
# if predictor1 == 0:
#     print("Pure Methane")
# if predictor1 == 1:
#     print("Mix")
#     mean = np.mean(data)
#     stdev = np.std(data)
#     data_norm = (data- mean)/stdev
#     print(type(data_norm), data_norm.shape)
#     predictor2 = loaded_model2.predict(data)
# '''
