#!/usr/bin/python3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
#import sys
import time
#import datetime
from Metrovan_components import *
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ads
#import busio
#import adafruit_bme280
#import digitalio
#import adafruit_max31855
#import board
import numpy as np

dataVector = []
timeVector = []
fill_line_clense_time = 20  #normally 20
global H2s_detected
global H2s_notdetected
global H2s_undefined
global are_maching_learning
are_machine_learning = "NO"
global app
global stepperB2
global cb
global purgeB
global v1
global v2
global v3
global v4
global v5
global v6
global mos_val
global pumpB
global heaterB
global printing
global linearAc
global stepperB
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

def purge_system_raw():
    start_time = time.time()
    global printing
    printing.setText("Purging System")
    print("Purging System")
    global v1
    global v2
    global v3
    global v4
    global v5
    global v6
    global pumpB
    global linearAc
    global veryStartTime
    global progress
    global app
    global emergencyStop

    if v1.valve.state != True:
        v1.enable()
    if v2.valve.state != True:
        v2.enable()
    if v5.valve.state != True:
        v5.enable()
    if v6.valve.state != True:
        v6.enable()
    linearAc.retract()
    pumpB.enable()
    app.processEvents()
    if emergencyStop == "STOP":
        return
    while time.time() < (start_time + chamber_purge_time):
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
        # wait patiently for the purging to be finished
    app.processEvents()
    if emergencyStop == "STOP":
            return
    pumpB.disable()
    if v1.valve.state != False:
        v1.disable()
    if v2.valve.state != False:
        v2.disable()
    if v5.valve.state != False:
        v5.disable()
    if v6.valve.state != True:
        v6.enable()
    printing.setText("Done Purging")
    print("Done purging")

def fill_chamber():
    global heaterB
    global linearAc
    global v1
    global v2
    global v3
    global v4
    global v5
    global v6
    global stepperB
    global progress
    global app
    global veryStartTime
    global totalTime
    global printing
    printing.setText("Filling Chamber")
    print("filling chamber")
    global heaterB
    heaterB.heat()
    if linearAc.state != 'retracted':
        linearAc.retract()
    #########FILL H2S ############

    # Filling the chamber
    app.processEvents()
    if emergencyStop == "STOP":
            return
    stepperMotorRT= 10  # Time it takes for the stepper motor to fully complete the retraction process
    stepperMotorET = 10 # Time it takes for the stepper motor to fully complete the extension process
    print("Filling Chamber")
    if v1.valve.state != True:
        v1.enable()
    if v2.valve.state != True:
        v2.enable()
    if v3.valve.state != True:
        v3.enable()
    if v4.valve.state != False:
        v4.disable()
    if v5.valve.state != True:
        v5.enable()
    app.processEvents()
    if emergencyStop =="STOP":
            return
    start_time = time.time()
    stepperB.syringePump.retract()
   # print("Everything is not fine")
    while (time.time() - start_time < stepperMotorRT):
        global progress
        global veryStartTime
        global totalTime
        progress.setValue((time.time()-veryStartTime)/totalTime*100)
       # print("Some things are fine")
        app.processEvents()
        if emergencyStop == "STOP":
            break
            # wait patiently for the Stepper Motor to finish retracting
    if emergencyStop == "STOP":
         return
   # print("Everything is fine")
    if v3.valve.state != False:
        v3.disable()

    start_time = time.time()
    stepperB.syringePump.extend()
    while (time.time() - start_time < stepperMotorRT):
     #   print("I am lost")
        global progress
        global veryStartTime
        global totalTime
        global app
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
            # wait patiently fo  r the Stepper Motor to finish retracting
       # print("End of fill")
    if emergencyStop == "STOP":
        return
