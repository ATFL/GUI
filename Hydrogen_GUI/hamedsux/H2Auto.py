#!/usr/bin/python3

#################### Documentation ####################
# Experiment Steps:
#       STEP 1: PURGE BOX::: V1:N V2:N V3:N V4:N V5:Y V6:Y
#       STEP 2: FILL METHANE P1::: V1:Y V2:N V3:Y V4:N V5:N V6:N
#       STEP 3: FILL METHANE P2::: V1:Y V2:N V3:N V4:Y V5:N V6:Y
#       STEP 4: FILL H2 P1::: V1:N V2:Y V3:Y V4:N V5:N V6:N
#       STEP 5: FILL H2 P2::: V1:N V2:Y V3:N V4:Y V5:N V6:Y
#       STEP 6: TEST::: V1:N V2:N V3:N V4:N V5:N V6:N

# To Do List:
    # Adapt valve status display
    # Write GUI


#################### Imports ####################

#>>>>> Pyqt5 Imports <<<<<
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
#>>>>> System Imports <<<<<
import random
import sys
from time import *
import time
import datetime
import os
import shutil
#>>>>> Rpi Imports <<<<<
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ads
import busio
import digitalio
import board
import numpy as np
import serial
from pathlib import Path



class LinearActuator:
    def __init__(self, LinActRetract,LinActExtend):
        self.LinActRetract = LinActRetract
        self.LinActExtend = LinActExtend
        self.extended_state = 3
        self.retracted_state = 1
        GPIO.setup(self.LinActRetract, GPIO.OUT)
        GPIO.setup(self.LinActExtend, GPIO.OUT)
        GPIO.output(self.LinActRetract, GPIO.LOW)
        GPIO.output(self.LinActExtend, GPIO.LOW)
        self.state = 'default'


    def extend(self):
        print('Extending linear actuator.')
        global positionSensor
        while (positionSensor.read() < self.extended_state):
            GPIO.output(LinActRetract, GPIO.LOW)
            GPIO.output(LinActExtend, GPIO.HIGH)
            print("i am looooopy")
        self.state = 'extended'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)
       

    def retract(self):
        global positionSensor
        print('Retracting linear actuator.')
        while (positionSensor.read() > self.retracted_state):
            GPIO.output(LinActRetract, GPIO.HIGH)
            GPIO.output(LinActExtend, GPIO.LOW)
        self.state = 'retracted'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)
    
#################### Global Objects ####################

#>>>>> Global Variables <<<<<
global test_counter #Counts tests completed. Initialized as 0.
global num_tests #Total number of tests to be completed. Set to number of gas concentrations to test.
dataVector = [] #Vector to store datapoints.
timeVector = [] #Vector to store timestamps corresponding to datapoints.
global continueTest

#>>>>>> Global Components <<<<<<
global adc
global linearActuator
global mos
global valve1
global valve2
global valve3
global valve4
global valve5
global valve6

#>>>>> Global GUI <<<<<<
global progressBar
global liveGraph
global processLabel
global LAIndicator

#################### Settings ####################

#>>>>> System Setup <<<<<

#Gas concentration settings
hydrogen_injection_conc = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
methane_injection_conc = [200,300,400,500,600,700,800,900,1000,50,150,250,350,450,550,650,750,850,950]

#Test counting settings
test_counter = 0
num_tests = len(methane_injection_conc)
continueTest = False

#Methane gas settings
fill_methane_time = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
methane_correction_factor = 0.72 #Found on MKS website.
methane_flow_factor = (60*2000*methane_correction_factor)/(10000000)

#Hydrogen gas settings
fill_hydrogen_time =  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
hydrogen_correction_factor = 1.01 #Found on MKS website.
hydrogen_flow_factor = (60*2000*hydrogen_correction_factor)/(10000000)

#Data recording settings
chamber_purge_time = 120 #Time to purge chamber. Normally 30.
sampling_time = 0.1 # DO NOT TOUCH. Time between samples taken, determines sampling frequency.
sensing_delay_time = 1 #Time delay after beginning data acquisition till when the sensor is exposed to sample. Normall 10,
sensing_retract_time =41  #Time allowed before sensor is retracted, no longer exposed to sample. Normally 40,
duration_of_signal = 200 #Total time per data recording. Normally 250
fill_line_clense_time = 0

for i in range(0, len(hydrogen_injection_conc)):
    fill_methane_time[i] = float(methane_injection_conc[i]*methane_flow_factor)
    fill_hydrogen_time[i] = float(hydrogen_injection_conc[i]*hydrogen_flow_factor)

