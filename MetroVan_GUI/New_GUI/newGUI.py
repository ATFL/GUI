#!/usr/bin/python3
import numpy
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph
import sys

## GUI Functions

class heater_Button(QPushButton):
    def __init__(self, parent=None):
        super(heater_Button, self).__init__()
        
        self.green = QtGui.QIcon("/home/pi/Downloads/object_On.png")
        self.red = QtGui.QIcon("/home/pi/Downloads/object_Off.png")
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
    def __init__(self, num, parent=None):
        super(valve_Button, self).__init__()
        self.setText("Valve "+ str(num) + " Mode")
        self.state = "A"
        self.A = QtGui.QIcon("/home/pi/Downloads/valveA.svg")
        self.B = QtGui.QIcon("/home/pi/Downloads/valveB.svg")
        self.setIcon(self.A)
        self.clicked.connect(lambda: self.valve_Switch())
    def valve_Switch(self):
        if self.state == "A":
            self.setIcon(self.B)
            self.state = "B"
        elif self.state == "B":
            self.setIcon(self.A)
            self.state = "A"
    
class pump_Button(QPushButton):
    def __init__(self, parent=None):
        super(pump_Button, self).__init__()
        self.setText("Pump Off")
        self.state = "off"
        self.green = QtGui.QIcon("/home/pi/Downloads/object_On.png")
        self.red = QtGui.QIcon("/home/pi/Downloads/object_Off.png")
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
        self.layout = QGridLayout()
        self.title = QLabel("Linear Actuator")
        self.layout.addWidget(self.title, 1,1)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(5.8)
        self.slider.setMaximum(10.8)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(0.2)
        #self.setText("Linear Actuator")
        self.slider.setValue(7.8)
        self.slider.sliderReleased.connect(self.move_Actuator)
        self.layout.addWidget(self.slider, 2,1)
        self.setLayout(self.layout)
    def move_Actuator(self):
        self.number = self.slider.value()
        print(self.number) 

class schematic(QWidget):
    def __init__(schematic, parent=None):
        super(schematic, self).__init__()
        
        
## Main Page Initiation
app = QApplication([])
mainPage = QTabWidget()
mainPage.setWindowTitle("MetroVan Sample Analysis") 
mainPage.resize(600, 350)
## Data Page Initiation 
firstPage = QWidget()

## Manual Controls Page Initiation 
secondPage = QWidget()
spLayout = QGridLayout() 
v1 = valve_Button(1)
v2 = valve_Button(2)
v3 = valve_Button(3)
v4 = valve_Button(4)
v5 = valve_Button(5)
heaterB = heater_Button()
pumpB = pump_Button()
linearAc = linAc_Button()
schem1 = QLabel()
schem1.setScaledContents(True)
schem2 = QLabel()
schem2.setScaledContents(True)
schematic = QPixmap("/home/pi/Downloads/object_Off.png")
schematic2 = QPixmap("/home/pi/Downloads/object_On.png")
schem1.setPixmap(schematic)
schem2.setPixmap(schematic2)
spLayout.addWidget(v1, 1,1,1,1)
spLayout.addWidget(v2, 2,1,1,1)
spLayout.addWidget(v3, 3,1,1,1)
spLayout.addWidget(v4, 4,1,1,1)
spLayout.addWidget(v5, 5,1,1,1)
spLayout.addWidget(heaterB, 6,1,1,1)
spLayout.addWidget(pumpB,7,1,1,1)
spLayout.addWidget(linearAc,8,1,1,1)
spLayout.addWidget(schem1, 1,2, 6,2)
spLayout.addWidget(schem2, 1,2,6,2)

secondPage.setLayout(spLayout)



mainPage.addTab(firstPage, "Sensor Response")
mainPage.addTab(secondPage, "Manual Controls") 

mainPage.show()
app.exec_()

