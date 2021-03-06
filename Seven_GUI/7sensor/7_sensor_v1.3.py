##7_sensor_v1.3

## This version Inlcudes the BME Sensor, including a seperate graph for the environmental factors, and check boxes to controlw hich sensors are being tabulated

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
#i2c 76
from Adafruit_BME280 import *
#i2c 77
from Adafruit_BME280_2 import *
import busio
import board
import digitalio
#from parameters_7sensor import *
# TODO: ADD BME and MAX Code

########SETUP##########
adc1 = ads.ADS1115(0x48)
adc2 = ads.ADS1115(0x49)

global timeVector
global x1
global x2
global x3
global x4
global x5
global x6
global monitor_sens
global app
global liveGraph
global run_test
global bmeT
global bmeH
global bmeP
#Initialization
x1 = []
x2 = []
x3 = []
x4 = []
x5 = []
x6 = []
monitor_sens = []
timeVector = []
bmeT = []
bmeH = []
bmeP = []
run_test = True

GPIO.setmode(GPIO.BCM)

###### COMPONENT SETUP ##############
#Setup of the Linear Actuator
class linearActuator():
    def __init__(self,pinNum):
        self.pinNum = pinNum
        GPIO.setup(self.pinNum,GPIO.OUT)
        self.pwm = GPIO.PWM(self.pinNum,50)
        self.pwm.start(9)
        self.state = 'recovery'
        print(self.state)

    def recover(self):
        if self.state != 'recovery':
            print("Moving to Recovery")
            self.pwm.ChangeDutyCycle(9)
            time.sleep(3)
            print("At Recovery")
            self.state = 'recovery'

        else:
            print("LA at Recovery")
            pass
    def expose(self):
        if self.state != 'exposure':
            print("Moving to Exposure")
            self.pwm.ChangeDutyCycle(5.36)
            time.sleep(2)
            print("At Exposure")
            self.state = 'exposure'

        else:
            print("LA at Exposure")
            pass

#Reads MOS Sensors Individually
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

# TODO: ADD BME and MAX Code
class bmeBox(QWidget):
    def __init__(self, bme, name):
        super(bmeBox,self).__init__()
        self.bme = bme
        self.name = name
        self.title = QLabel()
        self.pressure = QLabel()
        self.temperature = QLabel()
        self.humidity = QLabel()
        self.pageLayout = QGridLayout()
        self.title.setText(self.name)
        self.pressure.setText("Pressure: " + str(format(self.bme.read_pressure(), '.2f')))
        self.temperature.setText("Temperature: " + str(format(self.bme.read_temperature(), '.2f')))
        self.humidity.setText("Humidity: " + str(format(self.bme.read_humidity(), '.2f')))
        self.pageLayout.addWidget(self.title, 1,1)
        self.pageLayout.addWidget(self.pressure,2,1)
        self.pageLayout.addWidget(self.temperature,3,1)
        self.pageLayout.addWidget(self.humidity,4,1)
        self.setLayout(self.pageLayout)
    def update(self):
        self.pressure.setText("Pressure: " + str(format(self.bme.read_pressure(), '.2f')))
        self.temperature.setText("Temperature: " + str(format(self.bme.read_temperature(), '.2f')))
        self.humidity.setText("Humidity: " + str(format(self.bme.read_humidity(), '.2f')))


#Generates the Live Graph
#The Range of data is restricted to 200 s, and between 0 and 5 below
class live_Graph(pg.PlotWidget):
    def __init__(self,parent=None):
        super(live_Graph,self).__init__()
        #self.setAutoFillBackground(True)
        ## gets the total test time from parameter
        self.setRange(xRange=(0,250),yRange=(0,5),disableAutoRange=False)
        self.setTitle("Live Graph")
        self.setStyleSheet("pg.PlotWidget {border-style: outset; max-height: 50}")

class start_Button(QPushButton):
    def __init__(self,parent=None):
        super(start_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Start")
        self.clicked.connect(lambda: self.start_Procedure())

    def start_Procedure(self):
        #timeCheck = time.time()
        print("Starting Test")
        collect_data()

class resetButton(QPushButton):
    def __init__(self,parent=None):
        super(resetButton,self).__init__()


        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Reset")
        self.clicked.connect(lambda: self.reset_test())

    def reset_test():
        global timeVector
        global x1
        global x2
        global x3
        global x4
        global x5
        global x6
        global monitor_sens
        x1 = []
        x2 = []
        x3 = []
        x4 = []
        x5 = []
        x6 = []
        monitor_sens = []
        timeVector = []
        liveGraph.clear()

class linAc_exposeB(QPushButton):
    def __init__(self,linAc, parent=None):
        super(linAc_exposeB,self).__init__()
        self.linearActuator = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Expose")
        self.state = "recovery"
        self.clicked.connect(lambda: self.expose())

    def expose(self):
        if self.linearActuator.state == 'recovery':
            self.linearActuator.expose()
            self.linearActuator.state = 'exposure'

class linAc_recoverB(QPushButton):
    def __init__(self,linAc, parent=None):
        super(linAc_recoverB,self).__init__()
        self.linearActuator = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Recover")
        self.state = "exposure"
        self.clicked.connect(lambda: self.recover())

    def recover(self):
        if self.linearActuator.state == 'exposure':
            self.linearActuator.recover()
            self.linearActuator.state = 'recovery'

class start_Button(QPushButton):
    def __init__(self,parent=None):
        super(start_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Start")
        self.clicked.connect(lambda: self.start_Procedure())

    def start_Procedure(self):
        timeCheck = time.time()
        print("Starting Test")
        collect_data()

linAc = linearActuator(12)
sens1 = MOS(adc1,0)
sens2 = MOS(adc1,1)
sens3 = MOS(adc1,2)
sens4 = MOS(adc2,3)
sens5 = MOS(adc2,0)
sens6 = MOS(adc2,1)
monitor_sensor = MOS(adc2,2)

app = QApplication([])
app.setStyle('Fusion')
mainPage = QWidget()
mainPage.setWindowTitle("7 Sensor Setup")
mainPage.resize(800, 600)
liveGraph = live_Graph()
startB = start_Button()
linAc_exposeB = linAc_exposeB(linAc)
linAc_recoverB = linAc_recoverB(linAc)

pageLayout = QGridLayout()
pageLayout.addWidget(liveGraph)
pageLayout.addWidget(startB)
pageLayout.addWidget(linAc_exposeB)
pageLayout.addWidget(linAc_recoverB)
#pageLayout.addWidget(save_button)
mainPage.setLayout(pageLayout)
mainPage.show()
app.exec()
