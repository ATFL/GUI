import numpy
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import random
import sys
import time
from Metrovan_components import *
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ads
import busio
import adafruit_bme280
import digitalio
import Adafruit_MAX31855
import board

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Yes'))
layout.addWidget(QPushButton('No'))
window.setLayout(layout)
window.show()
app.exec_()