# Hamed's 7 Sensor Setup Code
# This version of the code will have the capability to control the linear
# actuator, begin the test, and provide a live graph of the sensor outputs.

#!/usr/bin/python3

import numpy as np 
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k') 
import random
import sys
import time
import datetime
import Adafruit_ADS1x15 as ads
import Adafruit_MAX31855.MAX31855 as MAX31855
import Adafruit_BME280 as adb
from Adafruit_BME280 import BME280 as bme2801
import Adafruit_BME280_2 as adb2
from Adafruit_BME280_2 import BME280 as bme2802
import busio
import board
import digitalio

adc1 = ads.ADS1115(0x48)
adc2 = ads.ADS1115(0x49)
## --- Global Variable Initialization --- ##
global liveGraph
global emergencyStop
global app
global printing
global progress
global startB
global veryStartTime
global totalTime
totalTime = 250
global stopB
global x1
x1 = []
global x2
x2 = []
global x3
x3 = []
global x4
x4 = []
global x5
x5 = []
global x6
x6 = []
global x7
x7 = []
global timeVector
timeVector = []
GPIO.setmode(GPIO.BCM) 
## --- Classes for Major Components --- ##

class linearActuator():
    def __init__(self, pinNum, enable):
        self.pinNum = pinNum
        self.enable = enable
        GPIO.setup(self.pinNum, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.output(self.enable, GPIO.HIGH)
        ## Make sure to change the starting pwm values for this linear actuator. 
        self.pwm = GPIO.PWM(self.pinNum, 50)
        self.pwm.start(9)
        time.sleep(5)
        GPIO.output(self.enable, GPIO.LOW) 
        self.state = 'recovery'
        
    def recover(self):
        if self.state != 'recovery':
            GPIO.output(self.enable, GPIO.HIGH)
            # Make sure to chance pwm value 
            self.pwm.ChangeDutyCycle(9)
            time.sleep(5)
            GPIO.output(self.enable, GPIO.LOW) 
            self.state = 'recovery'
        else:
            pass
    def expose(self):
        if self.state != 'exposure':
            GPIO.output(self.enable, GPIO.HIGH)
            # Make sure to change pwm values 
            self.pwm.ChangeDutyCycle(6)
            time.sleep(5)
            GPIO.output(self.enable, GPIO.LOW) 
            self.state = 'exposure'
        else:
            pass
class MOS:
    def __init__(self, adc, channel):
        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        self.GAIN = 2 / 3
        self.adc = adc
        self.channel = channel
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144

    def read(self):
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from MOS: {}".format(self.conversion_value))

        
class live_Graph(pg.PlotWidget):
    def __init__(self,parent=None):
        super(live_Graph,self).__init__()
        #self.setAutoFillBackground(True) 
        self.setRange(xRange=(0,200),yRange=(0,5),disableAutoRange=True)
        self.addLegend()
        self.setTitle("Live Graph")
        self.setStyleSheet("pg.PlotWidget {border-style: outset; max-height: 50}")
def collect_data():
    global linearAc
    global progress
    global app
    global emergencyStop
    global timeVector
    global printing
    global totalTime
    sampling_time_index = 1
    sampling_time = 0.1 #Do not change
    sensing_delay_time = 1 # Time after data recording begins for the sensor to be exposed
    sensing_retract_time = 43 # Number of seconds until the sensor is recovered
    duration_of_signal = 200 # The total number of seconds for the whole process
    start_time = time.time()
    global veryStartTime
    printing.setText("Starting Data Capture") 
    print('Starting data capture.')
    while (time.time() < (start_time + duration_of_signal)) and (emergencyStop != "STOP"):# While time is less than duration of logged file
        #print("We are inside the while loop")
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
        if (time.time() > (start_time + (sampling_time * sampling_time_index)) and (emergencyStop != "STOP")):  # if time since last sample is more than the sampling time, take another sample
           # print("Inside the graphing part...")
            global x1
            global x2
            global x3
            global x4
            global x5
            global x5
            global x6
            global x7
            x1.append(mos1.read())  # Perform analog to digital function, reading voltage from first sensor channel
            x2.append(mos2.read())
            x3.append(mos3.read())
            x4.append(mos4.read())
            x5.append(mos5.read())
            x6.append(mos6.read())
            x7.append(mos7.read())
            timeVector.append(time.time() - start_time)
           # print(*dataVector)
           # print("Before calling update Graph") 
            update_Graph()
            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        if (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (emergencyStop != "STOP")):
            print("we are in the 10-50 seconds loop") 
            if linearAc.state != 'exposure':
                linearAc.expose()

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        if (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (emergencyStop != "STOP"):
            print("Inside the first 10 seconds loop or last loop")
            if linearAc.state != 'recovery':
                linearAc.recover()

        # Otherwise, keep outputs off
##        else:
##            if linearAc.state != 'retracted':
##                linearAc.retract()
                
##    dataVector[:] = [x * (-1) for x in dataVector]
    #dataVector[:] = [baseline - x  for x in dataVector]
    if emergencyStop == "STOP":
        return
    print("Before the stack")
    combinedVector = np.column_stack((timeVector, x1, x2, x3, x4, x5, x6, x7))
    print("Right before save") 
##    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = time.strftime("/home/pi/Documents/GUI/Seven_GUI/%a%d%b%Y%H%M%S.csv",time.localtime())
    #filename = "/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/EmilyTest.csv"
    print("after filename") 
    np.savetxt(filename,combinedVector, fmt='%.10f', delimiter=',')
    print("File Saved")
    printing.setText("File Saved")
    return


def update_Graph():
    global liveGraph
    global emergencyStop
    global app
    global veryStartTime
    global totalTime
    global x1
    global x2
    global x3
    global x4
    global x5
    global x6
    global x7
    global timeVector
    
    liveGraph.clear()
    progress.setValue((time.time() - veryStartTime)/totalTime*100)
    liveGraph.plot(timeVector,x1, pen = 'b', name = 'Sensor 1')
    liveGraph.plot(timeVector,x2, pen = 'g', name = 'Sensor 2')
    liveGraph.plot(timeVector, x3, pen = 'r', name = 'Sensor 3')
    liveGraph.plot(timeVector, x4, pen = 'k', name = 'Sensor 4')
    liveGraph.plot(timeVector, x5, pen  = 'm', name = 'Sensor 5')
    liveGraph.plot(timeVector, x6, pen = 'y', name = 'Sensor 6')
    liveGraph.plot(timeVector, x7, pen = 'c', name = 'Sensor 7')
    legend = liveGraph.addLegend()
    legend.removeItem('Sensor 1')
    legend.removeItem('Sensor 2')
    legend.removeItem('Sensor 3')
    legend.removeItem('Sensor 4')
    legend.removeItem('Sensor 5')
    legend.removeItem('Sensor 6')
    legend.removeItem('Sensor 7')
    
    app.processEvents()
def test():
    global liveGraph
    liveGraph.clear()
    liveGraph.plot([1,2,3,4,5,6,7,8],[2,2,2,2,2,2,2,2], pen = 'b', name = 'Sensor 1')
    liveGraph.plot([2,3,4,5,6,7,8,9],[3,3,3,3,3,3,3,3], pen = 'r', name = 'Sensor 2')

class plot_Random(): # This is designed to test the success of the multithreading functionality
    def __init__(self,live_Graph, parent=None):
        super(plot_Random,self).__init__()
        x1 =[]
        y1 = []
        myXCounter = 0
        myYCounter = 0
        global emergencyStop
        global app
        global progress
        totalVal = 300
        while (myYCounter < 301) & (emergencyStop != "STOP"):
            
            myXCounter = myXCounter + 1
            progress.setValue(myXCounter/totalVal * 100)
            myListX.append(myXCounter)
            myYCounter = myYCounter + 1
            myListY.append(random.randint(0,5))
            live_Graph.plot(myListX,myListY)
            app.processEvents()

## --- Button Classes --- ##
class linAc_Button(QPushButton):
    def __init__(self, linAc, parent=None):
        super(linAc_Button, self).__init__()
        #self.setIconSize(QSize(15,15))
        self.linearActuator = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Click to Expose")
        self.state = "recovery"
        # Must be changed if working on Raspberry pi or personal laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        #self.green = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/on.svg")
        #self.red = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/off.svg")
        #self.setIcon(self.red)
        self.clicked.connect(lambda: self.linAc_Switch())
    def linAc_Switch(self):
        if self.state == "recovery":
            self.linearActuator.expose()
            #self.setIcon(self.green)
            self.setText("Click to Recover")
            self.state = "exposure"
        elif self.state == "exposure":
            self.linearActuator.recover()
            #self.setIcon(self.red)
            self.setText("Click to Expose")
            self.state = "off"
    def expose(self):
        if self.state == "recovery":
            self.linearActuator.expose()
            self.setText("Click to Recover")
            #self.setIcon(self.green)
            self.state = "exposure"
    def recover(self):
        if self.state == "exposure":
            self.linearActuator.recover()
            self.setText("Click to Expose")
            #self.setIcon(self.red)
            self.state = "recovery"

class start_Button(QPushButton):
    def __init__(self,parent=None):
        super(start_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Start")
        self.clicked.connect(lambda: self.start_Procedure())
      
    def start_Procedure(self):
        global emergencyStop 
        emergencyStop = "RUN"
        global stopB
        stopB.setEnabled(True)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please press 'Ok' after you are done inserting the sample.")
        msg.setWindowTitle("Sample Preparation")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        global veryStartTime
        veryStartTime = time.time()
        test_time  = time.time()
        global liveGraph
        liveGraph.clear()
        self.setEnabled(False)
        global linearAc
        linearAc.setEnabled(False) 
        global app 
        global printing
        
        global progress
        progress.setValue(0)
        
        printing.setText("Starting Test...")
        while emergencyStop != "STOP":
            collect_data()
            break
        global app 
        global printing
        global linearAc
        linearAc.setEnabled(True)
        self.setEnabled(True) 
        global progress
        global printing
        printing.setText("Ready for testing") 
        
class stop_Button(QPushButton):
    def __init__(self,parent=None):
        super(stop_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Stop")
        self.setEnabled(False)
        self.clicked.connect(lambda:self.stop_Procedure())
    def stop_Procedure(self):
        global emergencyStop
        emergencyStop = "STOP"
        global printing
        printing.setText("Stopping Test...")
        print("Stopping Test...")
        global linearAc
        linearAc.recover()
        linearAc.setEnabled(True)
        self.setEnabled(False)
        global startB
        startB.setEnabled(True) 
        
## --- Initialize Main Variables --- ##
    # Linear Actuator
linAc = linearActuator(33, 15)
    # Mos sensors 
mos1 = MOS(adc1, 0)
mos2 = MOS(adc1, 1)
mos3 = MOS(adc1, 2)
mos4 = MOS(adc1, 3)
mos5 = MOS(adc2, 0)
mos6 = MOS(adc2, 1)
mos7 = MOS(adc2, 2)

    #Max31855
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D21)
max31855 = MAX31855.MAX31855(25,24,18)

    #BME280
    # First BME 
i2c = busio.I2C(board.SCL, board.SDA)
BME2801 = bme2801(t_mode=4, p_mode=4, h_mode=4)
    # Second BME 
BME2802 = bme2802(t_mode=4, p_mode=4, h_mode=4)


## --- Page Widgets --- ##
app = QApplication([])
app.setStyle('Fusion')

mainPage = QWidget()
mainPage.setWindowTitle("Seven Sensor Setup") 
mainPage.resize(800, 600)
liveGraph = live_Graph()
progress = QtGui.QProgressBar()
linearAc = linAc_Button(linAc)
startB = start_Button()
stopB = stop_Button()
printing = QLabel()
printing.setText("Ready for Testing")


            
## --- Page Appearance Settings --- ##

pageLayout = QGridLayout()
pageLayout.addWidget(liveGraph,1,1, 3,3)
pageLayout.addWidget(progress, 4,1,1,3)
pageLayout.addWidget(startB, 5,1,1,1)
pageLayout.addWidget(stopB, 5,2,1,1)
pageLayout.addWidget(linearAc,5,3,1,1)
pageLayout.addWidget(printing,6,1,1,3) 
mainPage.setLayout(pageLayout) 
mainPage.show()




app.exec_()
GPIO.cleanup()