print(fill_methane_time)
#################### System Functions ####################

def purge_system():
    global linearActuator
    global valve1
    global valve2
    global valve3
    global valve4
    # global valve5
    # global valve6

    global progressBar
    global processLabel
    global valve1Indicator
    global valve2Indicator
    global valve3Indicator
    global valve4Indicator
    global valve5Indicator
    global valve6Indicator
    global LAIndicator

    global continueTest

    processLabel.setText('Purging system...')
    progressBar.setMaximum(chamber_purge_time)

    app.processEvents()
    start_time = time.time()
    print("Purging System \n V1:N V2:N V3:N V4:N V5:Y V6:Y")
    while time.time() < (start_time + chamber_purge_time) and continueTest == True:
        if linearActuator.state != 'retracted':
            linearActuator.retract()
            LAIndicator.disable()
        if valve1.state != False:
            valve1.disable()
            valve1Indicator.disable()
        if valve2.state != False:
            valve2.disable()
            valve2Indicator.disable()
        if valve3.state != False:
            valve3.disable()
            valve3Indicator.disable()
        if valve4.state != False:
            valve4.disable()
            valve4Indicator.disable()
        if valve6.state != True:
            valve6.enable()
            valve6Indicator.enable()
        if valve5.state != True:
            valve5.enable()
            valve5Indicator.enable()
        progressBar.setValue(time.time() - start_time)
        app.processEvents()
    app.processEvents()
    print("Done purging \n V1:N V2:N V3:N V4:N V5:N V6:N")
    #Shutoff valves after completed purging.
    if linearActuator.state != 'retracted':
        linearActuator.retract()
        LAIndicator.disable()
    if valve1.state != False:
        valve1.disable()
        valve1Indicator.disable()
    if valve2.state != False:
        valve2.disable()
        valve2Indicator.disable()
    if valve3.state != False:
        valve3.disable()
        valve3Indicator.disable()
    if valve4.state != False:
        valve4.disable()
        valve4Indicator.disable()
    if valve5.state != False:
        valve5.disable()
        valve5Indicator.disable()
    if valve6.state != False:
        valve6.disable()
        valve6Indicator.disable()

    check(fill_chamber)
    pass


def fill_chamber():
    # global linearActuator
    # global valve1
    # global valve2
    # global valve3
    # global valve4
    # global valve5
    # global valve6

    global progressBar
    global processLabel
    global valve1Indicator
    global valve2Indicator
    global valve3Indicator
    global valve4Indicator
    global valve5Indicator
    global valve6Indicator
    global LAIndicator

    global continueTest

    processLabel.setText('Cleansing line(s)...')
    progressBar.setMaximum(fill_line_clense_time)

    #Methane and hydrogen fill line clensing.
    app.processEvents()
