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
import adafruit_max31855
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
global peri_pumpB
global cb
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
totalTime = 600
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
    ## Start purging the dirty side 
    

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
    


class servo_Button(QWidget):
    def __init__(self, servo, parent=None):
        super(servo_Button, self).__init__(parent)
        self.servo = servo
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
