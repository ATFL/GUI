#!/usr/bin/python3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
import time
from mct_components import *
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ads
import numpy as np

dataVector = []
timeVector = []

global app
global stepper_motor
global mos_val
global printing
global liveGraph
global mos
global progress
global emergencyStop
global totalTime
global veryStartTime
veryStartTime = time.time()

totalTime = 600
emergencyStop = "RUN"

def update_Graph(xList, yList):
    global liveGraph
    global emergencyStop
    global app
    global veryStartTime
    global totalTime

    progress.setValue((time.time() - veryStartTime)/totalTime*100)
    liveGraph.plot(xList, yList)
    app.processEvents()

def pre_sensing_data():

def collect_data(xVector,yVector):

    global progress
    global app
    global emergencyStop
    global mos
    vaporization_time = 0.1 #normally 195
    sampling_time = 0.1 # DO NOT TOUCHtime between samples taken, determines sampling frequency
    sensing_delay_time = 1 # normally 1, time delay after beginning data acquisition till when the sensor is exposed to sample
    sensing_retract_time = 43 # normally 43, time allowed before sensor is retracted, no longer exposed to sample
    duration_of_signal = 200 # normally 200, time allowed for data acquisition per test run

    global printing
    baseline = 0
    printing.setText("Collecting Sample Data")
    print("Heating Done, data collection begins")
    heat_start_time = time.time()  # Local value. Capture the time at which the test began. All time values can use start_time as a reference
    dataVector = yVector
    timeVector = xVector
    dataVector.clear()
    timeVector.clear()
    dataVector = np.zeros(2000,1)
    sampling_time_index = 1
    app.processEvents()
    if emergencyStop == "STOP":
        return
    if linearAc.state != 'retracted':
        linearAc.retract()

    # Initial Heating Portion


    start_time = time.time()
    printing.setText("Starting Data Capture")
    print('Starting data capture.')
    while (time.time() < (start_time + duration_of_signal)) and (emergencyStop != "STOP"):# While time is less than duration of logged file
        #print("We are inside the while loop")
        progress.setValue((time.time()- start_time)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
        if (time.time() > (start_time + (sampling_time * sampling_time_index)) and (emergencyStop != "STOP")):  # if time since last sample is more than the sampling time, take another sample

            dataVector.append(mos.mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
            timeVector.append(time.time() - start_time)

            update_Graph(timeVector,dataVector)
            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        if (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (emergencyStop != "STOP")):
            print("we are in the 10-50 seconds loop")
            if linearAc.state != 'extended':
                linearAc.extend()

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        if (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (emergencyStop != "STOP"):
            print("Inside the first 10 seconds loop or last loop")
            if linearAc.state != 'retracted':
                linearAc.retract()

    if emergencyStop == "STOP":
        return
    print("Before the stack")
    dataVector[:] = [baseline - x  for x in dataVector]
    combinedVector = np.column_stack((timeVector, dataVector))
    print("Right before save")
##    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = time.strftime("/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/%a%d%b%Y%H%M%S.csv",time.localtime())
    #filename = "/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/EmilyTest.csv"
    print("after filename")
    np.savetxt(filename,combinedVector, fmt='%.10f', delimiter=',')
    print("File Saved")
    printing.setText("File Saved")

    pass

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')



## General Thoughts and Planning
# So the main thread should be the one that houses the actual processes (change linac, start pump etc)
# The worker thread should be the one that takes the plot data from the main thread during the data capture
# time and plots it on the graph. Another worker thread should consider how many points have been
# plotted and change the progress bar accordingly...
# Jk - threads suck, not using threads - instead we are using a bunch of global variables and forcing
# the app to recognize changes using app.processEvents()

class stepper_Button(QWidget):
    def __init__(self,syringePump, parent=None):
        super(stepper_Button, self).__init__()
        self.syringePump = syringePump
        self.layout = QVBoxLayout()
        self.title = QLabel("Syringe Pump")
        self.title.setStyleSheet("QLabel {font: 13px}")
        self.setStyleSheet("QSlider{max-height: 7px}")
        self.layout.addWidget(self.title)
        self.slider = QSlider(Qt.Horizontal)

        self.slider.setMinimum(0)
        self.slider.setMaximum(13)
        self.prevVal = 6
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(0.5)
        #self.setText("Linear Actuator")
        self.slider.setValue(6)
        self.slider.sliderReleased.connect(self.move_Stepper)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)
    def move_Stepper(self):
        self.number = self.slider.value()
        print(self.number)
        if self.prevVal < self.slider.value():
            i = self.slider.value() - self.prevVal
            while i > 0:
                self.syringePump.retract()
                i = i -1
            self.prevVal = self.slider.value()
        if self.prevVal > self.slider.value():
            i = self.prevVal - self.slider.value()
            while i > 0:
                self.syringePump.extend()
                i = i - 1
            self.prevVal = self.slider.value()


class mos_Button(QPushButton):
    def __init__(self,mos,parent=None):
        super(mos_Button, self).__init__()
        self.mos = mos
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Read MOS")
        self.clicked.connect(lambda: self.read_MOS())
    def read_MOS(self):
        #print("MOS Value: ")
        self.mos.print()
        global mos_val
        mos_val.setText("MOS: " + str(self.mos.read()))

class live_Graph(pg.PlotWidget):
    def __init__(self,parent=None):
        super(live_Graph,self).__init__()
        #self.setBackgroundColor(None)
        self.setRange(xRange=(0,200),yRange=(0,5),disableAutoRange=False)
        self.enableAutoScale()
        self.setTitle("Live Graph")
        self.setStyleSheet("pg.PlotWidget {border-style: outset; max-height: 50}")

class start_Button(QPushButton):
    def __init__(self,parent=None):
        super(start_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Start")
        self.clicked.connect(lambda: self.start_Procedure())
    def msgPress(self,i):
        if i.text() == "Yes":
            global stepperB
            stepperB.syringePump.spr = 1778
            stepperB.syringePump.step_count = stepperB.syringePump.spr*8
        elif i.text() == "No":
            global stepperB
            stepperB.syringePump.spr = 1600
            stepperB.syringePump.step_count = stepperB.syringePump.spr*8

    def start_Procedure(self):
        global emergencyStop
        emergencyStop = "RUN"

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("CLICK YES AFTER VAPORIZATION")
        msg.setWindowTitle("VAPORIZATION STATUS")
        msg.setStandardButtons(QMessageBox.Yes) | #QMessageBox.No
        retval = msg.exec_()

        veryStartTime = time.time()
        test_time  = time.time()
        global liveGraph
        liveGraph.clear()
        self.setEnabled(False)
        global app
        global printing
        global stepperB

        global liveGraph
        global mos
        mos.setEnabled(False)
        global progress
        progress.setValue(0)

        print("Starting Test...")

        global liveGraph
        while emergencyStop != "STOP":
            fill_chamber()
            print("Filling is done")
            app.processEvents()
            if emergencyStop == "STOP":
                break
            collect_data(timeVector, dataVector)
            app.processEvents()
            if emergencyStop == "STOP":
                break
            cleanse_chamber()
            app.processEvents()
            if emergencyStop == "STOP":
                break
            purge_system_raw()
            break


        global app

        global printing


        global stepperB

        global liveGraph
        global mos
        mos.setEnabled(True)
        global progress
        global printing
        printing.setText("Ready for testing")


class stop_Button(QPushButton):
    def __init__(self,parent=None):
        super(stop_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Stop")
        self.clicked.connect(lambda:self.stop_Procedure())
    def stop_Procedure(self):
        global emergencyStop
        emergencyStop = "STOP"
        print("Stopping Test...")

        global app

        global printing
        global stepperB
        global liveGraph
        global mos
        mos.setEnabled(True)


class print_Data(QLabel):
    def __init__(self,parent=None):
        super(print_Data,self).__init__()
        self.setText("Ready for Testing")

GPIO.setmode(GPIO.BCM)
# Linear Actuator
# Analog-Digital Converter
adc = ads.ADS1115(0x48)
GAIN = 2/3
#
# MOS Sensor
MOS_adc_channel = 0
mos1 = MOS(adc, MOS_adc_channel)



chamber_purge_time = 120 #normally 30 #Time to purge chamber: experiment with it

#########FILLING CHAMBER WITH TARGET GAS #############
# Filling Variables




#Stepper Motor Information
# Need to convert from BCM to BOARD
DIR = 25   # Direction GPIO Pin
STEP = 24  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1600   # Steps per Revolution (360 / 7.5)
SPR2 = 400
MODE = (15, 18, 23)   # Microstep Resolution GPIO Pins
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

Stepper_Motor = StepperMotor(DIR, STEP, CW, CCW, SPR, MODE, RESOLUTION)
Stepper_Motor2 = StepperMotor2(DIR,STEP,CW,CCW,SPR2,MODE,RESOLUTION)



## Main Page Initiation
app = QApplication([])
app.setStyle('Fusion')

print(QStyleFactory.keys())
mainPage = QTabWidget()
mainPage.setWindowTitle("MetroVan Sample Analysis")
mainPage.resize(600, 350)

## Data Page Initiation
firstPage = QWidget()
fpLayout = QGridLayout()
fpLayout.setVerticalSpacing(0)
liveGraph = live_Graph()
empty = QLabel("")
startB = start_Button()
stopB = stop_Button()
printing = print_Data()
progress = QtGui.QProgressBar()
fpLayout.addWidget(startB,4,1,1,2)
fpLayout.addWidget(stopB,4,3,1,2)
fpLayout.addWidget(printing,6,1,1,4)
fpLayout.addWidget(liveGraph,1,1,3,3)
fpLayout.addWidget(progress, 5,1,1,4)
firstPage.setLayout(fpLayout)

## Manual Controls Page Initiation
secondPage = QWidget()
spLayout = QGridLayout()
spLayout.setVerticalSpacing(0)


stepperB = stepper_Button(Stepper_Motor)
stepperB2 = stepper_Button(Stepper_Motor2)
mos = mos_Button(mos1)
mos_val = QLabel()
mos_val.setText("MOS: ")


spLayout.addWidget(stepperB2, 2,2)
spLayout.addWidget(mos,3,2)

spLayout.addWidget(mos_val,7,1)


secondPage.setLayout(spLayout)

mainPage.addTab(firstPage, "Sensor Response")
mainPage.addTab(secondPage, "Manual Controls")

mainPage.show()
app.exec_()

GPIO.cleanup()