#    start_time = time.time()
#    print("Cleansing Line \n V1:N V2:N V3:Y V4:Y V5:N V6:N")
#    while time.time() < (start_time + fill_line_clense_time) and continueTest == True:
#        if valve1.state != False:
#            valve1.disable()
#            valve1Indicator.disable()
#        if valve2.state != False:
#            valve2.disable()
#            valve2Indicator.disable()
#        if valve3.state != True:
#            valve3.enable()
#            valve3Indicator.enable()
#        if valve4.state != True:
#            valve4.enable()
#            valve4Indicator.enable()
#        if valve5.state != False:
#            valve5.disable()
#            valve5Indicator.disable()
#        if valve6.state != False:
#            valve6.disable()
#            valve6Indicator.disable()
#        app.processEvents()
#        pass

    #Close all valves after cleansing line.
    if valve1.state != False:
        valve1.disable()
        valve1Indicator.disable()
    if valve2.state != False:
        valve2.disable()
        valve2Indicator.disable()
    if valve3.state != False:
        valve3.disable()
        valve3Indicator.disable()
    if valve4.state != False:
        valve4.disable()
        valve4Indicator.disable()
    if valve5.state != False:
        valve5.disable()
        valve5Indicator.disable()
    if valve6.state != False:
        valve6.disable()
        valve6Indicator.disable()

    app.processEvents()
    #Filling the hydrogen chamber.
    processLabel.setText('Filling the hydrogen chamber...')
    progressBar.setMaximum(fill_hydrogen_time[test_counter])
    start_time = time.time()
    print("Filling Chamber Hydrogen\n V1:Y V2:N V3:N V4:N V5:N V6:N")
    while time.time() < ( start_time + fill_hydrogen_time[test_counter]) and continueTest == True:
        if valve1.state != False:
            valve1.disable()
            valve1Indicator.disable()
        if valve2.state != True:
            valve2.enable()
            valve2Indicator.enable()
        if valve3.state != False:
            valve3.disable()
            valve3Indicator.disable()
        if valve4.state != False:
            valve4.disable()
            valve4Indicator.disable()
        if valve5.state != False:
            valve5.disable()
            valve5Indicator.disable()
        if valve6.state != False:
            valve6.disable()
            valve6Indicator.disable()
        progressBar.setValue(time.time() - start_time)
        app.processEvents()
        pass
    app.processEvents()
    #Filling the methane chamber.
    processLabel.setText('Filling the methane chamber...')
    progressBar.setMaximum(fill_hydrogen_time[test_counter])
    start_time = time.time()
    print("Hydrogen Closed, Methane Only\n V1:Y V2:N V3:N V4:N V5:N V6:N")
    print(fill_methane_time[test_counter ])
    while time.time() < ( start_time + fill_methane_time[test_counter ]) and continueTest == True:
        if valve1.state != True:
            valve1.enable()
            valve1Indicator.enable()
        if valve2.state != False:
            valve2.disable()
            valve2Indicator.disable()
        if valve3.state != False:
            valve3.disable()
            valve3Indicator.disable()
        if valve4.state != False:
            valve4.disable()
            valve4Indicator.disable()
        if valve5.state != False:
            valve5.disable()
            valve5Indicator.disable()
        if valve6.state != False:
            valve6.disable()
            valve6Indicator.disable()
        progressBar.setValue(time.time() - start_time)
        app.processEvents()
        pass
    app.processEvents()
    print("Done Filling Methane, both gases closed \n V1:N V2:N V3:N V4:N V5:N V6:N")

    check(collect_data)