def cleanse_chamber():
    print("Beginning of cleanse")
    global heaterB
    global v1
    global v2
    global v3
    global v4
    global v5
    global v6
    global pumpB
    pumpB.disable()
    global linearAc
    global progress
    global app
    global emergencyStop
    start_time = time.time()
    app.processEvents()
    if emergencyStop =="STOP":
        return
    heaterB.heat()
    stepperMotorRT= 7  # Time it takes for the stepper motor to fully complete the retraction process
    stepperMotorET = 7 # Time it takes for the stepper motor to fully complete the extension process
    global printing
    printing.setText("Cleansing lines")
    print("Cleansing lines")
    CCT = 3 # The number of times you repeat the stepper motor cycle
    if v1.valve.state != False:
        v1.disable()
    if v2.valve.state != False:
        v2.disable()
    if v3.valve.state != False:
        v3.disable()
    if v4.valve.state != True:
        v4.enable()
    if v5.valve.state != False:
        v5.disable()
    heaterB.heat()
    cleanse_time = 5
    start_time = time.time()
    pumpB.enable()
    while (time.time() - start_time < cleanse_time):
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    if v4.valve.state != False:
        v4.disable()
    start_time = time.time()
    cleanse_time = 1
    while(time.time() - start_time < cleanse_time):
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    if v4.valve.state != True:
        v4.enable()
    pumpB.disable()
    if v3.valve.state!= True:
        v3.enable()
    if v2.valve.state!= True:
        v2.enable()

    start_time = time.time()
    global stepperB2
    stepperB2.syringePump.retract()
    while (time.time() - start_time < stepperMotorRT):

        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        # wait patiently for the Stepper Motor to finish retracting
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return

    if v3.valve.state !=False:
        v3.disable()
    start_time = time.time()
    stepperB2.syringePump.extend()
    while (time.time() - start_time < stepperMotorET):
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
            # wait patiently for the Stepper Motor to finish extending
    if emergencyStop == "STOP":
        return
    if v2.valve.state != False:
        v2.disable()
    pumpB.enable()
    start_time = time.time()
    cleanse_time = 2
    while(time.time() - start_time < cleanse_time):
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    pumpB.disable()
    start_time = time.time()
    ## EMILY CHANGED HEAT TIME (normally 20)
    heat_time = 20
    while time.time() - start_time < heat_time:
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    heaterB.cool()
    if v1.valve.state != True:
        v1.enable()

def collect_data(xVector,yVector):
    global heaterB
    global linearAc
    global progress
    global app
    global emergencyStop
    global mos
    vaporization_time = 195 #normally 195
    sampling_time = 0.1 # DO NOT TOUCHtime between samples taken, determines sampling frequency
    sensing_delay_time = 1 # normally 1, time delay after beginning data acquisition till when the sensor is exposed to sample
    sensing_retract_time = 43 # normally 43, time allowed before sensor is retracted, no longer exposed to sample
    duration_of_signal = 200 # normally 200, time allowed for data acquisition per test run

    global printing
    baseline = 5.106
    printing.setText("Heating up Sample")
    print("Data collection begins")
    heat_start_time = time.time()  # Local value. Capture the time at which the test began. All time values can use start_time as a reference
    dataVector = yVector
    timeVector = xVector
    dataVector.clear()
    timeVector.clear()
    sampling_time_index = 1
    app.processEvents()
    if emergencyStop == "STOP":
        return
    heaterB.heat()
    if linearAc.state != 'retracted':
        linearAc.retract()

    # Initial Heating Portion
    while (time.time() - heat_start_time < vaporization_time):#Vaporization time
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
       return

    start_time = time.time()
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
            dataVector.append(baseline - mos.mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
            timeVector.append(time.time() - start_time)
           # print(*dataVector)
           # print("Before calling update Graph")
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

        # Otherwise, keep outputs off
##        else:
##            if linearAc.state != 'retracted':
##                linearAc.retract()

##    dataVector[:] = [x * (-1) for x in dataVector]
    #dataVector[:] = [baseline - x  for x in dataVector]
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
    heaterB.cool()



## General Thoughts and Planning
# So the main thread should be the one that houses the actual processes (change linac, start pump etc)
# The worker thread should be the one that takes the plot data from the main thread during the data capture
# time and plots it on the graph. Another worker thread should consider how many points have been
# plotted and change the progress bar accordingly...
# Jk - threads suck, not using threads - instead we are using a bunch of global variables and forcing
# the app to recognize changes using app.processEvents()

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
## GUI Functions

## Global Variable Initialization


class heater_Button(QPushButton):
    def __init__(self, heater, parent=None):
        super(heater_Button, self).__init__()
        self.heater = heater
        self.heater.cool()
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px; max-height: 20px}")
        # Must be changed if working on Raspberry Pi or personal Laptop
        self.green = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/on.svg")
        # Must be changed if working on Raspberry Pi or personal laptop
        self.red = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/off.svg")
        self.setIcon(self.red)
        self.setText("Heater Off")
        self.state = "off"
        self.clicked.connect(lambda: self.heater_Switch())

    def heater_Switch(self):
        if self.state == "off":
            self.setIcon(self.green)
            self.setText("Heater On")
            self.state = "on"
            self.heater.heat()
        elif self.state == "on":
            self.setIcon(self.red)
            self.setText("Heater Off")
            self.state = "off"
            self.heater.cool()
    def heat(self):
        if self.state != "on":
            self.heater.heat()
            self.setIcon(self.green)
            self.setText("Heater On")
            self.state = "on"
            global app
            app.processEvents()
    def cool(self):
        if self.state != "off":
            self.heater.cool()
            self.setIcon(self.red)
            self.setText("Heater Off")
            self.state = "off"
            global app
            app.processEvents()

