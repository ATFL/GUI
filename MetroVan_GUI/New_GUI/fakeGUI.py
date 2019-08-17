#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 16:23:39 2019

@author: EmilyEarl
"""

## Fake GUI for high res images for MetroVan 


#!/usr/bin/python3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
import sys
import time
import datetime



dataVector = []
timeVector = []
fill_line_clense_time = 20 #normally 20
global H2s_detected
global H2s_notdetected
global H2s_undefined
global are_maching_learning
are_machine_learning = "NO"
global app
global stepperB2
global cb
global purgeB
global v3
global v4
global v5
global v6
global pumpB 
global heaterB
global printing
global linearAc
global stepperB
global liveGraph
global mos 
global progress
progress = 0
global emergencyStop
global totalTime
global veryStartTime
veryStartTime = time.time() 
totalTime = 600
emergencyStop = "RUN"

def update_Graph(xList,yList):
    global liveGraph
    global emergencyStop
    global app
    global veryStartTime
    global totalTime
    
    progress.setValue((time.time() - veryStartTime)/totalTime*100)
    liveGraph.plot(xList,yList)
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
    linearAc.linearAc.retract()
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
    if linearAc.linearAc.state != 'retracted':
        linearAc.linearAc.retract()
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
    if linearAc.linearAc.state != 'retracted':
        linearAc.linearAc.retract()
    
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
            dataVector.append(mos.mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
            timeVector.append(time.time() - start_time)
           # print(*dataVector)
           # print("Before calling update Graph") 
            update_Graph(timeVector,dataVector)
            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        elif (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (emergencyStop != "STOP")):
            print("we are in the 10-50 seconds loop") 
            if linearAc.linearAc.state != 'extended':
                linearAc.linearAc.extend()

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        elif (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (emergencyStop != "STOP"):
            print("Inside the first 10 seconds loop or last loop")
            if linearAc.linearAc.state != 'retracted':
                linearAc.linearAc.retract()

        # Otherwise, keep outputs off
        else:
            if linearAc.linearAc.state != 'retracted':
                linearAc.linearAc.retract()
                
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
    def __init__(self, parent=None):
        super(heater_Button, self).__init__()
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px; max-height: 20px}")
        # Must be changed if working on Raspberry Pi or personal Laptop
        self.green = QtGui.QIcon("/Users/EmilyEarl/Downloads/attachments/on.svg")
        # Must be changed if working on Raspberry Pi or personal laptop
        self.red = QtGui.QIcon("/Users/EmilyEarl/Downloads/attachments/off.svg")
        self.setIcon(self.red)
        self.setText("Heater Off")
        self.state = "off"
        self.clicked.connect(lambda: self.heater_Switch())
      
    def heater_Switch(self):
        if self.state == "off":
            self.setIcon(self.green)
            self.setText("Heater On")
            self.state = "on"
        
        elif self.state == "on":
            self.setIcon(self.red)
            self.setText("Heater Off")
            self.state = "off"
            
    def heat(self):
        if self.state != "on":
           
            self.setIcon(self.green)
            self.setText("Heater On")
            self.state = "on"
            global app
            app.processEvents()
    def cool(self):
        if self.state != "off":
            
            self.setIcon(self.red)
            self.setText("Heater Off")
            self.state = "off"
            global app
            app.processEvents()

class valve_Button(QPushButton):
    def __init__(self, num,schematic, parent=None):
        super(valve_Button, self).__init__()
        self.setText("Valve "+ str(num) + " Mode")
        self.state = "A"
        self.schematic = schematic
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px}")
        # Must be changed if working on Raspberry Pi or personal Laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        self.A = QtGui.QIcon("/Users/EmilyEarl/Downloads/attachments/A.svg")
        self.B = QtGui.QIcon("/Users/EmilyEarl/Downloads/attachments/B.svg")
        self.setIcon(self.A)
        self.clicked.connect(lambda: self.valve_Switch())
    def valve_Switch(self):
        if self.state == "A":
            self.setIcon(self.B)
            self.state = "B"
            self.schematic.valve_Flip()
        elif self.state == "B":
            self.setIcon(self.A)
            self.state = "A"
            self.schematic.valve_Flip()
    def enable(self):
        self.state = "B"
        self.setIcon(self.B)
        self.schematic.valve_Flip()
    def disable(self):
        self.state = "A"
        self.setIcon(self.A)
        self.schematic.valve_Flip()

class pump_Button(QPushButton):
    def __init__(self, parent=None):
        super(pump_Button, self).__init__()
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Pump Off")
        self.state = "off"
        # Must be changed if working on Raspberry pi or personal laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        self.green = QtGui.QIcon("/Users/EmilyEarl/Downloads/attachments/on.svg")
        self.red = QtGui.QIcon("/Users/EmilyEarl/Downloads/attachments/off.svg")
        self.setIcon(self.red)
        self.clicked.connect(lambda: self.pump_Switch())
    def pump_Switch(self):
        if self.state == "off":
            self.setIcon(self.green)
            self.setText("Pump On")
            self.state = "on"
        elif self.state == "on":
            self.setIcon(self.red)
            self.setText("Pump Off")
            self.state = "off"
    def enable(self):
        if self.state == "off":
            self.setText("Pump On")
            self.setIcon(self.green)
            self.state = "on"
    def disable(self):
        if self.state == "on":
            self.setText("Pump Off")
            self.setIcon(self.red)
            self.state = "off"
    
class linAc_Button(QWidget):
    def __init__(self, parent=None):
        super(linAc_Button, self).__init__(parent)
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
    def __init__(self, parent=None):
        super(stepper_Button, self).__init__()
        self.layout = QVBoxLayout()
        self.title = QLabel("Syringe Pump")
        self.title.setStyleSheet("QLabel {font: 13px}")
        self.setStyleSheet("QSlider{max-height: 7px}")
        self.layout.addWidget(self.title)
        self.slider = QSlider(Qt.Horizontal)
        
        self.slider.setMinimum(0)
        self.slider.setMaximum(5)
        self.prevVal = 0
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(0.5)
        #self.setText("Linear Actuator")
        self.slider.setValue(0)
        self.slider.sliderReleased.connect(self.move_Stepper)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)
    def move_Stepper(self):
        self.number = self.slider.value()
        print(self.number)
        if self.prevVal < self.slider.value():
            i = self.slider.value() - self.prevVal
            while i > 0:
                i = i -1
            self.prevVal = self.slider.value()
        if self.prevVal > self.slider.value():
            i = self.prevVal - self.slider.value()
            while i > 0:
                i = i - 1
            self.prevVal = self.slider.value() 
        

class mos_Button(QPushButton):
    def __init__(self,parent=None):
        super(mos_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Read MOS")
        self.clicked.connect(lambda: self.read_MOS()) 
    def read_MOS(self):
        print("MOS Value: 3.719 ")
        
        
class cleanse_Button(QPushButton):
    def __init__(self, parent=None):
        super(cleanse_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Cleanse Lines")
        self.clicked.connect(lambda: self.cleanse_Lines())
    def cleanse_Lines(self):
        global emergencyStop
        print("Cleaning Lines") 
        
class purge_Button(QPushButton):
    def __init__(self,parent=None):
        super(purge_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Purge Chamber")
        self.clicked.connect(lambda: self.purge_Chamber())
    def purge_Chamber(self):
        global emergencyStop
        print("Purging Chamber")
      
        
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
    def start_Procedure(self):
        global H2s_undefined
        H2s_undefined.setStyleSheet("QLabel {font:13px; border: 2px solid light gray; color: gray}")
        global emergencyStop 
        emergencyStop = "RUN"
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
        
        
        global mos
        mos.setEnabled(False)
        global progress
        progress.setValue(0)
        
        print("Starting Test...")
        
       
        while emergencyStop != "STOP":
           xVal = [0.1108071804,0.2100093365,0.3100752831,0.4099316597,0.510373354,0.6100468636,0.7101950645,0.8099265099,0.9096524715,3.0189058781,3.0284538269,3.0377063751,3.047557354,3.0571541786,3.0667219162,3.0762655735,3.0857367516,3.0952670574,3.1046323776,3.1142702103,3.1237902641,3.1336066723,3.1434626579,3.1530840397,3.1625919342,3.1722984314,3.1819214821,3.1914470196,3.2009949684,3.2106707096,3.2200989723,3.2295775414,3.3096420765,3.4098820686,3.5098764896,3.6096637249,3.7097244263,3.8096466064,3.9096524715,4.0097880363,4.1096930504,4.2097036839,4.3097105026,4.4097447395,4.5096564293,4.6096971035,4.709843874,4.8106729984,4.910296917,5.0097956657,5.1097824574,5.2097711563,5.3097867966,5.4097626209,5.5097782612,5.6100337505,5.7099103928,5.8096899986,5.909724474,6.0098118782,6.1096789837,6.2096321583,6.3109433651,6.4108440876,6.5101633072,6.610445261,6.71453619,6.8107030392,6.9108505249,7.0102181435,7.1107909679,7.2101268768,7.3105409145,7.4107296467,7.5101115704,7.6098809242,7.7100346088,7.8101489544,7.9099807739,8.0099744797,8.1100730896,8.2099769115,8.3100357056,8.4099531174,8.5102541447,8.6107230186,8.7103085518,8.8105785847,8.9108483791,9.0102133751,9.1101250648,9.2130365372,9.310530901,9.4107992649,9.5130643845,9.6097431183,9.7104189396,9.8099319935,9.9100050926,10.0097501278,10.1097209454,10.2096209526,10.3108072281,10.4139552116,10.5100300312,10.6106603146,10.7104947567,10.810488224,10.9104988575,11.0104632378,11.110470295,11.2104833126,11.3104767799,11.4107441902,11.5110607147,11.6110155582,11.7106955051,11.8104710579,11.9109098911,12.0102038383,12.1110444069,12.2126324177,12.3101260662,12.410091877,12.5103592873,12.6099655628,12.7099506855,12.8098990917,12.9099566936,13.0099318027,13.1099197865,13.2102730274,13.3100047112,13.4101037979,13.5113563538,13.6102163792,13.7097225189,13.8097572327,13.9097192287,14.009636879,14.1097085476,14.2095429897,14.3097360134,14.4096560478,14.5096757412,14.6097669601,14.7097153664,14.8128969669,14.9102218151,15.0117106438,15.1100101471,15.2099299431,15.3099756241,15.4100446701,15.510011673,15.6100428104,15.710054636,15.8099346161,15.9145953655,16.0110871792,16.1106705666,16.2106399536,16.3105978966,16.4103987217,16.5103719234,16.6113972664,16.7101824284,16.8099944592,16.9100885391,17.0108919144,17.1100583076,17.2108211517,17.310110569,17.409999609,17.5099527836,17.6098423004,17.711735487,17.8131558895,17.9116234779,18.0136146545,18.1114044189,18.2100830078,18.31011343,18.4097373486,18.5100295544,18.6100347042,18.7144472599,18.8100683689,18.9101762772,19.0102314949,19.1102588177,19.2105169296,19.3099999428,19.4100084305,19.5099966526,19.6101620197,19.7109282017,19.8103349209,19.9107904434,20.0101618767,20.1099610329,20.2101275921,20.310107708,20.410061121,20.5100543499,20.6100137234,20.7183380127,20.815769434,20.9102339745,21.0109405518,21.1109297276,21.2119450569,21.3104679585,21.4106264114,21.5131602287,21.6132729053,21.7102031708,21.809789896,21.909744978,22.009832859,22.1101791859,22.2099986076,22.3100173473,22.4147894382,22.5100903511,22.6119310856,22.71073699,22.813740015,22.91598773,23.0103743076,23.1108677387,23.2106041908,23.3103716373,23.4101247787,23.5100870132,23.6101715565,23.7101929188,23.8102014065,23.9101855755,24.011095047,24.1153330803,24.2114245892,24.3104608059,24.4110062122,24.5124335289,24.6108956337,24.710495472,24.8117218018,24.910063982,25.0136160851,25.1105778217,25.2111155987,25.3097271919,25.4106616974,25.5100681782,25.6100003719,25.7102189064,25.8106758595,25.9170815945,26.0171160698,26.1102657318,26.2110388279,26.3102338314,26.4101495743,26.510995388,26.610793829,26.7104918957,26.8101556301,26.9110810757,27.0103008747,27.1099851131,27.2099881172,27.3100342751,27.4155189991,27.5098984241,27.6099944115,27.7106151581,27.8104047775,27.9102785587,28.0103242397,28.1100170612,28.2100286484,28.3100969791,28.4100136757,28.5100786686,28.6100075245,28.7099044323,28.8098840714,28.911375761,29.0100209713,29.1099357605,29.2101109028,29.3104364872,29.4100217819,29.5103132725,29.6100687981,29.7100663185,29.8101782799,29.9101057053,30.0102951527,30.1101560593,30.2135510445,30.3105034828,30.4134838581,30.5120103359,30.6133744717,30.7112267017,30.8108894825,30.9110758305,31.0109524727,31.110963583,31.2112910748,31.3109586239,31.4109041691,31.5106635094,31.6105391979,31.7105576992,31.8106315136,31.9110178947,32.0099806786,32.1138832569,32.210103035,32.3098859787,32.4098134041,32.5096535683,32.6097004414,32.7099359035,32.8097939491,32.9097673893,33.0098285675,33.1097772121,33.2096543312,33.3096694946,33.4129998684,33.5102849007,33.6102645397,33.7101430893,33.80996418,33.9100382328,34.0099494457,34.1099390984,34.2099757195,34.3099272251,34.4099521637,34.5099253654,34.6099750996,34.7099318504,34.810500145,34.9103727341,35.0101890564,35.1100354195,35.2100493908,35.3100607395,35.4102945328,35.5105910301,35.6103527546,35.7098588943,35.8099141121,35.9099440575,36.0104341507,36.1102628708,36.2150630951,36.3099918365,36.4099955559,36.5099670887,36.6100292206,36.710003376,36.8096570969,36.9097447395,37.0101556778,37.1099405289,37.2112834454,37.3103868961,37.4101378918,37.5102090836,37.6101808548,37.7101919651,37.8099112511,37.91020751,38.0101537704,38.1100919247,38.2100405693,38.3101081848,38.4130249023,38.5130383968,38.6101307869,38.7099680901,38.8101809025,38.9099154472,39.0099265575,39.1099863052,39.2100629807,39.3098948002,39.4100124836,39.509912014,39.6101689339,39.7099986076,39.8101093769,39.9100432396,40.0105953217,40.1104056835,40.2104980946,40.3104858398,40.4101066589,40.5100464821,40.6100378036,40.7101385593,40.809943676,40.9100594521,41.0105690956,41.1101896763,41.2102255821,41.3101756573,41.4101829529,41.5101416111,41.6100907326,41.710123539,41.810100317,41.9103553295,42.0113182068,42.1124987602,42.2101271152,42.3101580143,42.4105260372,42.5100963116,42.6102318764,42.7102124691,42.8102016449,42.9102125168,43.0102038383,45.0408861637,45.0508060455,45.0612633228,45.0717940331,45.0817251205,45.0916700363,45.1014916897,45.1117072105,45.1217844486,45.1317818165,45.1416010857,45.1514222622,45.1613993645,45.1723198891,45.1821804047,45.1919863224,45.2018909454,45.2118153572,45.2217638493,45.2317974567,45.2418191433,45.2516589165,45.3100543022,45.4097306728,45.5099694729,45.60998559,45.7102649212,45.8101806641,45.9101295471,46.0100855827,46.1101799011,46.2100775242,46.3102080822,46.4102330208,46.5104894638,46.6108746529,46.7104682922,46.8102910519,46.9106240273,47.0116102695,47.1141076088,47.2104384899,47.3328909874,47.4110569954,47.5180156231,47.6156673431,47.7109827995,47.8106434345,47.9100625515,48.029992342,48.110196352,48.2100393772,48.3101594448,48.4101498127,48.509983778,48.6099712849,48.7100563049,48.8101363182,48.9101035595,49.0106601715,49.1106791496,49.2100641727,49.3107964993,49.4106707573,49.5107204914,49.6105964184,49.7104406357,49.8103685379,49.9140908718,50.0100016594,50.1101827621,50.2100155354,50.3100268841,50.4100897312,50.5100450516,50.6101438999,50.7102534771,50.8099520206,50.9100222588,51.0098726749,51.1099908352,51.210360527,51.3102173805,51.4100506306,51.5101101398,51.6114938259,51.7100157738,51.810116291,51.9100539684,52.0100631714,52.1100811958,52.2102890015,52.3104486465,52.4100501537,52.5100903511,52.6100702286,52.7098426819,52.8097410202,52.9106230736,53.0099897385,53.1103539467,53.2099878788,53.3100190163,53.4102170467,53.5100524426,53.6100823879,53.7163763046,53.8100545406,53.910061121,54.0133121014,54.1101887226,54.2114500999,54.3105869293,54.411469698,54.5113899708,54.6108360291,54.7108528614,54.8105280399,54.9103324413,55.0101020336,55.1100876331,55.2101049423,55.3100924492,55.4100825787,55.5102579594,55.6104154587,55.7101104259,55.8101141453,55.9101011753,56.0102977753,56.1100857258,56.2101089954,56.3098840714,56.4098775387,56.5102097988,56.6098349094,56.7100024223,56.8099689484,56.909787178,57.0100288391,57.1099610329,57.2096533775,57.3096625805,57.4097056389,57.5097420216,57.6099536419,57.7100234032,57.8100168705,57.9099824429,58.0103111267,58.1102137566,58.2099802494,58.3101146221,58.4103591442,58.510150671,58.610471487,58.7101781368,58.8101096153,58.9118845463,59.0100154877,59.109960556,59.2099075317,59.3099420071,59.4099955559,59.5099701881,59.6099660397,59.7099812031,59.8099145889,59.9099628925,60.0106756687,60.1100311279,60.2099542618,60.3100643158,60.4101924896,60.5099935532,60.6098899841,60.7100219727,60.8096773624,60.9096622467,61.0101389885,61.1096479893,61.2096557617,61.3099002838,61.4096307755,61.5096209049,61.6096551418,61.70962286,61.8096392155,61.9096980095,62.0096583366,62.1096644402,62.2096612453,62.3096349239,62.4096703529,62.5096299648,62.6096842289,62.7096655369,62.809687376,62.9096632004,63.0096330643,63.1098365784,63.2096793652,63.3096556664,63.4097063541,63.5096523762,63.6096804142,63.7096443176,63.8095662594,63.9096074104,64.0096414089,64.1095647812,64.209612608,64.3096346855,64.4097397327,64.5096075535,64.6097583771,64.709707737,64.8096563816,64.9095962048,65.0097327232,65.1096813679,65.2097346783,65.3099410534,65.409693718,65.5096898079,65.6101891994,65.7096509933,65.8096904755,65.9097929001,66.0097949505,66.1096816063,66.2100510597,66.3096780777,66.4096455574,66.5106999874,66.6114351749,66.7101566792,66.8126676083,66.9100627899,67.0104210377,67.1114294529,67.2099645138,67.3101379871,67.4099726677,67.5100212097,67.6103725433,67.7101864815,67.8099741936,67.9100036621,68.0100033283,68.1100645065,68.2100353241,68.3099403381,68.4099750519,68.5099737644,68.6100170612,68.7099883556,68.8099884987,68.9104197025,69.0106406212,69.1105835438,69.2102704048,69.310885191,69.4103038311,69.5099892616,69.6103429794,69.7108268738,69.8097593784,69.9097166061,70.010226965,70.1098258495,70.209713459,70.3097472191,70.4099283218,70.5097231865,70.6097097397,70.7096767426,70.8097138405,70.9097654819,71.0097293854,71.1097295284,71.2096552849,71.3096609116,71.409730196,71.5097260475,71.609744072,71.7096755505,71.809718132,71.9095933437,72.009765625,72.1096146107,72.2096188068,72.3096055984,72.4100003242,72.5096349716,72.6100511551,72.7099328041,72.8099441528,72.9103629589,73.0100638866,73.1096153259,73.2096395493,73.309678793,73.4096734524,73.5097908974,73.609811306,73.7096629143,73.8096108437,73.90969491,74.0097239017,74.1097638607,74.2105500698,74.3110563755,74.4137847424,74.5132112503,74.6101822853,74.7102305889,74.810131073,74.9101819992,75.010184288,75.110170126,75.2102217674,75.3101503849,75.4103608131,75.5104534626,75.612016201,75.7110671997,75.8106300831,75.911482811,76.0099463463,76.1099476814,76.210255146,76.3107366562,76.4105181694,76.5106756687,76.610575676,76.7100687027,76.8118629456,76.9100255966,77.0099799633,77.1099183559,77.2102150917,77.3100016117,77.4099953175,77.5100255013,77.609664917,77.709703207,77.809876442,77.90964818,78.0101499557,78.1099152565,78.2096970081,78.3096404076,78.4097361565,78.5096695423,78.6098506451,78.7144582272,78.809804678,78.909673214,79.0097472668,79.1097722054,79.2096838951,79.3097119331,79.4096093178,79.509740591,79.6097068787,79.709559679,79.8096010685,79.9096462727,80.0096411705,80.1095700264,80.209634304,80.309586525,80.4097962379,80.5100517273,80.6100935936,80.7100412846,80.8114898205,80.9100410938,81.0101015568,81.1103403568,81.2099070549,81.3099219799,81.4101588726,81.5100674629,81.6099691391,81.7108802795,81.8099269867,81.9099900723,82.0100047588,82.1105773449,82.2105710506,82.310046196,82.4099693298,82.5100595951,82.6099903584,82.709987402,82.8115096092,82.9100325108,83.0146253109,83.1109187603,83.2101180553,83.3100814819,83.4101145267,83.5103263855,83.6126668453,83.7103545666,83.8098502159,83.9097688198,84.009718895,84.1099483967,84.2100784779,84.310949564,84.4099776745,84.5100636482,84.6103923321,84.7106473446,84.8108534813,84.910769701,85.0109250546,85.1105258465,85.2100520134,85.3100562096,85.4100337029,85.510035038,85.6100034714,85.7099888325,85.8100152016,85.9100239277,86.0101680756,86.1098763943,86.2099802494,86.310488224,86.4099583626,86.5100274086,86.6099703312,86.7099642754,86.810110569,86.9101724625,87.0100243092,87.1100766659,87.2099292278,87.3101079464,87.4104719162,87.5164256096,87.6145045757,87.7103266716,87.8103947639,87.9100589752,88.0101385117,88.1100087166,88.2099938393,88.3100316525,88.4098768234,88.5099375248,88.6099655628,88.7103641033,88.8110539913,88.9102978706,89.0103030205,89.1104030609,89.2104184628,89.3102705479,89.4107897282,89.5102362633,89.6101951599,89.7101991177,89.8102638721,89.910825491,90.0144388676,90.1106843948,90.2104823589,90.3134765625,90.4102518559,90.5107507706,90.6101164818,90.7106254101,90.8105568886,90.9096977711,91.0097258091,91.1095814705,91.209624052,91.3096020222,91.4095797539,91.509575367,91.6095945835,91.7096068859,91.8095777035,91.9096055031,92.0097455978,92.1097602844,92.2096087933,92.3095891476,92.4095897675,92.5096213818,92.609618187,92.7095887661,92.8095917702,92.9096007347,93.0101072788,93.1100244522,93.2100651264,93.3101792336,93.410119772,93.5097055435,93.6097147465,93.7098867893,93.809715271,93.9096744061,94.0097308159,94.1097009182,94.2097172737,94.3097572327,94.4097247124,94.5097050667,94.6097383499,94.7098183632,94.8097236156,94.9098167419,95.009676218,95.1097729206,95.209675312,95.3100726604,95.4103755951,95.5095870495,95.6097109318,95.7096369267,95.8096289635,95.9096755981,96.0099358559,96.110663414,96.2105941772,96.3113617897,96.411945343,96.5120794773,96.6120727062,96.7120630741,96.8111555576,96.9150540829,97.0160443783,97.1113789082,97.2133867741,97.3100185394,97.4099681377,97.5100665092,97.6100289822,97.710057497,97.81041646,97.9107239246,98.010869503,98.1110355854,98.2107803822,98.3108472824,98.4110834599,98.5108120441,98.6111295223,98.7107961178,98.8114800453,98.9109575748,99.0104703903,99.1104977131,99.2104861736,99.3105037212,99.4106986523,99.5105171204,99.610527277,99.7102429867,99.8099923134,99.9100039005,100.0100297928,100.1099486351,100.2100343704,100.3101365566,100.4100801945,100.5100581646,100.6101646423,100.7100262642,100.8095929623,100.909702301,101.009717226,101.1103620529,101.2102131844,101.3096389771,101.4096953869,101.509755373,101.6096498966,101.7098565102,101.8096396923,101.9098677635,102.0104885101,102.1101722717,102.2100794315,102.3100962639,102.4098334312,102.5098876953,102.6098666191,102.7097122669,102.8097302914,102.9103171825,103.0102453232,103.1102325916,103.210183382,103.3102316856,103.410063982,103.5100429058,103.6101005077,103.7098999023,103.8101642132,103.9102475643,104.0100061893,104.1099171638,104.209962368,104.3113570213,104.4100704193,104.5100395679,104.610170126,104.7099158764,104.8105316162,104.9105494022,105.0111346245,105.1103329659,105.210031271,105.3103489876,105.4131600857,105.5109984875,105.6104948521,105.7111954689,105.8126528263,105.9103281498,106.009901762,106.109998703,106.2099909782,106.3104321957,106.410451889,106.5103647709,106.6107468605,106.7122764587,106.8100931644,106.9109623432,107.0100226402,107.1096003056,107.2101278305,107.3105983734,107.4108734131,107.5110793114,107.6123352051,107.7121841908,107.8103539944,107.9101996422,108.0107939243,108.1120958328,108.2102286816,108.3114614487,108.4115672112,108.5121846199,108.6120026112,108.7099974155,108.8103251457,108.9107851982,109.0104768276,109.1107816696,109.210889101,109.3109128475,109.4102828503,109.5101726055,109.6099874973,109.710351944,109.8101758957,109.9101276398,110.0101253986,110.1102077961,110.2104616165,110.3100457191,110.4096591473,110.5096831322,110.6096496582,110.7097094059,110.8097338676,110.9097168446,111.0098085403,111.10973382,111.2097043991,111.3096356392,111.4096772671,111.5097167492,111.6097199917,111.7099428177,111.80966115,111.9096534252,112.0096566677,112.1096715927,112.2096512318,112.309687376,112.4096791744,112.5097153187,112.60962677,112.7097604275,112.8097093105,112.9097149372,113.0095911026,113.1096363068,113.2095994949,113.3095970154,113.4096078873,113.5097620487,113.6096117496,113.7096450329,113.8096094131,113.9097628593,114.0099315643,114.10978508,114.2096500397,114.3098571301,114.4100379944,114.5111474991,114.609739542,114.7097539902,114.8099124432,114.9100198746,115.0100641251,115.1108932495,115.2099671364,115.3097300529,115.4096062183,115.5100281239,115.6097400188,115.7097485065,115.8098771572,115.9101157188,116.0101459026,116.1098144054,116.2097225189,116.3096909523,116.4097070694,116.5096588135,116.6098093987,116.7113866806,116.8096199036,116.9100515842,117.0104868412,117.1100735664,117.2101082802,117.3105733395,117.4132606983,117.5150432587,117.6114706993,117.7122347355,117.8127982616,117.9130971432,118.0154390335,118.110751152,118.2100296021,118.3102090359,118.4101593494,118.5102431774,118.6111912727,118.710334301,118.8100502491,118.910194397,119.0101845264,119.1101944447,119.2113001347,119.3110740185,119.4110586643,119.5141582489,119.6110098362,119.7101795673,119.8101844788,119.9103877544,120.01014781,120.1100604534,120.2101478577,120.3100061417,120.4112253189,120.5118975639,120.6260123253,120.7109687328,120.8339247704,120.9121546745,121.01567626,121.110262394,121.2158071995,121.3102331161,121.4101419449,121.5105865002,121.6102190018,121.7101612091,121.8105397224,121.9106726646,122.0125641823,122.113011837,122.212816,122.3104221821,122.4102303982,122.5101037025,122.6103198528,122.7124488354,122.81077981,122.9100980759,123.0102233887,123.1098742485,123.2106685638,123.3100378513,123.4099025726,123.5099253654,123.6104536057,123.7152109146,123.8096694946,123.9108178616,124.0097811222,124.1103975773,124.2119357586,124.3302721977,124.4148447514,124.5100922585,124.6212244034,124.7144458294,124.81051898,124.9101612568,125.0102279186,125.1110002995,125.2101926804,125.3105835915,125.4119932652,125.5130643845,125.6108219624,125.7110807896,125.8106808662,125.9116594791,126.0106108189,126.1101763248,126.210365057,126.3230073452,126.4108424187,126.510507822,126.610257864,126.711196661,126.8101694584,126.9113919735,127.010176897,127.1102545261,127.2101738453,127.3102743626,127.4104588032,127.5103342533,127.6097126007,127.7099301815,127.809864521,127.9098007679,128.0097885132,128.1098132133,128.2097892761,128.3097503185,128.4101018906,128.5099070072,128.610575676,128.7108459473,128.8107962608,128.9113893509,129.0104227066,129.1102621555,129.2101976871,129.310120821,129.4109740257,129.510065794,129.6100788116,129.7100419998,129.8100316525,129.9103224277,130.0103869438,130.1100561619,130.2101011276,130.3101878166,130.4109230042,130.5102915764,130.6119432449,130.7113204002,130.8107349873,130.910564661,131.0100972652,131.1109173298,131.2102966309,131.3108894825,131.4101054668,131.5109071732,131.6107976437,131.7138900757,131.8104557991,131.911583662,132.0102772713,132.1156897545,132.2128019333,132.3105940819,132.4102253914,132.5100541115,132.6103115082,132.7133951187,132.812510252,132.9199690819,133.0100049973,133.1100103855,133.2116806507,133.3182005882,133.4126474857,133.512283802,133.6118824482,133.7105801105,133.8109352589,133.9119281769,134.0104956627,134.1108796597,134.2107851505,134.3105077744,134.4105911255,134.5121097565,134.610722065,134.7158503532,134.8144137859,134.9102153778,135.0103712082,135.1126866341,135.2103483677,135.3100063801,135.4103705883,135.5104959011,135.6107304096,135.7106878757,135.8107452393,135.9111673832,136.01115942,136.1108064651,136.2102286816,136.3102514744,136.4101941586,136.5109562874,136.6109881401,136.7101240158,136.8102588654,136.9102067947,137.0171844959,137.1108939648,137.2143275738,137.3098900318,137.410233736,137.5205523968,137.6164438725,137.7137715816,137.8110451698,137.9137969017,138.0110735893,138.1112318039,138.2155292034,138.3120491505,138.4160895348,138.510007143,138.6098630428,138.7099256516,138.8102052212,138.9104430676,139.0108466148,139.1109032631,139.2103910446,139.310226202,139.4102714062,139.5101840496,139.6101574898,139.7105152607,139.8105380535,139.910421133,140.0101351738,140.1100656986,140.210026741,140.3104195595,140.4107208252,140.5107579231,140.6147563457,140.7102372646,140.8103485107,140.9101498127,141.01040411,141.1102540493,141.2104229927,141.3103251457,141.410368681,141.5105624199,141.6106681824,141.7102203369,141.810542345,141.9101228714,142.0098316669,142.1101460457,142.215190649,142.3123421669,142.4104008675,142.510207653,142.6103842258,142.7106015682,142.8102743626,142.9195129871,143.011305809,143.1110832691,143.2112264633,143.3101553917,143.4144687653,143.511494875,143.6166739464,143.7113797665,143.8105127811,143.910702467,144.0114557743,144.1109628677,144.2101173401,144.3103966713,144.4101629257,144.5099446774,144.6101150513,144.7103891373,144.8101789951,144.9100980759,145.0127286911,145.1106622219,145.2102451324,145.3099014759,145.4111320972,145.5095841885,145.6207859516,145.7145607471,145.8106284142,145.9164574146,146.0109012127,146.1104743481,146.2108113766,146.3099763393,146.410046339,146.5104365349,146.6102137566,146.7110176086,146.8105106354,146.9110372066,147.0100307465,147.1102106571,147.2103364468,147.3111097813,147.4107296467,147.510766983,147.6116468906,147.7100400925,147.8100152016,147.9101486206,148.0100913048,148.1115837097,148.2113115788,148.3099246025,148.4105410576,148.51217556,148.6115906239,148.7105045319,148.8105025291,148.9111392498,149.0096378326,149.1101386547,149.2096757889,149.3101491928,149.4098258018,149.5096304417,149.6096937656,149.7096941471,149.8096725941,149.9096734524,150.0098619461,150.1097888947,150.2100615501,150.3099298477,150.409692049,150.5096149445,150.6097512245,150.7097017765,150.8100407124,150.9098198414,151.0099418163,151.1131029129,151.2105808258,151.3149166107,151.411236763,151.5108773708,151.6102526188,151.710185051,151.8102293015,151.9143619537,152.0100677013,152.1103146076,152.2102024555,152.3134818077,152.4109354019,152.5102415085,152.6101472378,152.7106719017,152.8108184338,152.9106719494,153.010696888,153.1103532314,153.2103798389,153.3104178905,153.4127008915,153.5100903511,153.610291481,153.710190773,153.8099267483,153.9098725319,154.0098991394,154.1099152565,154.2105102539,154.3104262352,154.4100530148,154.5099318027,154.609786272,154.7098326683,154.8131449223,154.9099650383,155.0098688602,155.1144416332,155.2098002434,155.3099002838,155.4116351604,155.5098388195,155.6100857258,155.7097098827,155.8101825714,155.9097080231,156.0098392963,156.1099364758,156.2097058296,156.3098142147,156.4101858139,156.5102636814,156.6099298,156.7098593712,156.8096444607,156.9097197056,157.0096611977,157.1099572182,157.2097847462,157.309586525,157.4096500874,157.5096626282,157.6095676422,157.7096054554,157.809677124,157.9104351997,158.0096309185,158.1096255779,158.20962286,158.3095977306,158.4096684456,158.5096094608,158.6097502708,158.7096512318,158.8097119331,158.9109678268,159.0096206665,159.1349081993,159.2099320889,159.3098618984,159.4109771252,159.5202085972,159.6157069206,159.7098648548,159.8143219948,159.9213857651,160.0158097744,160.1099905968,160.2123017311,160.3114645481,160.4117877483,160.5115706921,160.6118311882,160.7121114731,160.8121914864,160.9214951992,161.0150980949,161.1115853786,161.2113637924,161.3104579449,161.4100980759,161.5194592476,161.6138417721,161.7101607323,161.8100094795,161.9112598896,162.0137174129,162.118329525,162.2105970383,162.3105657101,162.4183189869,162.5101590157,162.611137867,162.7101378441,162.810136795,162.910326004,163.0101184845,163.1101791859,163.210069418,163.3099291325,163.4165053368,163.517580986,163.6098790169,163.709936142,163.810410738,163.9097135067,164.0110006332,164.1099259853,164.2099757195,164.3118014336,164.4102151394,164.5101010799,164.6100900173,164.7103190422,164.8100707531,164.9114580154,165.0101873875,165.1102380753,165.2100636959,165.3105208874,165.4241371155,165.5178415775,165.6118090153,165.7146453857,165.8106257915,165.9102983475,166.010456562,166.1102693081,166.2111938,166.3122344017,166.4109842777,166.5110650063,166.6124851704,166.7113153934,166.8112847805,166.9101550579,167.0106070042,167.1100058556,167.2101004124,167.3100714684,167.4100446701,167.5104773045,167.6105554104,167.709751606,167.8098003864,167.9095902443,168.009565115,168.1095645428,168.2095615864,168.309602499,168.4095749855,168.5098567009,168.6101672649,168.7099921703,168.8099367619,168.9100077152,169.0099952221,169.110147953,169.21017313,169.3101425171,169.410056591,169.5105178356,169.610465765,169.7100768089,169.8099551201,169.910520792,170.0098454952,170.1097829342,170.2097532749,170.309858799,170.4100246429,170.5101439953,170.6099004745,170.7099716663,170.8107376099,170.9102127552,171.0104978085,171.1100301743,171.2101445198,171.3099417686,171.4100840092,171.510445118,171.6098928452,171.7099773884,171.8099143505,171.9099168777,172.0097045898,172.1109457016,172.2099490166,172.3097252846,172.4095737934,172.510543108,172.6104092598,172.7099964619,172.8102231026,172.950330019,173.0097343922,173.1097962856,173.2107579708,173.3097085953,173.4100027084,173.5095815659,173.609565258,173.7095804214,173.8095738888,173.9095671177,174.0095303059,174.1096553802,174.2096540928,174.3098759651,174.4099113941,174.5098588467,174.6098725796,174.7099132538,174.8101093769,174.9111726284,175.0099346638,175.1099374294,175.2103152275,175.3099224567,175.4105165005,175.5101664066,175.6104967594,175.7099940777,175.8101294041,175.9103131294,176.0101425648,176.1103718281,176.2099869251,176.3139185905,176.4100692272,176.5100615025,176.6105909348,176.7102613449,176.8099730015,176.9100625515,177.0100040436,177.1099669933,177.2101275921,177.3110697269,177.4149742126,177.5100436211,177.6096692085,177.7096233368,177.8095679283,177.9098494053,178.0095934868,178.1096041203,178.2096674442,178.3096446991,178.4100542068,178.5096325874,178.6095728874,178.709679842,178.8096776009,178.9099829197,179.0106809139,179.1102256775,179.2101426125,179.3101391792,179.4105195999,179.5104281902,179.6103601456,179.7108001709,179.8102560043,179.9102404118,180.0097169876,180.1097898483,180.2105295658,180.3119804859,180.410387516,180.5100750923,180.6099765301,180.7099483013,180.8100142479,180.9106991291,181.0182521343,181.4460978508,181.5284638405,181.6232159138,181.6331133842,181.6431581974,181.6532509327,181.7389502525,181.8768870831,181.9186229706,182.0124080181,182.1101953983,182.2100536823,182.3100509644,182.4105038643,182.510402441,182.61105299,182.7101383209,182.8103706837,182.910340786,183.0104398727,183.1102905273,183.2103271484,183.3104355335,183.4109222889,183.5106773376,183.6104223728,183.7102799416,183.810148716,183.9101595879,184.0103983879,184.1103446484,184.210050106,184.3102278709,184.4101085663,184.5109155178,184.6101715565,184.7100403309,184.8099551201,184.9100260735,185.0103707314,185.1100804806,185.209987402,185.3099589348,185.4099988937,185.5101180077,185.6098985672,185.7105052471,185.8099393845,185.9100506306,186.0095760822,186.1099817753,186.2108943462,186.3121159077,186.4103620052,186.5102443695,186.6180772781,186.714060545,186.8133230209,186.9100568295,187.0099830627,187.1101579666,187.2099897861,187.3107316494,187.410639286,187.510727644,187.6111798286,187.7105612755,187.8100025654,187.9097905159,188.0104699135,188.1098444462,188.2099461555,188.3098416328,188.4099149704,188.5098845959,188.6099858284,188.7099215984,188.810063839,188.9099094868,189.0120744705,189.1104142666,189.2104518414,189.3097999096,189.4099254608,189.5103361607,189.6104469299,189.7151725292,189.8151996136,189.9151332378,190.0106904507,190.1100711823,190.210901022,190.3109960556,190.410228014,190.5101356506,190.6102852821,190.7109956741,190.8102371693,190.9101667404,191.0101053715,191.1102108955,191.2099802494,191.3103427887,191.4100956917,191.5101182461,191.6100461483,191.7101590633,191.8103911877,191.9105911255,192.0105764866,192.1106104851,192.2105841637,192.3099901676,192.4100348949,192.5100696087,192.6103386879,192.7116370201,192.8100130558,192.909668684,193.0096371174,193.1096742153,193.2096405029,193.3097159863,193.4097197056,193.5096404552,193.6096994877,193.7096881866,193.8096055984,193.9096841812,194.0098452568,194.109691143,194.2096586227,194.3096029758,194.4097604752,194.5096898079,194.6096072197,194.7096195221,194.8095912933,194.9096300602,195.0097539425,195.1097259521,195.2097747326,195.3096849918,195.4096591473,195.5096490383,195.6096727848,195.7096843719,195.8096165657,195.9096844196,196.0098392963,196.1097157001,196.2096672058,196.3098199368,196.4097237587,196.509708643,196.6096675396,196.7096631527,196.8096892834,196.9097008705,197.0098962784,197.1095969677,197.2102208138,197.3102669716,197.4096858501,197.509624958,197.6098132133,197.7096874714,197.8095860481,197.9097204208,198.0097076893,198.1096916199,198.2113130093,198.3096213341,198.4095985889,198.5122771263,198.6097536087,198.7096540928,198.8097183704,198.909733057,199.0096614361,199.1096611023,199.2097012997,199.3097593784,199.4098351002,199.5097062588,199.6096944809,199.7096369267,199.8097171783,199.9097092152]
           yVal = [1.305,1.308,1.305,1.308,1.305,1.305,1.305,1.308,1.308,1.305,1.308,1.308,1.305,1.308,1.305,1.308,1.308,1.308,1.305,1.308,1.308,1.305,1.305,1.308,1.308,1.305,1.308,1.308,1.308,1.305,1.308,1.305,1.308,1.305,1.308,1.305,1.305,1.305,1.308,1.308,1.308,1.308,1.308,1.308,1.305,1.308,1.305,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.305,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.305,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.308,1.311,1.308,1.308,1.311,1.311,1.308,1.311,1.311,1.311,1.311,1.308,1.308,1.308,1.308,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.314,1.311,1.311,1.311,1.311,1.311,1.311,1.311,1.314,1.314,1.311,1.314,1.314,1.311,1.314,1.311,1.314,1.314,1.314,1.314,1.314,1.314,1.314,1.314,1.314,1.314,1.317,1.314,1.317,1.314,1.314,1.314,1.317,1.317,1.317,1.317,1.317,1.317,1.317,1.317,1.317,1.317,1.317,1.317,1.32,1.32,1.317,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.32,1.323,1.323,1.323,1.323,1.323,1.323,1.323,1.323,1.326,1.323,1.326,1.326,1.326,1.326,1.323,1.326,1.326,1.326,1.326,1.326,1.326,1.326,1.329,1.329,1.329,1.329,1.326,1.329,1.329,1.329,1.329,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.338,1.335,1.335,1.335,1.338,1.338,1.338,1.338,1.341,1.341,1.338,1.338,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.344,1.344,1.344,1.344,1.344,1.347,1.344,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.35,1.35,1.35,1.35,1.35,1.35,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.362,1.362,1.362,1.362,1.362,1.362,1.365,1.365,1.365,1.368,1.365,1.368,1.368,1.368,1.368,1.368,1.368,1.368,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.374,1.374,1.374,1.374,1.374,1.377,1.377,1.377,1.377,1.377,1.377,1.38,1.38,1.38,1.383,1.38,1.383,1.383,1.383,1.383,1.383,1.386,1.386,1.386,1.386,1.386,1.386,1.386,1.386,1.389,1.389,1.392,1.389,1.389,1.392,1.392,1.389,1.392,1.392,1.395,1.395,1.395,1.398,1.395,1.398,1.398,1.398,1.398,1.398,1.398,1.398,1.401,1.401,1.401,1.401,1.404,1.401,1.404,1.404,1.404,1.416,1.413,1.413,1.416,1.413,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.416,1.419,1.416,1.419,1.419,1.419,1.419,1.419,1.422,1.422,1.422,1.422,1.422,1.425,1.425,1.425,1.425,1.425,1.428,1.425,1.428,1.428,1.428,1.428,1.428,1.431,1.431,1.431,1.431,1.431,1.431,1.434,1.434,1.434,1.434,1.434,1.434,1.437,1.437,1.437,1.44,1.44,1.44,1.44,1.44,1.44,1.443,1.44,1.443,1.443,1.443,1.443,1.443,1.443,1.443,1.446,1.446,1.446,1.446,1.446,1.446,1.449,1.449,1.449,1.449,1.449,1.452,1.452,1.452,1.452,1.452,1.452,1.455,1.455,1.455,1.458,1.455,1.455,1.455,1.458,1.455,1.458,1.458,1.458,1.461,1.458,1.461,1.458,1.461,1.461,1.464,1.464,1.464,1.464,1.464,1.464,1.464,1.464,1.467,1.467,1.467,1.467,1.467,1.467,1.467,1.467,1.47,1.47,1.47,1.47,1.47,1.47,1.47,1.47,1.47,1.47,1.473,1.473,1.473,1.473,1.473,1.473,1.473,1.476,1.476,1.476,1.476,1.473,1.476,1.476,1.476,1.476,1.476,1.476,1.476,1.479,1.476,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.482,1.482,1.479,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.485,1.482,1.482,1.482,1.482,1.482,1.485,1.482,1.482,1.482,1.482,1.485,1.482,1.482,1.482,1.485,1.485,1.485,1.482,1.485,1.485,1.485,1.482,1.482,1.485,1.485,1.485,1.485,1.485,1.485,1.485,1.485,1.485,1.482,1.482,1.485,1.482,1.485,1.485,1.485,1.485,1.485,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.482,1.479,1.482,1.479,1.479,1.479,1.479,1.479,1.482,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.479,1.476,1.476,1.476,1.476,1.476,1.476,1.476,1.476,1.476,1.476,1.476,1.473,1.476,1.476,1.476,1.476,1.473,1.473,1.473,1.473,1.473,1.473,1.473,1.47,1.473,1.473,1.473,1.473,1.47,1.473,1.47,1.47,1.47,1.47,1.47,1.47,1.47,1.47,1.467,1.467,1.467,1.467,1.467,1.467,1.467,1.467,1.467,1.467,1.464,1.464,1.464,1.464,1.464,1.464,1.464,1.464,1.461,1.464,1.461,1.461,1.461,1.461,1.461,1.461,1.461,1.461,1.461,1.461,1.461,1.458,1.458,1.458,1.458,1.458,1.458,1.458,1.458,1.458,1.455,1.455,1.455,1.455,1.455,1.455,1.455,1.455,1.455,1.455,1.455,1.452,1.452,1.452,1.452,1.452,1.452,1.452,1.449,1.449,1.449,1.449,1.452,1.449,1.449,1.449,1.449,1.449,1.449,1.446,1.449,1.446,1.446,1.446,1.446,1.446,1.446,1.443,1.446,1.443,1.443,1.443,1.443,1.443,1.443,1.443,1.443,1.443,1.44,1.44,1.44,1.44,1.44,1.44,1.44,1.44,1.44,1.437,1.437,1.437,1.437,1.437,1.437,1.437,1.437,1.437,1.437,1.437,1.434,1.434,1.434,1.434,1.434,1.434,1.434,1.434,1.434,1.431,1.431,1.431,1.431,1.431,1.431,1.431,1.431,1.431,1.428,1.428,1.428,1.428,1.428,1.428,1.428,1.428,1.428,1.425,1.425,1.425,1.425,1.425,1.425,1.422,1.425,1.422,1.422,1.422,1.422,1.422,1.419,1.419,1.422,1.422,1.422,1.419,1.419,1.419,1.419,1.419,1.419,1.419,1.419,1.419,1.416,1.419,1.419,1.416,1.416,1.416,1.416,1.416,1.416,1.413,1.413,1.413,1.416,1.416,1.413,1.413,1.413,1.413,1.413,1.413,1.413,1.41,1.413,1.41,1.41,1.41,1.41,1.41,1.41,1.41,1.41,1.41,1.41,1.407,1.407,1.407,1.407,1.407,1.407,1.407,1.407,1.407,1.404,1.407,1.404,1.404,1.404,1.404,1.404,1.404,1.404,1.404,1.401,1.404,1.404,1.401,1.401,1.401,1.401,1.401,1.401,1.401,1.401,1.401,1.398,1.398,1.401,1.398,1.398,1.398,1.398,1.398,1.398,1.398,1.398,1.395,1.395,1.395,1.398,1.395,1.395,1.395,1.395,1.392,1.395,1.395,1.392,1.395,1.395,1.392,1.392,1.392,1.395,1.392,1.392,1.392,1.392,1.392,1.392,1.392,1.389,1.389,1.389,1.389,1.389,1.392,1.389,1.389,1.389,1.389,1.389,1.389,1.386,1.386,1.386,1.386,1.386,1.389,1.386,1.386,1.386,1.386,1.386,1.386,1.386,1.386,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.383,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.38,1.377,1.377,1.377,1.377,1.377,1.377,1.377,1.377,1.377,1.374,1.374,1.377,1.377,1.374,1.374,1.374,1.374,1.374,1.377,1.374,1.374,1.374,1.374,1.374,1.374,1.374,1.371,1.374,1.374,1.374,1.374,1.374,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.371,1.368,1.371,1.368,1.368,1.371,1.368,1.368,1.368,1.368,1.368,1.368,1.368,1.368,1.365,1.365,1.365,1.368,1.368,1.368,1.365,1.368,1.365,1.365,1.365,1.365,1.365,1.365,1.365,1.368,1.365,1.365,1.365,1.365,1.365,1.362,1.365,1.365,1.365,1.365,1.365,1.365,1.365,1.365,1.365,1.362,1.365,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.362,1.359,1.362,1.359,1.362,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.359,1.356,1.359,1.359,1.356,1.359,1.359,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.356,1.353,1.356,1.356,1.356,1.353,1.353,1.356,1.356,1.353,1.356,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.353,1.35,1.35,1.353,1.353,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.35,1.347,1.35,1.35,1.35,1.35,1.35,1.347,1.35,1.35,1.347,1.347,1.35,1.347,1.35,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.35,1.347,1.347,1.347,1.347,1.35,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.347,1.344,1.344,1.344,1.347,1.344,1.347,1.347,1.344,1.347,1.344,1.347,1.347,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.347,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.344,1.341,1.344,1.341,1.344,1.344,1.341,1.344,1.344,1.344,1.341,1.344,1.344,1.341,1.344,1.344,1.344,1.341,1.344,1.341,1.341,1.341,1.341,1.341,1.344,1.341,1.344,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.344,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.338,1.341,1.341,1.341,1.341,1.341,1.338,1.341,1.341,1.338,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.341,1.338,1.341,1.338,1.338,1.338,1.341,1.338,1.338,1.338,1.341,1.338,1.341,1.341,1.338,1.338,1.338,1.338,1.338,1.341,1.341,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.338,1.335,1.338,1.338,1.335,1.335,1.335,1.338,1.338,1.338,1.338,1.335,1.335,1.338,1.335,1.335,1.335,1.338,1.338,1.338,1.338,1.338,1.338,1.335,1.335,1.335,1.338,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.338,1.335,1.338,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.332,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.332,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.335,1.332,1.335,1.335,1.335,1.332,1.335,1.332,1.335,1.332,1.335,1.332,1.335,1.335,1.335,1.332,1.335,1.335,1.332,1.335,1.335,1.335,1.335,1.335,1.332,1.332,1.332,1.335,1.332,1.332,1.335,1.332,1.332,1.332,1.332,1.335,1.335,1.332,1.332,1.332,1.332,1.332,1.335,1.332,1.335,1.332,1.332,1.332,1.335,1.335,1.332,1.332,1.332,1.335,1.332,1.332,1.335,1.332,1.332,1.332,1.332,1.332,1.335,1.332,1.335,1.335,1.332,1.335,1.332,1.335,1.332,1.332,1.332,1.332,1.335,1.332,1.332,1.332,1.335,1.332,1.335,1.332,1.332,1.332,1.332,1.332,1.332,1.335,1.332,1.335,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.335,1.335,1.332,1.332,1.332,1.332,1.335,1.332,1.332,1.332,1.335,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.329,1.332,1.332,1.332,1.332,1.332,1.329,1.329,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.329,1.332,1.329,1.329,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.329,1.332,1.329,1.332,1.332,1.329,1.329,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.329,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.329,1.329,1.332,1.329,1.329,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.329,1.332,1.332,1.329,1.332,1.332,1.332,1.329,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.332,1.329]
           liveGraph.plot(xVal,yVal)
           progress.setValue(100)
           break
        
        global are_machine_learning
        if are_machine_learning == "NO":
           
            H2s_undefined.setStyleSheet("QLabel {font:13px; border: 2px solid black; background-color: orange}")
        self.setEnabled(True) 
        
        v1.setEnabled(True)
        
        v2.setEnabled(True)
        
        v3.setEnabled(True)
       
        v4.setEnabled(True)
        
        v5.setEnabled(True)
        
        v6.setEnabled(True)
        cb.setEnabled(True)
        purgeB.setEnabled(True) 
        global app 
       
        pumpB.setEnabled(True)
        
        heaterB.setEnabled(True)
        global printing
        global linearAc
        
        global stepperB
        
        
        
        mos.setEnabled(True)
       
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
schem1 = schematic("/Users/EmilyEarl/Downloads/attachments/v1b.png","/Users/EmilyEarl/Downloads/attachments/v1a.png")
schem2 = schematic("/Users/EmilyEarl/Downloads/attachments/v2b-2.png", "/Users/EmilyEarl/Downloads/attachments/v2a-2.png")
schem3 = schematic("/Users/EmilyEarl/Downloads/attachments/v3b.png", "/Users/EmilyEarl/Downloads/attachments/v3a.png")
schem4 = schematic("/Users/EmilyEarl/Downloads/attachments/v4b.png","/Users/EmilyEarl/Downloads/attachments/v4a.png")
schem5 = schematic("/Users/EmilyEarl/Downloads/attachments/v5dis.png","/Users/EmilyEarl/Downloads/attachments/v5en.png")
schem6 = schematic("/Users/EmilyEarl/Downloads/attachments/v6dis.png","/Users/EmilyEarl/Downloads/attachments/v6en.png")

v1 = valve_Button(1,schem1)
v2 = valve_Button(2, schem2)
v3 = valve_Button(3, schem3)
v4 = valve_Button(4, schem4)
v5 = valve_Button(5, schem5)
v6 = valve_Button(6, schem6)
heaterB = heater_Button()
pumpB = pump_Button()
linearAc = linAc_Button()
stepperB = stepper_Button()
stepperB2 = stepper_Button()
mos = mos_Button()
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
