import tkinter as tk
from tkinter import*
import sys
import datetime
from pathlib import Path
import os
import _thread
import tkinter.ttk as ttk
import RPi.GPIO as GPIO
import serial
import numpy as np
import time
import Adafruit_ADS1x15
from numpy import genfromtxt
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np

global positionSensor


            
adc1 = Adafruit_ADS1x15.ADS1115(address = 0x48)
#adc2 = Adafruit_ADS1x15.ADS1115(address = 0x49)
start_time = time.time()  # capture the time at which the test began. All time values can use start_time as a reference
dataVector1 = []  # data values to be returned from sensor 1
timeVector = []  # time values associated with data values
count = 0


while (count < 2000):
#    print("Big Orange: ", adc1.read_adc(0, gain = 2/3))
#    print ("Sensor 2 Val: ", adc1.read_adc(1, gain = 2/3))
#    print("Pressure: ", adc1.read_adc(1, gain = 2/3))
    dataVector1.append(adc1.read_adc(3, gain=2/3))
    timeVector.append(time.time() - start_time)
    print ("Sensor Val: ", (adc1.read_adc(3, gain = 2/3))/pow(2, 15)*6.144)
    
#    print("Temperature: ", adc2.read_adc(1, gain = 2/3))
#    print ("Pressure: ", adc2.read_adc(0, gain = 2/3))
#    
    time.sleep(0.1) 
    count = count + 1
    
##pwm.ChangeDutyCycle(4.5)
##count2 = 0 
##while (count2 < 10):
##    print("Sensor 1 Val: ", adc.read_adc(0, gain = 2/3))
##    print ("Sensor 2 Val: ", adc.read_adc(1, gain = 2/3))
##    time.sleep(1) 
##    count2 = count2 + 1
##    
##
##pwm.stop()
combinedVector = np.column_stack((timeVector, dataVector1))   
current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month
day = current_time.day
#createFolders(year, month, day)
hour = current_time.hour
minute = current_time.minute

fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + 'Mo_Neg_nolid.csv'
#fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_bl.csv'

np.savetxt(r'/home/pi/Documents/Hameds_Tests/'+str(fileName), combinedVector, fmt='%.10f', delimiter=',')
GPIO.cleanup()
print('ended')


    