class valve_Button(QPushButton):
    def __init__(self, num,schematic,valve, parent=None):
        super(valve_Button, self).__init__()
        self.valve = valve
        self.valve.disable()
        self.setText("Valve "+ str(num) + " Mode")
        self.state = "A"
        self.schematic = schematic
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px}")
        # Must be changed if working on Raspberry Pi or personal Laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        self.A = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/A.svg")
        self.B = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/B.svg")
        self.setIcon(self.A)
        self.clicked.connect(lambda: self.valve_Switch())
    def valve_Switch(self):
        if self.state == "A":
            self.setIcon(self.B)
            self.valve.enable()
            self.state = "B"
            self.schematic.valve_Flip()
        elif self.state == "B":
            self.setIcon(self.A)
            self.valve.disable()
            self.state = "A"
            self.schematic.valve_Flip()
    def enable(self):
        self.state = "B"
        self.setIcon(self.B)
        self.valve.enable()
        self.schematic.valve_Flip()
    def disable(self):
        self.state = "A"
        self.setIcon(self.A)
        self.valve.disable()
        self.schematic.valve_Flip()

class pump_Button(QPushButton):
    def __init__(self, pump, parent=None):
        super(pump_Button, self).__init__()
        self.setIconSize(QSize(15,15))
        self.pump = pump
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Pump Off")
        self.state = "off"
        # Must be changed if working on Raspberry pi or personal laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        self.green = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/on.svg")
        self.red = QtGui.QIcon("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/off.svg")
        self.setIcon(self.red)
        self.clicked.connect(lambda: self.pump_Switch())
    def pump_Switch(self):
        if self.state == "off":
            self.pump.enable()
            self.setIcon(self.green)
            self.setText("Pump On")
            self.state = "on"
        elif self.state == "on":
            self.pump.disable()
            self.setIcon(self.red)
            self.setText("Pump Off")
            self.state = "off"
    def enable(self):
        if self.state == "off":
            self.pump.enable()
            self.setText("Pump On")
            self.setIcon(self.green)
            self.state = "on"
    def disable(self):
        if self.state == "on":
            self.pump.disable()
            self.setText("Pump Off")
            self.setIcon(self.red)
            self.state = "off"
class linAc_Button(QWidget):
    def __init__(self, linearAc, parent=None):
        super(linAc_Button, self).__init__(parent)
        self.linearAc = linearAc
        self.state = "default"

        self.layout = QVBoxLayout()
        self.title = QLabel("Linear Actuator")
        self.title.setStyleSheet("QLabel {font: 13px}")
        self.setStyleSheet("QSlider{max-height: 7px}")
        self.layout.addWidget(self.title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(5.8)
        self.slider.setMaximum(10.8)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        #self.setText("Linear Actuator")
        self.slider.setValue(7.8)
        self.slider.sliderReleased.connect(self.move_Actuator)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)
    def move_Actuator(self):
        self.number = self.slider.value()
        print(self.number)
        self.linearAc.variableMove(self.number)
    def retract(self):
        self.linearAc.retract()
        self.state = "retracted"
    def extend(self):
        self.linearAc.extend()
        self.state = "extended"

class schematic(QLabel):
    def __init__(self, firstIm, secondIm, parent=None):
        super(schematic, self).__init__()
        self.firstIm = firstIm
        self.secondIm = secondIm
        self.setScaledContents(True)
        self.schematic1 = QPixmap(self.firstIm)
        self.schematic2 = QPixmap(self.secondIm)
        self.setPixmap(self.schematic1)
        self.state = "A"
        print(self.state)

    def valve_Flip(self):
        if self.state == "A":
            self.setPixmap(self.schematic2)
            self.state = "B"
        elif self.state == "B":
            self.setPixmap(self.schematic1)
            self.state = "A"

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

