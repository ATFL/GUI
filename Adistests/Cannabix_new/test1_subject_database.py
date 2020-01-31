#MAC COMPATIBLE IMPORTS
import numpy as np
from PyQt5 import QtWidgets, QtGui, QTCore
from PyQT5.QtWidgets import *
from PyQT5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
import random
import sys
import time
import datetime

#RPI only imports
import Adafruit_ADS1x15 as ads

class nsButton(QPushButton):
    def __init__(self,parent=None):
        super(nsButton,self).__init__()
        self.setStyleSheet("QPushButton {font:13px}")
        self.setText("Add New Subject")
        self.clicked.connect(lambda:self.add_new_s())

    def add_new_s(self):
        print('New Subject Added')


class lsButton(QPushButton):
    def __init__(self,parent=None):
        super(nsButton,self).__init__()
        self.setStyleSheet("QPushButton {font:13px}")
        self.setText("Load Existing Subject")
        self.clicked.connect(lambda:self.add_new_s())

    def add_new_s(self):
        print('Old Subject Loaded')


app = QApplication([])
app.setStyle('Fusion')

subjectPage = QWidget()
subjectPage.setWindowTitle('Subject Options')
subjectPage.resize(800,600)
newSubject_button = nsButton()
loadSubject_button = lsButton()
pageLayout = QGridLayout()
pageLayout.addWidget(newSubject_button)
pageLayout.addWidget(loadSubject_button)
subjectPage.setLayout(pageLayout)
subjectPage.show()
app.exec()