def collect_data():
    global linearActuator
    global mos
    global valve1
    global valve2
    global valve3
    global valve4
    global valve5
    global valve6
    global liveGraph

    global progressBar
    global processLabel
    global valve1Indicator
    global valve2Indicator
    global valve3Indicator
    global valve4Indicator
    global valve5Indicator
    global valve6Indicator
    global LAIndicator

    global continueTest

    processLabel.setText('Collecting data...')
    progressBar.setMaximum(duration_of_signal)
    app.processEvents()
    start_time = time.time()  # Local value. Capture the time at which the test began. All time values can use start_time as a reference
    global test_counter
    global dataVector
    global timeVector
    dataVector.clear()
    timeVector.clear()
    update_Graph(timeVector,dataVector)
    sampling_time_index = 1

    # Initial state checks
    if linearActuator.state != 'retracted':
        linearActuator.retract()
        LAIndicator.disable()
    if valve1.state != False:
        valve1.disable()
        valve1Indicator.disable()
    if valve2.state != False:
        valve2.disable()
        valve2Indicator.disable()
    if valve3.state != False:
        valve3.disable()
        valve3Indicator.disable()
    if valve4.state != False:
        valve4.disable()
        valve4Indicator.disable()
    if valve5.state != False:
        valve5.disable()
        valve5Indicator.disable()
    if valve6.state != False:
        valve6.disable()
        valve6Indicator.disable()

    app.processEvents()
    start_time = time.time()
    print('Starting data capture.')
    while (time.time() < (start_time + duration_of_signal)) and (continueTest == True):  #While time is less than duration of logged file
        if (time.time() > (start_time + (sampling_time * sampling_time_index)) and (continueTest == True)):  # if time since last sample is more than the sampling time, take another sample
            dataVector.append(mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
            timeVector.append(time.time() - start_time)

            update_Graph(timeVector,dataVector)

            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        if (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (continueTest == True)):
            print(linearActuator.state) 
            if linearActuator.state != 'extended':
                linearActuator.extend()
                LAIndicator.enable()
                print("The linear actuator should be extended")

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        if (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (continueTest == True):
            if linearActuator.state != 'retracted':
                linearActuator.retract()
                LAIndicator.disable()
                print("The linear actuator should be retracted")

        progressBar.setValue(time.time() - start_time)
        app.processEvents()
    app.processEvents()
    time_len = len(timeVector)
    methConc_array = np.ndarray(shape=(time_len,1))
    methConc_array.fill(methane_injection_conc[test_counter])
    H2Conc_array = np.ndarray(shape=(time_len,1))
    H2Conc_array.fill(hydrogen_injection_conc[test_counter])
    combinedVector = np.column_stack((timeVector, dataVector,methConc_array,H2Conc_array))

    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = time.strftime("%a%d%b%Y%H%M%S",time.localtime()) + "H" + str(hydrogen_injection_conc[test_counter]) + "M" + str(methane_injection_conc[test_counter]) + ".csv"
    np.savetxt(r'/home/pi/Desktop/H2Auto_Data/'+filename, combinedVector, fmt='%.10f', delimiter=',')
    print("Test ",test_counter + 1," File Saved")
    app.processEvents()

    test_counter += 1
    check(multi_test_run) #Evaluate if the test loop continues.
    pass

def multi_test_run():
    global num_tests
    #num_tests = len(methane_injection_conc)
    global test_counter
    if test_counter < num_tests:
        purge_system()
        pass
    else:
        global continueTest
        continueTest = False #Set the test flag to false, stops testing.
        print(num_tests," Tests Completed")

def check(next_procedure):
    global continueTest
    if continueTest == True:
        next = next_procedure()
        return next
    elif continueTest == False:
        pass
    pass


def update_Graph(xList,yList):
    global liveGraph

    liveGraph.plot(xList,yList)
    app.processEvents()



#################### Classes ####################

class PositionSensor():
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
        print("\nReading from Linear Actuator Position Sensor: {}".format(self.conversion_value))


class LinearActuator:
    def __init__(self, LinActRetract,LinActExtend):
        self.LinActRetract = LinActRetract
        self.LinActExtend = LinActExtend
        self.extended_state = 3.9
        self.retracted_state = 1.2
        GPIO.setup(self.LinActRetract, GPIO.OUT)
        GPIO.setup(self.LinActExtend, GPIO.OUT)
        GPIO.output(self.LinActRetract, GPIO.LOW)
        GPIO.output(self.LinActExtend, GPIO.LOW)
        self.state = 'default'

    def extend(self):
        print('Extending linear actuator.')
        global positionSensor
        while (positionSensor.read() < self.extended_state):
            GPIO.output(LinActRetract, GPIO.LOW)
            GPIO.output(LinActExtend, GPIO.HIGH)
            print('Send help.')
        self.state = 'extended'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)

    def retract(self):
        print('Retracting linear actuator.')
        global positionSensor
        while (positionSensor.read() > self.retracted_state):
            GPIO.output(LinActRetract, GPIO.HIGH)
            GPIO.output(LinActExtend, GPIO.LOW)
        self.state = 'retracted'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)

