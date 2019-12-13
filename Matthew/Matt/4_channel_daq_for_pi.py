#	This program is designed to automate the data collection process for the ATFL HETEK Project.
#	Developed by Matthew Barriault and Isaac Alexander


# Imports
import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import numpy as np
from pathlib import Path
import datetime
import os

#------------------------Variable Declarations------------------------#
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

sampling_time = 0.1

# Duration of signal is 10 + exposure time + 150
duration_of_signal = 240

#------------------------Function definitions------------------------#

def exposeAndCollectData():
    start_time = time.time() # capture the time at which the test began. All time values can use start_time as a reference
    dataVector1 = [] # data values to be returned from sensor 1
    dataVector2 = [] # data values to be returned from sensor 2
    dataVector3 = [] # data values to be returned from sensor 1
    dataVector4 = [] # data values to be returned from sensor 
    timeVector = []

    sampling_time_index = 1 #sampling_time_index is used to ensure that sampling takes place every interval of sampling_time, without drifting.
    data_date_and_time = time.asctime( time.localtime(time.time()) ) 
    print("Starting data capture")

    while (time.time() < (start_time + duration_of_signal)): # While time is less than duration of logged file


            if (time.time() > (start_time + (sampling_time * sampling_time_index))): # if time since last sample is more than the sampling time, take another sample
                dataVector1.append( adc.read_adc(0, gain=GAIN) ) # Perform analog to digital function, reading voltage from first sensor channel
                dataVector2.append( adc.read_adc(1, gain=GAIN) ) #  Perform analog to digital function, reading voltage from second sensor channel                     
                dataVector3.append( adc.read_adc(2, gain=GAIN) ) #  Perform analog to digital function, reading voltage from second sensor channel                     
                dataVector4.append( adc.read_adc(3, gain=GAIN) ) #  Perform analog to digital function, reading voltage from second sensor channel                     

                timeVector.append( time.time() - start_time )

                sampling_time_index += 1 # increment sampling_time_index to set awaited time for next data sample
                if ((sampling_time_index - 1) % 10 == 0):
                    print(int(time.time() - start_time))

    return dataVector1, dataVector2, dataVector3, dataVector4, timeVector


def createFolders(year, month, day):
    ##  Get the path for the folders by year, month and day
    year_path = '/home/pi/Desktop/Matt/results/' + str(year)
    year_folder = Path(year_path)
    month_path = '/home/pi/Desktop/Matt/results/' + str(year) + '/' +str(month)
    month_folder = Path(month_path)
    day_path = '/home/pi/Desktop/Matt/results/' + str(year) + '/' +str(month) + '/' + str(day)
    day_folder = Path(day_path)
    ##  Start creating the folders, when the var complete == True, all the folders have been created
    complete = False
    while complete == False:
        if year_folder.is_dir():
            if month_folder.is_dir():
                if day_folder.is_dir():
                    print ("Today's folder is ready")
                    complete = True
                else:
                    os.makedirs(day_path)
                    print ("Creating today's folder")
                    complete = True       
            else:
                os.makedirs(month_path)
        else:
            os.makedirs(year_path)

    ## This function gets the current time for the time stamp of the txt file and for the folder location

#------------------------Main operation-------------------------------#      
dataVector1, dataVector2, dataVector3, dataVector4, timeVector = exposeAndCollectData()
combinedVector = np.column_stack((timeVector, dataVector1, dataVector2, dataVector3, dataVector4))
    
current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month
day = current_time.day
createFolders(year, month, day)
hour = current_time.hour
minute = current_time.minute
#fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_bl_test.csv'
fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_2microlitre_methanol_80sec_Test2.csv'

print(fileName)
np.savetxt(r'/home/pi/Desktop/Matt/results/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(fileName), combinedVector, fmt = '%.10f', delimiter = ',')
