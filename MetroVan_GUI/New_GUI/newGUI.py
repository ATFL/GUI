#!/usr/bin/python3
import numpy
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
import sys
import time
from Metrovan_components import * 


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
global app 
global v1
global v2
global v3
global v4 
global v5
global v6
global pump 
global heaterB
global pumpB
global printing
global linearAc 
global steppB
global liveGraph 
global progress
global emergencyStop 
emergencyStop = "RUN"


class heater_Button(QPushButton):
    def __init__(self, parent=None):
        super(heater_Button, self).__init__()
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px; max-height: 20px}")
        # Must be changed if working on Raspberry Pi or personal Laptop
        self.green = QtGui.QIcon("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/on.svg")
        # Must be changed if working on Raspberry Pi or personal laptop
        self.red = QtGui.QIcon("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/off.svg")
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
        self.A = QtGui.QIcon("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/A.svg")
        self.B = QtGui.QIcon("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/B.svg")
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
    
class pump_Button(QPushButton):
    def __init__(self, parent=None):
        super(pump_Button, self).__init__()
        self.setIconSize(QSize(15,15))
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Pump Off")
        self.state = "off"
        # Must be changed if working on Raspberry pi or personal laptop
        # Must be changed if working on Raspberry Pi or personal laptop
        self.green = QtGui.QIcon("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/on.svg")
        self.red = QtGui.QIcon("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/off.svg")
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

class mos_Button(QPushButton):
    def __init__(self,parent=None):
        super(mos_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Read MOS")
        self.clicked.connect(lambda: self.read_MOS()) 
    def read_MOS(self):
        print("MOS Value: ")
        
class cleanse_Button(QPushButton):
    def __init__(self, parent=None):
        super(cleanse_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Cleanse Lines")
        self.clicked.connect(lambda: self.cleanse_Lines())
    def cleanse_Lines(self):
        print("Cleaning Lines") 

class purge_Button(QPushButton):
    def __init__(self,parent=None):
        super(purge_Button, self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Purge Chamber")
        self.clicked.connect(lambda: self.purge_Chamber())
    def purge_Chamber(self):
        print("Purging Chamber")
        
class live_Graph(pg.PlotWidget):
    def __init__(self,parent=None):
        super(live_Graph,self).__init__()
        #self.setBackgroundColor(None)
        self.setRange(xRange=(0,300),yRange=(0,5),disableAutoRange=True)
        self.setTitle("Live Graph")
        self.setStyleSheet("pg.PlotWidget {border-style: outset; max-height: 50}")
        
class start_Button(QPushButton):
    def __init__(self,parent=None):
        super(start_Button,self).__init__()
        self.setStyleSheet("QPushButton {font: 13px}")
        self.setText("Start")
        self.clicked.connect(lambda: self.start_Procedure())
    def start_Procedure(self):
        global emergencyStop 
        emergencyStop = "RUN" 
        print("Starting Test...")
        global liveGraph
        liveGraph.clear()
        plot_Random(liveGraph)
        
        
        
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
            
            
class update_Graph():
    def __init__(self, xlist, ylist):
        xData = pyqtSignal(list)
        yData = pyqtSignal(list)
    
            
        
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
fpLayout.addWidget(startB,3,1)
fpLayout.addWidget(stopB,3,2)
fpLayout.addWidget(printing,5,1,1,2)
fpLayout.addWidget(liveGraph,1,1,2,2)
fpLayout.addWidget(progress, 4,1,1,2)
firstPage.setLayout(fpLayout)

## Manual Controls Page Initiation 
secondPage = QWidget()
spLayout = QGridLayout()
spLayout.setVerticalSpacing(0)
# Must be changed if working on raspberry pi or personal laptop
schem1 = schematic("/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/on.svg","/Users/EmilyEarl/Documents/ATFL/GUI/GUI/MetroVan_GUI/New_GUI/off.svg")
v1 = valve_Button(1,schem1)
v2 = valve_Button(2, schem1)
v3 = valve_Button(3, schem1)
v4 = valve_Button(4, schem1)
v5 = valve_Button(5, schem1)
v6 = valve_Button(6, schem1)
heaterB = heater_Button()
pumpB = pump_Button()
linearAc = linAc_Button()
steppB = stepper_Button()
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
spLayout.addWidget(steppB, 2,2)
spLayout.addWidget(mos,3,2)
spLayout.addWidget(cb, 4,2)
spLayout.addWidget(purgeB,5,2)
spLayout.addWidget(schem1, 1,3, 7,2)


secondPage.setLayout(spLayout)



mainPage.addTab(firstPage, "Sensor Response")
mainPage.addTab(secondPage, "Manual Controls") 

mainPage.show()
app.exec_()

