### This setup is for the 7 sensor setup Version 1.2

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
#Initialization
x1 = []
x2 = []
x3 = []
x4 = []
x5 = []
x6 = []
monitor_sens = []
timeVector = []
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
            time.sleep(2)
            print("At Recovery")
            self.state = 'recovery'

        else:
            print("LA at Recovery")
            pass
    def expose(self):
        if self.state != 'exposure':
            print("Moving to Exposure")
            self.pwm.ChangeDutyCycle(5.5)
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

def collect_data():
    global linearActuator
    global app
    global timeVector
    global run_test
    t1 = time.time() #start time
    #t2 = sampling_time_index #imported from parameters
    #t3 = sampling_time #imported from parameters
    #t4 = sensor_expose_time #sensing delay time imported from parameters
    #t5 = sensor_retract_time #imported from parameters

    t2 = 1
    t3 = 0.1
    t4 = 5
    t5 = 42
    #Pre-test Settings
    if(linAc.state != 'recovery'):
        linAc.recover()

    while (run_test == True):
        app.processEvents()
        if(time.time() > t1+t3*t2):
            global x1
            global x2
            global x3
            global x4
            global x5
            global x6
            global monitor_sens

            # TODO: ADD BME and MAX Code

            x1.append(sens1.read())
            x2.append(sens2.read())
            x3.append(sens3.read())
            x4.append(sens4.read())
            x5.append(sens5.read())
            x6.append(sens6.read())
            monitor_sens.append(monitor_sensor.read())
            timeVector.append(time.time() - t1)
            # TODO: ADD BME and MAX Code
            if(time.time() % 5 == 0):
                update_Graph()

    combinedVector = np.column_stack((timeVector,x1,x2,x3,x4,x5,x6,monitor_sens))
    ## File Saving Parameters ##
    filePath = 'test_files/'
    testName = time.strftime('%a%d%b%Y%H%M',time.localtime())
    file_extension = '.csv'
    file_name = filePath + testName + file_extension
    np.savetxt(filename,combinedVector,fmt='10.f',delimiter=',')
    #File is Saved
    print('File ' + testName + ' saved')


    if (time.time() < t1+t4 and linAc.state != 'recovery'):
        linAc.recover()
    if (time.time() > t1+t4 and time.time() < t1+t5 and linAc.state != 'exposure'):
         linAc.expose()
    if (time.time > t1+t5 and linAc.state != 'recovery'):
        linAc.recover()

    else:
        pass

def update_Graph():
    global app
    global liveGraph
    global timeVector
    global x1
    global x2
    global x3
    global x4
    global x5
    global x6
    global monitor_sens
    liveGraph.clear()
    liveGraph.plot(timeVector, x1)
    liveGraph.plot(timeVector, x2)
    liveGraph.plot(timeVector, x3)
    liveGraph.plot(timeVector, x4)
    liveGraph.plot(timeVector, x5)
    liveGraph.plot(timeVector, x6)
    liveGraph.plot(timeVector, monitor_sens)
    app.processEvents()

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
            #self.setText("Click to Recover")
            #self.setIcon(self.green)
            self.linearActuator.state = 'exposure'

class linAc_recoverB(QPushButton):
    def __init__(self,linAc, parent=None):
        super(linAc_recoverB,self).__init__()
        self.linearActuator = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Recover")
        self.state = "expose"
        self.clicked.connect(lambda: self.recover())

    def recover(self):
        if self.linearActuator.state == 'exposure':
            self.linearActuator.recover()
            self.setText("Click to Expose")
            #self.setIcon(self.red)
            self.linearActuator.state = 'recovery'

# class baseline_measure(QPushButton):
#     def __init__(self,sens1,sens2,sens3,sens4,sens5,sens6, parent = None):
#         super(baseline_measure,self).init__()
#         self.sens1 = sens1
#         self.sens2 = sens2
#         self.sens3 = sens3
#         self.sens4 = sens4
#         self.sens5 = sens5
#         self.sens6 = sens6
#         self.setStyleSheet("QPushButton {font: 13px}")
#         self.setText("Check Baseline")
#         self.clicked.connect(lambda: self.baseline())
#
#     def baseline(self):
#         time_start = time.time()
#         s1 = []
#         s2 = []
#         s3 = []
#         s4 = []
#         s5 = []
#         s6 = []
#
#         while time.time() < time_start + 10):
#
#
#
#
# class baseline_measure(QPushButton):
#     def __init__(self,sens1,sens2,sens3,sens4,sens5,sens6, parent=None):
#         super(baseline_measure,self).__init__()
#         self.sens1 = sens1
#         self.sens2 = sens2
#         self.sens3 = sens3
#         self.sens4 = sens4
#         self.sens5 = sens5
#         self.sens6 = sens6
#         self.setStyleSheet("QPushButton {font: 13px}")
#         self.setText("Check Baseline")
#         self.clicked.connect(lambda: self.baseline())
#
#     def baseline(self):
#         time_start = time.time()
#         s1 = []
#         s2 = []
#         s3 = []
#         s4 = []
#         s5 = []
#         s6 = []
#         while(time.time() < time_start+10):
#             # Oh hey emily was here
#             s1.append(sens1.read())
#             s2.append(sens2.read())
#             s3.append(sens3.read())
#             s4.append(sens4.read())
#             s5.append(sens5.read())
#             s6.append(sens6.read())
#
#

# Initializing the MOS and Linear Actuator
# TODO: ADD the BME and MAX

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


class save_Button(QPushButton):
    def __init__(self,parent=None):
        super(save_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Save")
        self.clicked.connect(lambda: self.save())

    def save(self):
        global run_test
        run_test = False


class linAc_exposeButton(QPushButton):
    def __init__(self,linAc, parent=None):
        super(linAc_exposeButton,self).__init__()
        self.linearActuator = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Expose")
        self.state = "recovery"
        self.clicked.connect(lambda: self.expose())

    def expose(self):
        if self.linearActuator.state == 'recovery':
            self.linearActuator.expose()
            #self.setText("Click to Recover")
            #self.setIcon(self.green)
            self.linearActuator.state = 'exposure'

class linAc_recoverButton(QPushButton):
    def __init__(self,linAc, parent=None):
        super(linAc_recoverButton,self).__init__()
        self.linearActuator = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Recover")
        self.state = "expose"
        self.clicked.connect(lambda: self.recover())

    def recover(self):
        if self.linearActuator.state == 'exposure':
            self.linearActuator.recover()
            #self.setText("Recover")
            #self.setIcon(self.red)
            self.linearActuator.state = 'recovery'

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
linAc_exposeB = linAc_exposeButton(linAc)
linAc_recoverB = linAc_recoverButton(linAc)
save_button = save_Button()
pageLayout = QGridLayout()
pageLayout.addWidget(liveGraph)
pageLayout.addWidget(startB)
pageLayout.addWidget(linAc_exposeB)
pageLayout.addWidget(linAc_recoverB)
pageLayout.addWidget(save_button)
mainPage.setLayout(pageLayout)
mainPage.show()
app.exec()
