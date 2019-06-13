import numpy
import sklearn

dataVector = np.loadtxt("data.csv")

def Data_Manip(data):
      samples = 5
      smoothedData = np.zeros((len(data), 1))
#
      for j in range(samples, (len(data) - samples)):
          sum = 0
          for k in range(-1 * samples,samples + 1):
              sum = sum + data[j + k] #delete [0]

          smoothedData[j] = sum / (2 * samples + 1)

      for j in range(len(data)):
          if smoothedData[j] == 0:
              smoothedData[j] = data[j]

      ## Downsample - takes the values at time samples of multiples of 1 sec only, so one point from each 10
      downsampledData = np.zeros((1, 1))
      for j in range(len(smoothedData)):
          if (j % 10 == 0):
              if (j == 0):
                  downsampledData[0] = np.array(
                      [[smoothedData[j, 0]]])
              else:
                  downsampledData = np.vstack((downsampledData, np.array(
                      [[smoothedData[j, 0]]])))

      return downsampledData


  prep_data = Data_Manip(dataVector)

  HH_class = '/home/pi/Desktop/gui/Hetek_GUI_Dev/C_HH.sav' #this is the file against which we compare
  loaded_model = pickle.load(open(HH_class,'rb'))


  predicted_class = loaded_model.predict(pred_data)
  if predicted_class == 1:
      #app.frames[DataPage].naturalGasLabel.config(bg=warning_color)
      print("METHANE + ETHANE")

  else:
      print("METHANE")
      pass
  #if 1 natural gas is present, else no


  pass