class cleanse_Button(QPushButton):
    def __init__(self, parent=None):
        super(cleanse_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Cleanse Lines")
        self.clicked.connect(lambda: self.cleanse_Lines())
    def cleanse_Lines(self):
        global emergencyStop
        print("Cleaning Lines")
        cleanse_chamber()
class purge_Button(QPushButton):
    def __init__(self,parent=None):
        super(purge_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Purge Chamber")
        self.clicked.connect(lambda: self.purge_Chamber())
    def purge_Chamber(self):
        global emergencyStop
        print("Purging Chamber")
        purge_system_raw()

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
        msg.setText("Are you using a filter to remove sediment?")
        msg.setWindowTitle("Filter Settings")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()
        if retval == QtGui.QMessageBox.Yes:
            global stepperB
            stepperB.syringePump.spr = 1778
            stepperB.syringePump.step_count = stepperB.syringePump.spr*8
        elif retval == QtGui.QMessageBox.No:
            global stepperB
            stepperB.syringePump.spr = 1600
            stepperB.syringePump.step_count = stepperB.syringePump.spr*8

        print(stepperB.syringePump.spr)
        veryStartTime = time.time()
        test_time  = time.time()
        global H2s_undefined
        H2s_undefined.setStyleSheet("QLabel {font:13px; border: 2px solid light gray; color: gray}")
        global liveGraph
        liveGraph.clear()
        self.setEnabled(False)
        global cb
        cb.setEnabled(False)
        global purgeB
        purgeB.setEnabled(False)
        global v1
        v1.setEnabled(False)
        global v2
        v2.setEnabled(False)
        global v3
        v3.setEnabled(False)
        global v4
        v4.setEnabled(False)
        global v5
        v5.setEnabled(False)
        global v6
        v6.setEnabled(False)
        global app
        global pumpB
        pumpB.setEnabled(False)
        global heaterB
        heaterB.setEnabled(False)
        global printing
        global linearAc

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

        global are_machine_learning
        if are_machine_learning == "NO":
            global H2s_undefined
            H2s_undefined.setStyleSheet("QLabel {font:13px; border: 2px solid black; background-color: orange}")
        self.setEnabled(True)
        global v1
        v1.setEnabled(True)
        global v2
        v2.setEnabled(True)
        global v3
        v3.setEnabled(True)
        global v4
        v4.setEnabled(True)
        global v5
        v5.setEnabled(True)
        global v6
        v6.setEnabled(True)
        cb.setEnabled(True)
        purgeB.setEnabled(True)
        global app
        global pumpB
        pumpB.setEnabled(True)
        global heaterB
        heaterB.setEnabled(True)
        global printing
        global linearAc

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
        global v1
        v1.setEnabled(True)
        v1.disable()
        global v2
        v2.setEnabled(True)
        v2.disable()
        global v3
        v3.setEnabled(True)
        v3.disable()
        global v4
        v4.setEnabled(True)
        v4.disable()
        global v5
        v5.setEnabled(True)
        v5.disable()
        global v6
        v6.setEnabled(True)
        v6.valve.disable()
        global app
        global pumpB
        pumpB.setEnabled(True)
        pumpB.disable()
        global heaterB
        heaterB.setEnabled(True)
        heaterB.cool()
        global printing
        global linearAc

        global stepperB

        global liveGraph
        global mos
        mos.setEnabled(True)



class print_Data(QLabel):
    def __init__(self,parent=None):
        super(print_Data,self).__init__()
        self.setText("Ready for Testing")

class print_Garbage(): # This is designed to test the success of the multithreading functionality
    def __init__(self,parent=None):
        super(print_Garbage,self).__init__()
        count = True
        global emergencyStop
        while (count == True) & (emergencyStop != "STOP"):
            print("Hello, I am the muffin man")
            app.processEvents()


class plot_Random(): # This is designed to test the success of the multithreading functionality
    def __init__(self,live_Graph, parent=None):
        super(plot_Random,self).__init__()
        myListX =[]
        myListY= []
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






        #################### Object Declaration ####################
GPIO.setmode(GPIO.BCM)
# Linear Actuator
pinLA = 16
pinEnable = 13
linearActuator = LinearActuator(pinLA,pinEnable)
# Analog-Digital Converter
adc = ads.ADS1115(0x48)
GAIN = 2/3
#
# MOS Sensor
MOS_adc_channel = 0
mos1 = MOS(adc, MOS_adc_channel)
# Heater
heater = 26
Metro_Heater = Heater(heater)
# Pump (Acting as Valve 3 on the PCB)
pump_pin = 20
pump = Pump(pump_pin)
# Valves
pinvalve1 = 17
pinvalve2 = 22
pinvalve3 = 19
pinvalve4 = 5
pinvalve5 = 27
##Valve 6 was never actually created, reconfiguring this value will be necessary
pinvalve6 = 7
valve1 = Valve('Valve1',pinvalve1) #Methane Tank to MFC
valve2 = Valve('Valve2',pinvalve2) #H2 Tank to MFC
valve3 = Valve('Valve3',pinvalve3) #Sample Gas into Chamber
valve4 = Valve('Valve4',pinvalve4) #Air into Chamber
valve5 = Valve('Valve5',pinvalve5) #Chamber Exhaust
valve6 = Valve('Valve6',pinvalve6)

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

#Max31855
##spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
##cs = digitalio.DigitalInOut(board.D21)
##max31855 = adafruit_max31855.MAX31855(spi, cs)



# Bme280 (I2C Network)
# First BME
##i2c = busio.I2C(board.SCL, board.SDA)
##bme280 = adafruit_bme280_76.Adafruit_BME280_I2C(i2c)
### Second BME
##bme280_2 = adafruit_bme280.Adafruit_BME280_I2C(i2c)


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
H2s_detected = QLabel()
H2s_detected.setText("H2S Detected")
H2s_detected.setStyleSheet("QLabel {font: 13px; border: 2px solid light gray; color: gray}")
H2s_notdetected = QLabel()
H2s_notdetected.setText("H2S Not Detected")
H2s_notdetected.setStyleSheet("QLabel {font: 13px; border: 2px solid light gray; color: gray}")
H2s_undefined = QLabel()
H2s_undefined.setText("H2S Data Unavailable")
H2s_undefined.setStyleSheet("QLabel {font:13px; border: 2px solid light gray; color: gray}")
fpLayout.addWidget(startB,4,1,1,2)
fpLayout.addWidget(stopB,4,3,1,2)
fpLayout.addWidget(printing,6,1,1,4)
fpLayout.addWidget(liveGraph,1,1,3,3)
fpLayout.addWidget(progress, 5,1,1,4)
fpLayout.addWidget(H2s_detected, 1,4,1,1)
fpLayout.addWidget(H2s_notdetected,2,4,1,1)
fpLayout.addWidget(H2s_undefined,3,4,1,1)
firstPage.setLayout(fpLayout)

## Manual Controls Page Initiation
secondPage = QWidget()
spLayout = QGridLayout()
spLayout.setVerticalSpacing(0)
# Must be changed if working on raspberry pi or personal laptop
schem1 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v1b.png","/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v1a.png")
schem2 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v2b-2.png", "/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v2a-2.png")
schem3 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v3b.png", "/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v3a.png")
schem4 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v4b.png","/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v4a.png")
schem5 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v5dis.png","/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v5en.png")
schem6 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v6dis.png","/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v6en.png")

v1 = valve_Button(1,schem1,valve1)
v2 = valve_Button(2, schem2,valve2)
v3 = valve_Button(3, schem3,valve3)
v4 = valve_Button(4, schem4,valve4)
v5 = valve_Button(5, schem5,valve5)
v6 = valve_Button(6, schem6,valve6)
heaterB = heater_Button(Metro_Heater)
pumpB = pump_Button(pump)
linearAc = linAc_Button(linearActuator)
stepperB = stepper_Button(Stepper_Motor)
stepperB2 = stepper_Button(Stepper_Motor2)
mos = mos_Button(mos1)
mos_val = QLabel()
mos_val.setText("MOS: ")
cb = cleanse_Button()
purgeB = purge_Button()
spLayout.addWidget(v1, 1,1)
spLayout.addWidget(v2, 2,1)
spLayout.addWidget(v3, 3,1)
spLayout.addWidget(v4, 4,1)
spLayout.addWidget(v5, 5,1)
spLayout.addWidget(v6, 6,1)
spLayout.addWidget(heaterB, 6,2)
spLayout.addWidget(pumpB,7,2)
spLayout.addWidget(linearAc,1,2)
spLayout.addWidget(stepperB2, 2,2)
spLayout.addWidget(mos,3,2)
spLayout.addWidget(cb, 4,2)
spLayout.addWidget(purgeB,5,2)
spLayout.addWidget(mos_val,7,1)
spLayout.addWidget(schem1, 1,3, 7,2)
spLayout.addWidget(schem2, 1,3, 7,2)
spLayout.addWidget(schem3, 1,3, 7,2)
spLayout.addWidget(schem4, 1,3, 7,2)
spLayout.addWidget(schem5, 1,3, 7,2)
spLayout.addWidget(schem6, 1,3, 7,2)

secondPage.setLayout(spLayout)

mainPage.addTab(firstPage, "Sensor Response")
mainPage.addTab(secondPage, "Manual Controls")

mainPage.show()
app.exec_()

GPIO.cleanup()