## Hamed Code V2.0

#!/usr/bin/python3
import numpy
import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
import sys
import time

global personInput
personInput = 0
global dipPersonInput
dipPersonInput = 0 
global startButton
global app
global continueR
global stopButton
global extendVal
global repeat
repeat = 0
global progress
global stopButtonMain
global startTime
global totalTime
totalTime = 0
class linearActuator():
    def __init__(self, pinNum, enable):
        self.pinNum = pinNum
        self.enable = enable
        GPIO.setup(self.pinNum, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.output(self.enable, GPIO.HIGH)
        self.pwm = GPIO.PWM(self.pinNum, 50)
        self.pwm.start(9)
        time.sleep(5)
        GPIO.output(self.enable, GPIO.LOW) 
        self.state = 'default'
        
    def extend(self):
        global extendVal
        if self.state != 'extended':
            GPIO.output(self.enable, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(9)
            time.sleep(5)
            GPIO.output(self.enable, GPIO.LOW) 
            self.state = 'extended'
        else:
            pass
    def retract(self):
        if self.state != 'retracted':
            GPIO.output(self.enable, GPIO.HIGH) 
            self.pwm.ChangeDutyCycle(float(extendVal))
            time.sleep(5)
            GPIO.output(self.enable, GPIO.LOW) 
            self.state = 'retracted'
        else:
            pass
    def submerge(self):
        global dipPersonInput
        self.seconds = dipPersonInput
        self.retract()
        global app
        app.processEvents()
        self.state = 'retracted'
        start_time = time.time()
        while(time.time() - start_time) < int(self.seconds):
            pass
        self.extend()
        self.state = 'extended'
            

class servo():
    def __init__(self, pinNum, name):
        self.pinNum = pinNum
        GPIO.setup(self.pinNum, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pinNum, 50)
        self.state = 'disabled'
        self.name = name
        
        
        
    def move_Servo(self):
        self.state = 'enabled'
        self.pwm.start(0.1) 
        self.pwm.ChangeDutyCycle(0.5)
    def stop_Servo(self):
        self.state = 'disabled'
        self.pwm.stop() 
        
class servos():
    def __init__(self, servo1, servo2, servo3, servo4):
        self.s1 = servo1
        self.s2 = servo2
        self.s3 = servo3
        self.s4 = servo4
        
    def move_All_Servos(self):
        global personInput
        self.seconds = personInput 
    
        self.s1.state = 'enabled'
        self.s2.state = 'enabled'
        self.s3.state = 'enabled'
        self.s4.state = 'enabled'
        self.s1.pwm.start(0.1)
        self.s2.pwm.start(0.1)
        self.s3.pwm.start(0.1)
        self.s4.pwm.start(0.1)
        self.start_time = time.time()
        global continueR
        continueR = True
        while (time.time() - self.start_time) < int(self.seconds):
        
            self.s1.pwm.ChangeDutyCycle(0.5)
            self.s2.pwm.ChangeDutyCycle(0.5)
            self.s3.pwm.ChangeDutyCycle(0.5)
            self.s4.pwm.ChangeDutyCycle(0.5)
            global app
            app.processEvents()
            if (continueR == False):
                break
        self.s1.pwm.stop()
        self.s2.pwm.stop()
        self.s3.pwm.stop()
        self.s4.pwm.stop()
        self.s1.state = 'disabled'
        self.s2.state = 'disabled'
        self.s3.state = 'disabled'
        self.s4.state = 'disabled'
        global startButton
        startButton.setEnabled(True)
        startButton.setText("Begin Rotation")
        stopButton.setEnabled(False) 
        
    def move_All_Servos_Main(self):
        global personInput
        self.seconds = personInput 
    
        self.s1.state = 'enabled'
        self.s2.state = 'enabled'
        self.s3.state = 'enabled'
        self.s4.state = 'enabled'
        self.s1.pwm.start(0.1)
        self.s2.pwm.start(0.1)
        self.s3.pwm.start(0.1)
        self.s4.pwm.start(0.1)
        self.start_time = time.time()
        global continueR
        continueR = True
        while (time.time() - self.start_time) < int(self.seconds):
        
            self.s1.pwm.ChangeDutyCycle(0.5)
            self.s2.pwm.ChangeDutyCycle(0.5)
            self.s3.pwm.ChangeDutyCycle(0.5)
            self.s4.pwm.ChangeDutyCycle(0.5)
            global progress
            global startTime
            global totalTime
            progress.setValue((time.time() - startTime)/totalTime*100)
            global app
            app.processEvents()
            if (continueR == False):
                break
        self.s1.pwm.stop()
        self.s2.pwm.stop()
        self.s3.pwm.stop()
        self.s4.pwm.stop()
        self.s1.state = 'disabled'
        self.s2.state = 'disabled'
        self.s3.state = 'disabled'
        self.s4.state = 'disabled'
        
        

class linAc_Button(QPushButton):
    def __init__(self, linAc, parent=None):
        super(linAc_Button, self).__init__()
        self.linAc = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Dip")
        self.state = "retracted"
        self.clicked.connect(lambda: self.linAc_Switch())
    def linAc_Switch(self):
        if self.state == "retracted":
            self.setText("Remove")
            self.state = "extended"
            self.linAc.extend()
        elif self.state == "extended":
            self.setText("Dip")
            self.state = "retracted"
            self.linAc.retract()
            
class submerge_Button(QPushButton):
    def __init__(self, linAc, parent=None):
        super(submerge_Button, self).__init__()
        self.linAc = linAc
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Submerge")
        self.state = 'retracted'
        self.clicked.connect(lambda: self.submerge())
        
    def submerge(self):
        global dipPersonInput
        self.seconds = dipPersonInput
        self.linAc.retract()
        self.setText("Coating...")
        self.setEnabled(False)
        global app
        app.processEvents()
        self.state = 'retracted'
        start_time = time.time()
        while(time.time() - start_time) < int(self.seconds):
            pass
        self.linAc.extend()
        self.state = 'extended'
        self.setText("Submerge")
        self.setEnabled(True)
            
class servo_Start(QPushButton):
    def __init__(self, servo1, servo2, servo3, servo4, ss, parent=None):
        super(servo_Start, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Begin Rotation")
        self.ss = ss
        self.s1 = servo1
        self.s2 = servo2
        self.s3 = servo3
        self.s4 = servo4
        self.servos = servos(self.s1, self.s2, self.s3, self.s4)
        self.setEnabled(True)
        self.clicked.connect(lambda: self.switch_Servo())
        
        self.clicked.connect(lambda:self.servos.move_All_Servos())
        
    def switch_Servo(self):
        self.setEnabled(False)
        self.ss.setEnabled(True)
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Rotating...")
        
        global app
        app.processEvents()
#        self.servos.move_All_Servos(self.seconds)


class servo_Stop(QPushButton):
    def __init__(self, servo1, servo2, servo3, servo4, parent=None):
        super(servo_Stop, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Emergency Stop")
        self.servos = servos(servo1, servo2, servo3, servo4)
        self.setEnabled(False)
        self.clicked.connect(lambda: self.stop_Servo())
        
    def stop_Servo(self):
        #self.servos.emerg_Stop()
        self.setEnabled(False)
        global startButton
        startButton.setEnabled(True)
        global continueR
        continueR = False
        
        
            
class servo_Hold(QPushButton):
    def __init__(self, servo, parent = None):
        super(servo_Hold, self).__init__()
        self.servo= servo
        self.setCheckable(True) 
        self.setStyleSheet("QPushButton {font:13px}")
        self.setText(self.servo.name)
        self.pressed.connect(lambda: self.servo_Rotate())
        self.released.connect(lambda: self.servo_Stop())
    
    def servo_Rotate(self):
        self.servo.move_Servo()
    def servo_Stop(self):
        self.servo.stop_Servo()
        
class repeat(QPushButton):
    def __init__(self,servo1, servo2, servo3, servo4, linAc, parent = None):
        super(repeat, self).__init__()
        self.s1 = servo1
        self.s2 = servo2
        self.s3 = servo3
        self.s4 = servo4
        self.linAc = linAc
        self.servos = servos(self.s1,self.s2,self.s3,self.s4)
        self.setStyleSheet("QPushButton {font:13px}")
        self.setText("Begin Cycling")
        self.pressed.connect(lambda: self.cycling())
        
    def cycling(self):
        self.setEnabled(False)
        global stopButtonMain
        stopButtonMain.setEnabled(True)
        global app
        app.processEvents()
        global startTime
        startTime = time.time()
        global totalTime
        global personInput
        global dipPersonInput
        global repeat
        totalTime = (int(dipPersonInput) + 4 + int(personInput))*int(repeat)
        
                                     
        global repeat
        count = 0
        while count < int(repeat):
            ## Step 1. Sumberge
            self.linAc.submerge()
            global progress
            
            progress.setValue((time.time() - startTime)/totalTime*100)
            global app
            app.processEvents()
            ## Step 2. Spin
            self.servos.move_All_Servos_Main()
            global app
            app.processEvents()
            if continueR == False:
                break
            count = count +1
        self.setEnabled(True)
        global stopButtonMain
        stopButtonMain.setEnabled(False)
        global progress 
        progress.setValue(0)
        
        
        
GPIO.setmode(GPIO.BOARD) 
app = QApplication([])
app.setStyle('Fusion')

mainPage = QTabWidget()
mainPage.setWindowTitle("Dipping Machine") 
mainPage.resize(600, 400)

def textChanged(text):
    global personInput
    personInput = text
    print (personInput)
def dipTextChanged(text):
    global dipPersonInput
    dipPersonInput = text
    print(dipPersonInput)
def extendChanged(text):
    global extendVal
    extendVal = text
    print(extendVal) 
def repChanged(text):
    global repeat
    repeat = text
    print(repeat) 

   
descriptor = QLabel()
descriptor.setText("Number of Seconds for Servo Rotation: ")
dipDescriptor = QLabel()
dipDescriptor.setText("Number of Seconds for Coating: ")
exDescriptor = QLabel()
exDescriptor.setText("Linear Actuator Depth (5-10): ")
editSpace = QLineEdit()
editSpace.textChanged.connect(textChanged)
dipEditSpace = QLineEdit()
dipEditSpace.textChanged.connect(dipTextChanged)
exEditSpace = QLineEdit()
exEditSpace.textChanged.connect(extendChanged) 
blank  = QLabel()
blank.setText("")

descriptor2 = QLabel()
descriptor2.setText("Number of Seconds per Servo Rotation Cycle: ")
dipDescriptor2 = QLabel()
dipDescriptor2.setText("Number of Seconds Submerged per Cycle: ")
exDescriptor2 = QLabel()
exDescriptor2.setText("Linear Actuator Depth (5-10): ")
editSpace2 = QLineEdit()
editSpace2.textChanged.connect(textChanged)
dipEditSpace2 = QLineEdit()
dipEditSpace2.textChanged.connect(dipTextChanged)
exEditSpace2 = QLineEdit()
exEditSpace2.textChanged.connect(extendChanged)
repetitions = QLabel()
repetitions.setText("Number of Cycles: ")
repEditSpace = QLineEdit()
repEditSpace.textChanged.connect(repChanged)



## Data Page Initiation 
firstPage = QWidget()
fpLayout = QGridLayout()
servo1 = servo(8, "Servo 1")
servo2 = servo(22, "Servo 2")
servo3 = servo(12, "Servo 3")
servo4 = servo(18, "Servo 4")
linAc = linearActuator(16,10)
linAcB = submerge_Button(linAc)
progress = QProgressBar()
stopButton = servo_Stop(servo1,servo2,servo3,servo4)
startButton = servo_Start(servo1,servo2,servo3,servo4, stopButton)
stopButtonMain = servo_Stop(servo1,servo2,servo3,servo4)
mainButton = repeat(servo1,servo2,servo3,servo4,linAc)
fpLayout.addWidget(exDescriptor2, 1,1)
fpLayout.addWidget(exEditSpace2,1,2)
fpLayout.addWidget(dipDescriptor2, 2,1)
fpLayout.addWidget(dipEditSpace2, 2,2)
fpLayout.addWidget(descriptor2,3,1)
fpLayout.addWidget(editSpace2,3,2)
fpLayout.addWidget(repetitions, 4,1)
fpLayout.addWidget(repEditSpace,4,2)
fpLayout.addWidget(mainButton,5,1)
fpLayout.addWidget(stopButtonMain,5,2)
fpLayout.addWidget(progress,6,1,1,2)
firstPage.setLayout(fpLayout)

## Manual Page Initiation
secondPage = QWidget()
spLayout = QGridLayout()
servo1B = servo_Hold(servo1)
servo2B = servo_Hold(servo2)
servo3B = servo_Hold(servo3)
servo4B = servo_Hold(servo4)

spLayout.addWidget(dipDescriptor,1,1)
spLayout.addWidget(dipEditSpace,1,2)
spLayout.addWidget(exDescriptor,2,1)
spLayout.addWidget(exEditSpace,2,2)
spLayout.addWidget(linAcB,3,1,1,2)
spLayout.addWidget(blank,4,1)
spLayout.addWidget(descriptor,5,1)
spLayout.addWidget(editSpace,5,2)
spLayout.addWidget(startButton,6,1)
spLayout.addWidget(stopButton,6,2)
spLayout.addWidget(blank,7,1) 
spLayout.addWidget(servo1B,8,1)
spLayout.addWidget(servo2B,8,2)
spLayout.addWidget(servo3B,9,1)
spLayout.addWidget(servo4B,9,2) 

secondPage.setLayout(spLayout) 

mainPage.addTab(firstPage, "Automated Controls")
mainPage.addTab(secondPage, "Manual Controls") 

mainPage.show()
app.exec_()
linAc.pwm.stop()
GPIO.cleanup() 