import os
import sys
import time
import datetime
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import serial
import numpy as np
from pathlib import Path


def createFolders(year, month, day):
    ##  Get the path for the folders by year, month and day
    year_path = '/home/pi/Documents/Tests/' + str(year)
    year_folder = Path(year_path)
    month_path = '/home/pi/Documents/Tests/' + str(year) + '/' + str(month)
    month_folder = Path(month_path)
    day_path = '/home/pi/Documents/Tests/' + str(year) + '/' + str(month) + '/' + str(day)
    day_folder = Path(day_path)
    ##  Start creating the folders, when the var complete == True, all the folders have been created
    complete = False
    while complete == False:
        if year_folder.is_dir():
            if month_folder.is_dir():
                if day_folder.is_dir():
                    complete = True
                else:
                    try:
                        print(day_path)
                        original_mask = os.umask(0x0000)
##                        desired_permission = 0777
                        os.makedirs(day_path, mode=0x0777)
                        complete = True
                    finally:
                        os.umask(original_mask)
            else:
                os.makedirs(month_path)
        else:
            os.makedirs(year_path)
    pass

GPIO.setmode(GPIO.BOARD) 
    
LA = 16
Laenable = 18
GPIO.setup(LA, GPIO.OUT)
GPIO.setup(Laenable, GPIO.OUT)
GPIO.output(Laenable, GPIO.HIGH)
dataVector = []
timeVector = []
startTime = time.time()

pwm = GPIO.PWM(LA, 50)
pwm.start(9)
time.sleep(2)
GPIO.output(Laenable, GPIO.LOW)
time.sleep(240)

GPIO.output(Laenable, GPIO.HIGH)
pwm.ChangeDutyCycle(5)
time.sleep(2)
GPIO.output(Laenable, GPIO.LOW)
firstTime = time.time()
while((time.time() - firstTime)< 42):
    dataVector.append(adc1.read_adc(0, gain = 2/3))
    timeVector.append(time.time() - startTime)
    
GPIO.output(Laenable, GPIO.HIGH)
pwm.ChangeDutyCycle(9)
time.sleep(2)
GPIO.output(Laenable, GPIO.LOW)
secondTime = time.time()
while((time.time() - secondTime) < 60):
    dataVector.append(adc1.read_adc(0, gain = 2/3))
    timeVector.append(time.time() - startTime)

combinedVector = np.column_stack((timeVector, dataVector))
current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month
day = current_time.day
createFolders(year, month, day)
hour = current_time.hour
minute = current_time.minute
fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + 'Mo_Neg_nolid.csv'
    #fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_bl.csv'
np.savetxt(r'/home/pi/Documents/Tests/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(fileName), combinedVector, fmt='%.10f', delimiter=',')
pass
print("Data has been saved!") 


