#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:28:55 2019

@author: EmilyEarl
"""

## Mini - MetroVan Code 

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
import sys
import time
import datetime
from Metrovan_components import *
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ads
import busio
import adafruit_bme280
import digitalio
import board
import numpy as np


# Need to make a peristaltic pump class, and a peristaltic pump button class 
# Need to make a servo class and servo button class 
dataVector = []
timeVector = []
fill_line_clense_time = 20 #normally 20
global H2s_detected
global H2s_notdetected
global H2s_undefined
global are_maching_learning
are_machine_learning = "NO"
global app
global peri_pumpF
global peri_pumpB
global mos_val
global purgeB
global v1
global v2
global pumpB 
global heaterB
global printing
global servoB
global liveGraph
global mos 
global progress
global emergencyStop
global totalTime
global veryStartTime
veryStartTime = time.time() 
totalTime = 300
emergencyStop = "RUN"

def update_Graph(xList,yList):
    global liveGraph
    global emergencyStop
    global app
    global veryStartTime
    global totalTime
    global progress
    
    progress.setValue((time.time() - veryStartTime)/totalTime*100)
    liveGraph.plot(xList,yList)
    app.processEvents()

#valve2 switches between 
#overall 40 seconds on sample, 20 on clean 
# valve 1 open when purging dirty side 
# close valve 1 when purging clean side 
    # valve 1 is normally closed without power 

    
def purge_system_raw(): 
    start_time = time.time() 
    global printing 
    printing.setText("Purging System") 
    global v1 
    global v2 
    global pumpB
    global servoB
    global veryStartTime
    global app
    global emergencyStop
    
    ## Start purging the dirty side 
    servoB.servo.clean_chamber()
    if v2.valve.state != False:
        v2.disable()
    if v1.valve.state != True:
        v1.enable()
    sample_cleanse_time = 40
    start_time = time.time()
    pumpB.enable()
    while time.time() < start_time + sample_cleanse_time:
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    pump.disable()
    servoB.servo.sample_chamber()
    if v2.valve.state != True:
        v2.enable()
    if v1.valve.state != False:
        v1.disable()
    clean_cleanse_time = 20
    start_time = time.time()
    while time.time() < start_time + clean_cleanse_time:
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    
def fill_chamber():
    global heaterB
    global peri_pumpB
    global peri_pumpF
    global emergencyStop
    global very_Start_Time
    global totalTime
    global progress
    heaterB.enable()
    peri_pumpF.enable()
    progress.setValue((time.time()- veryStartTime)/totalTime*100)
    app.processEvents()
    if emergencyStop == "STOP":
       return
    peri_pumpB.enable()
    progress.setValue((time.time()- veryStartTime)/totalTime*100)
    app.processEvents()
    if emergencyStop == "STOP":
       return
    start_time = time.time() 
    while time.time() < (vaporization_time + start_time):
        progress.setValue((time.time()- veryStartTime)/totalTime*100)
        app.processEvents()
        if emergencyStop == "STOP":
            break
    if emergencyStop == "STOP":
        return
    heaterB.disable()
    
def collect_data(xVector,yVector):
    global heaterB
    global peri_pumpF
    global peri_pumpB
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
    if servoB.state != "clean":
        servoB.open_clean()
    
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
            if servoB.state != "sample":
                servoB.open_sample()

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        if (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (emergencyStop != "STOP"):
            print("Inside the first 10 seconds loop or last loop")
            if servoB.state != "clean":
                servoB.open_clean()

        # Otherwise, keep outputs off
##        else:
##            if linearAc.linearAc.state != 'retracted':
##                linearAc.linearAc.retract()
                
##    dataVector[:] = [x * (-1) for x in dataVector]
    #dataVector[:] = [baseline - x  for x in dataVector]
    if emergencyStop == "STOP":
        return
    print("Before the stack")
    dataVector[:] = [baseline - x  for x in dataVector]
    combinedVector = np.column_stack((timeVector, dataVector))
    print("Right before save") 
##    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = time.strftime("/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/Mini/%a%d%b%Y%H%M%S.csv",time.localtime())
    #filename = "/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/EmilyTest.csv"
    print("after filename") 
    np.savetxt(filename,combinedVector, fmt='%.10f', delimiter=',')
    print("File Saved")
    printing.setText("File Saved")

    pass
    heaterB.cool()
    
class peristaltic_pump_Button(QPushButton):
    def __init__(self, peri_pump,forb, parent =None):
        super(peristaltic_pump_Button, self).__init__(parent)
        self.peri_pump = peri_pump
        self.setStyleSheet("QPushButton {font: 13px}")
        if forb == "forwards":
            self.setText("Deliver Sample")
        else:
            self.setText("Remove Excess Sample")
        # Must be changed if working on Raspberry pi or personal laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        self.clicked.connect(lambda: self.enable())
    def enable(self):
        if self.forb == "forwards":
            self.peri_pump.forwards()
        elif self.state == "backwards":
            self.peri_pump.backwards()
    
        
class servo_Button(QWidget):
    def __init__(self, servo, parent=None):
        super(servo_Button, self).__init__(parent)
        self.servo = servo
        self.state = "default"
        self.layout = QVBoxLayout()
        self.title = QLabel("Servo")
        self.title.setStyleSheet("QLabel {font: 13px}")
        self.setStyleSheet("QSlider{max-height: 7px}")
        self.layout.addWidget(self.title)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(2)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setValue(1)
        self.slider.sliderReleased.connect(self.move_Servo)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)
    def move_Servo(self):
        self.number = self.slider.value()
        if self.number == 0:
            self.servo.sample_Chamber()
        elif self.number == 2: 
            self.servo.clean_Chamber()
        else:
            self.servo.default()
    def open_clean(self):
        self.servo.clean_chamber()
        self.state = "clean"
    def open_sample(self):
        self.servo.sample_chamber()
        self.state = "sample"
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
        pass
        
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
            global peri_pumpB
            global peri_pumpF
            peri_pumpB.peri_pump.move_time = 10
            peri_pumpF.peri_pump.move_time = 10
            # fill with how to change the peristaltic pump
        elif retval == QtGui.QMessageBox.No:
            global peri_pumpB
            global peri_pumpF
            peri_pumpB.peri_pump.move_time = 7
            peri_pumpF.peri_pump.move_time = 7
            # fill with how to change the peristaltic pump

       
        veryStartTime = time.time()
        test_time  = time.time()
        global H2s_undefined
        H2s_undefined.setStyleSheet("QLabel {font:13px; border: 2px solid light gray; color: gray}")
        global liveGraph
        liveGraph.clear()
        self.setEnabled(False)
        global purgeB
        purgeB.setEnabled(False)
        global v1
        v1.setEnabled(False)
        global v2
        v2.setEnabled(False)
        peri_pumpB.setEnabled(False)
        peri_pumpF.setEnabled(False)
        global app 
        global pumpB
        pumpB.setEnabled(False)
        global heaterB
        heaterB.setEnabled(False)
        global printing
        
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
        peri_pumpB.setEnabled(True)
        peri_pumpF.setEnabled(True) 
        purgeB.setEnabled(True) 
        global app 
        global pumpB
        pumpB.setEnabled(True)
        global heaterB
        heaterB.setEnabled(True)
        global printing
        
        
        
        
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
        global peri_pumpB
        peri_pumpB.setEnabled(True)
        global peri_pumpF
        peri_pumpF.setEnabled(True)
        global v2
        v2.setEnabled(True)
        v2.disable()
        global app 
        global pumpB
        pumpB.setEnabled(True)
        pumpB.disable()
        global heaterB
        heaterB.setEnabled(True)
        heaterB.cool()
        global printing
        
        
        
        
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
            
## Now the variables
GPIO.setmode(GPIO.BCM) 
peri_pumpH = 16
peri_pumpL = 12
peri_pumpE = 20
servo_pin = 8
servo_enable = 7
heater_pin = 26
valve1_pin = 19
valve2_pin = 14
pump_pin = 21
mos_channel = 1

adc = ads.ADS1115(0x48)
peri_pump = Peristaltic_Pump(peri_pumpH,peri_pumpL,peri_pumpE)
servo = servo(servo_pin,servo_enable)
heater = Heater(heater_pin)
valve1 = Valve("Valve 1", valve1_pin)
valve2 = Valve("Valve 2", valve2_pin)
pump = Pump(pump_pin)
mos1 = MOS(adc, mos_channel)

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
schem1 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v1dismini.png","/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v1enmini.png")
schem2 = schematic("/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v2bmini.png", "/home/pi/Documents/gui/MetroVan_GUI/New_GUI/v2enmini.png")

v1 = valve_Button(1,schem1,valve1)
v2 = valve_Button(2, schem2,valve2)
heaterB = heater_Button(heater)
pumpB = pump_Button(pump)
servoB = servo_Button(servo)
peri_pumpF = peristaltic_pump_Button(peri_pump, "forwards")
peri_pumpB = peristaltic_pump_Button(peri_pump, "backwards")

mos = mos_Button(mos1)
mos_val = QLabel()
mos_val.setText("MOS: ") 
purgeB = purge_Button()
spLayout.addWidget(v1, 1,1)
spLayout.addWidget(v2, 2,1)
spLayout.addWidget(heaterB, 3,1)
spLayout.addWidget(pumpB,4,1)
spLayout.addWidget(servoB,1,2)
spLayout.addWidget(peri_pumpF, 2,2)
spLayout.addWidget(peri_pumpB,3,2)
spLayout.addWidget(mos,4,2)
spLayout.addWidget(purgeB,5,2)
spLayout.addWidget(mos_val,5,1)
spLayout.addWidget(schem1, 1,3, 5,2)
spLayout.addWidget(schem2, 1,3, 5,2)





secondPage.setLayout(spLayout)



mainPage.addTab(firstPage, "Sensor Response")
mainPage.addTab(secondPage, "Manual Controls") 

mainPage.show()
app.exec_()

GPIO.cleanup()



                