class Valve:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def switch(self):
        if self.state == False:
            self.enable()
        elif self.state == True:
            self.disable()

    def enable(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True
        print(self.name + ' enabled.')
        #print("GPIO.LOW")

    def disable(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False
        print(self.name + ' disabled.')

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


#>>>>> System Components <<<<<

GPIO.setmode(GPIO.BCM)

#Analog-Digital Converter
adc = ads.ADS1115(0x48) #This has to come before sensor intitializations.

#Linear actuator
LinActRetract = 22 #Board 15; BCM 22
LinActExtend = 27 #Board 13; BCM 27
linearActuator = LinearActuator(LinActRetract,LinActExtend)

#Position sensor
Lin_act_position_channel = 2
positionSensor = PositionSensor(adc, Lin_act_position_channel)

#MOS Sensor
MOS_adc_channel = 0
mos = MOS(adc, MOS_adc_channel)

#Valves
pinvalve1 = 18  #Board 12; BCM 18.
pinvalve2 = 25  #Board 22; BCM 25.
pinvalve3 = 23  #Board 16; BCM 23.
pinvalve4 = 24  #Board 18; BCM 24.
pinvalve5 = 16  #Board 36; BCM 16.
pinvalve6 = 21  #Board 40; BCM 21.
valve1 = Valve('Valve 1',pinvalve1) #Methane Tank to MFC
valve2 = Valve('Valve 2',pinvalve2) #H2 Tank to MFC
valve3 = Valve('Valve 3',pinvalve3) #Line Venting
valve4 = Valve('Valve 4',pinvalve4) #Sample Gas into Chamber
valve5 = Valve('Valve 5',pinvalve5) #Air into Chamber
valve6 = Valve('Valve 6',pinvalve6) #Chamber Exhaust


#################### GUI ####################

class live_Graph(pg.PlotWidget):
    def __init__(self,parent=None):
        super(live_Graph,self).__init__()
        #self.setBackgroundColor(None)
        self.setRange(xRange=(0,200),yRange=(0,5),disableAutoRange=False)
        self.enableAutoScale()
        self.setTitle("Live Graph")
        self.setStyleSheet("pg.PlotWidget {border-style: outset; max-height: 50}")

class ValveButton(QtWidgets.QPushButton):
    def __init__(self,valve,indicator,parent=None):
        super(ValveButton,self).__init__()
        self.valve = valve
        self.indicator = indicator
        self.setText(self.valve.name)
        self.clicked.connect(lambda: self.switch_state())

    def switch_state(self):
        self.valve.switch()
        self.indicator.switch()

class LinActExtendButton(QtWidgets.QPushButton):
    def __init__(self,linearActuator,indicator,parent=None):
        super(LinActExtendButton,self).__init__()
        self.linearActuator = linearActuator
        self.indicator = indicator
        self.setText('Extend linear actuator')
        self.clicked.connect(lambda: self.extend_LA())

    def extend_LA(self):
        if self.linearActuator.state != 'extended':
            self.linearActuator.extend()
            self.indicator.enable()
        else:
            print('Linear actuator already extended.')
            pass


class LinActRetractButton(QtWidgets.QPushButton):
    def __init__(self,linearActuator,indicator,parent=None):
        super(LinActRetractButton,self).__init__()
        self.linearActuator = linearActuator
        self.indicator = indicator
        self.setText('Retract linear actuator')
        self.clicked.connect(lambda: self.retract_LA())

    def retract_LA(self):
        if self.linearActuator.state != 'retracted':
            self.linearActuator.retract()
            self.indicator.disable()
        else:
            print('Linear actuator already retracted.')
            pass


class MOSButton(QtWidgets.QPushButton):
    def __init__(self,mos,parent=None):
        super(MOSButton,self).__init__()
        self.mos = mos
        self.setText('Print MOS')
        self.clicked.connect(lambda: self.switch_state())

    def switch_state(self):
        self.mos.print()

class MainButton(QtWidgets.QPushButton):
    def __init__(self,parent=None):
        super(MainButton,self).__init__()
        self.state = False
        self.setText('Run')
        self.clicked.connect(lambda: self.switch_state())

    def switch_state(self):
        global continueTest
        if self.state == False:
            continueTest = True
            print('Test starting.')
            self.setText('Stop')
            self.state = True
            purge_system()
        elif self.state == True:
            self.setText('Run')
            self.state = False
            continueTest = False
            print('Test stopping.')


class Indicator(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(Indicator, self).__init__()
        # self.setScaledContents(True)
        self.onPix = QtGui.QPixmap("/home/pi/Desktop/LEDon.png")
        self.offPix = QtGui.QPixmap("/home/pi/Desktop/LEDoff.png")
        self.setPixmap(self.offPix)
        self.state = False

    def switch(self):
        if self.state == False:
            self.setPixmap(self.onPix)
            self.state = True
            app.processEvents()
        if self.state == True:
            self.setPixmap(self.offPix)
            self.state = False
            app.processEvents()

    def enable(self):
        self.setPixmap(self.onPix)

    def disable(self):
        self.setPixmap(self.offPix)

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.winId()))])
        self.setFixedSize(640, 480)


class H2Auto_GUI(object):
    def setupUi(self, MainWindow):
        #Setup GUI Framework
        MainWindow.setObjectName("H2Auto")

        self.centralwidget = QtWidgets.QTabWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        #Global stuff
        global liveGraph
        global progressBar
        global processLabel
        global valve1
        global valve2
        global valve3
        global valve4
        global valve5
        global valve6
        global linearActuator
        global mos
        global valve1Indicator
        global valve2Indicator
        global valve3Indicator
        global valve4Indicator
        global valve5Indicator
        global valve6Indicator
        global LAIndicator

        #First page
        self.page1 = QtWidgets.QWidget()
        self.p1Layout = QtWidgets.QGridLayout() #Defines layout format.
        self.p1Layout.setSpacing(10)
        #Create first page objects
        liveGraph = live_Graph()
        progressBar = QtWidgets.QProgressBar()
        processLabel = QtWidgets.QLabel()
        processLabel.setText('Ready for testing.')
        processLabel.setAlignment(QtCore.Qt.AlignVCenter)
        valve1Label = QtWidgets.QLabel()
        valve2Label = QtWidgets.QLabel()
        valve3Label = QtWidgets.QLabel()
        valve4Label = QtWidgets.QLabel()
        valve5Label = QtWidgets.QLabel()
        valve6Label = QtWidgets.QLabel()
        LALabel = QtWidgets.QLabel()
        valve1Label.setText('Valve 1')
        valve2Label.setText('Valve 2')
        valve3Label.setText('Valve 3')
        valve4Label.setText('Valve 4')
        valve5Label.setText('Valve 5')
        valve6Label.setText('Valve 6')
        LALabel.setText('Lin Act')
        valve1Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        valve2Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        valve3Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        valve4Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        valve5Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        valve6Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        LALabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        valve1Indicator = Indicator()
        valve2Indicator = Indicator()
        valve3Indicator = Indicator()
        valve4Indicator = Indicator()
        valve5Indicator = Indicator()
        valve6Indicator = Indicator()
        LAIndicator = Indicator()
        mainButton = MainButton()
        #Add objects to first page layout
        self.p1Layout.addWidget(liveGraph,0,0,7,5) #0075
        self.p1Layout.addWidget(processLabel,6,0,7,1) #6071
        self.p1Layout.addWidget(progressBar,8,0,9,1) #8071
        self.p1Layout.addWidget(valve1Label,0,8,1,1) #0811
        self.p1Layout.addWidget(valve2Label,1,8,1,1) #1811
        self.p1Layout.addWidget(valve3Label,2,8,1,1) #2811
        self.p1Layout.addWidget(valve4Label,3,8,1,1) #3811
        self.p1Layout.addWidget(valve5Label,4,8,1,1) #4811
        self.p1Layout.addWidget(valve6Label,5,8,1,1) #5811
        self.p1Layout.addWidget(LALabel,6,8,1,1) #6811
        self.p1Layout.addWidget(valve1Indicator,0,9,1,1) #0911
        self.p1Layout.addWidget(valve2Indicator,1,9,1,1) #1911
        self.p1Layout.addWidget(valve3Indicator,2,9,1,1) #2911
        self.p1Layout.addWidget(valve4Indicator,3,9,1,1) #3911
        self.p1Layout.addWidget(valve5Indicator,4,9,1,1) #4911
        self.p1Layout.addWidget(valve6Indicator,5,9,1,1) #5911
        self.p1Layout.addWidget(LAIndicator,6,9,1,1) #6911
        self.p1Layout.addWidget(mainButton,7,8,2,2)
        self.page1.setLayout(self.p1Layout)

        #Second page
        self.page2 = QtWidgets.QWidget()
        self.p2Layout = QtWidgets.QGridLayout() #Defines layout format.
        self.p2Layout.setVerticalSpacing(0)
        #Create second page Objects
        valve1Button = ValveButton(valve1,valve1Indicator)
        valve2Button = ValveButton(valve2,valve2Indicator)
        valve3Button = ValveButton(valve3,valve3Indicator)
        valve4Button = ValveButton(valve4,valve4Indicator)
        valve5Button = ValveButton(valve5,valve5Indicator)
        valve6Button = ValveButton(valve6,valve6Indicator)
        extendLAButton = LinActExtendButton(linearActuator,LAIndicator)
        retractLAButton = LinActRetractButton(linearActuator,LAIndicator)
        printMOSButtion = MOSButton(mos)
        #Add objects to second page layout
        self.p2Layout.addWidget(valve1Button)
        self.p2Layout.addWidget(valve2Button)
        self.p2Layout.addWidget(valve3Button)
        self.p2Layout.addWidget(valve4Button)
        self.p2Layout.addWidget(valve5Button)
        self.p2Layout.addWidget(valve6Button)
        self.p2Layout.addWidget(extendLAButton)
        self.p2Layout.addWidget(retractLAButton)
        self.p2Layout.addWidget(printMOSButtion)
        self.page2.setLayout(self.p2Layout)

        #Add pages to tab system
        self.centralwidget.addTab(self.page1,'Monitor')
        self.centralwidget.addTab(self.page2,'Settings')

        MainWindow.resize(800, 480)

try:
    if __name__ == "__main__": #Executes if this file is the source file. Does not run if imported.
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        MainWindow.setWindowTitle('H\u00b2Auto')
        ui = H2Auto_GUI()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
except keyboardinterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
    print('GPIO cleaned up properly.')
