# >>> GUI Imports <<<
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
# >>> Numpy <<<
import numpy as np
import math
# >>> System Imports <<<
import sys
import datetime
import time
from pathlib import Path
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

global timeLabel
global concInput
global testSelect
global liveGraph
global mainButton
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k') 
cont = False

projFile = r'/home/pi/Documents/Volded/'
adc1 = Adafruit_ADS1x15.ADS1115(address = 0x48)

def collect_data(type,concentration):
    global liveGraph
    global timeLabel
    global cont
    global mainButton
    dataVector1 = []  # data values to be returned from sensor 1
    timeVector = []  # time values associated with data values
    start_time = time.time()

    while (time.time()<(start_time+201)) and cont:
        dataVector1.append((adc1.read_adc(3, gain=2/3)/pow(2, 15)*6.144))
        timeVector.append(time.time() - start_time)
        timeLabel.setText(str(time.time() - start_time))
        update_Graph(timeVector,dataVector1)
        app.processEvents()
        time.sleep(0.1)

    combinedVector = np.column_stack((timeVector, dataVector1))
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute

    fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute)
    
    
    if type == 'Methanol' and cont:
        fileName = 'Methanol/' + fileName + '_M'+ str(concentration) +'.csv'
        np.savetxt(str(projFile)+str(fileName), combinedVector, fmt='%.10f', delimiter=',')
    elif type == 'Ethanol' and cont:
        fileName = 'Ethanol/' + fileName + '_E' + str(concentration) + '.csv'
        np.savetxt(str(projFile)+str(fileName), combinedVector, fmt='%.10f', delimiter=',')
    elif type == 'Examine' and cont:
        fileName = 'Examine/' + fileName + '_NULL.csv'
        np.savetxt(str(projFile)+str(fileName), combinedVector, fmt='%.10f', delimiter=',')
    else:
        pass
    app.processEvents()
    print('Ended')
    cont = False
    mainButton.setText('Run')
    timeLabel.setText('---')

def update_Graph(xList,yList):
    global liveGraph

    liveGraph.plot(xList,yList)
    app.processEvents()

def update_Volume():
    global volOutput
    global concInput
    global testSelect
    concentration = concInput.text()
    test = testSelect.currentText()

    if concentration == "":
        return
    pressure = 96000 #Pa
    temperature = 24.5 #C
    gas_constant = 8.314
    vol_chamber = 0.009938375 #m^3
    Ct = pressure/(gas_constant*(temperature+273.15))
    Cip = (int(concentration) * Ct)/(10**6)
    app.processEvents()

    if test == 'Methanol':
        density = 792 #Kg/m3
        MW = 32.04 #g/mol
        sampleVolume = MW*vol_chamber/(density*1000)*Cip*(10**9)
    if test == 'Ethanol':
        density = 789 #Kg/m3
        MW = 46.07 #g/mol
        sampleVolume = MW*vol_chamber/(density*1000)*Cip*(10**9)
    if test == 'Examine':
        sampleVolume = '---'

    volOutput.setText(str(sampleVolume))
    app.processEvents()


class live_Graph(pg.PlotWidget):
    def __init__(self,parent=None):
        super(live_Graph,self).__init__()
        self.setRange(xRange=(0,300),yRange=(0,5),disableAutoRange=False)
        self.enableAutoScale()
        self.setTitle("Live Graph")
        self.setStyleSheet("pg.PlotWidget {border-style: outset; max-height: 50}")

class MainButton(QtWidgets.QPushButton):
    def __init__(self,parent=None):
        super(MainButton,self).__init__()
        self.setText('Run')
        self.clicked.connect(lambda: self.run_test())

    def run_test(self):
        print('Send help.')
        global concInput
        global testSelect
        global liveGraph
        global cont
        if cont == False:
            cont = True
            concentration = concInput.text()
            test = testSelect.currentText()
            self.setText('Stop')
            collect_data(str(test),concentration)
        elif cont == True:
            cont = False
            self.setText('Run')
        else:
            pass
        

class ResetButton(QtWidgets.QPushButton):
    def __init__(self,parent=None):
        super(ResetButton,self).__init__()
        self.setText('Reset graph')
        self.clicked.connect(lambda: self.reset())

    def reset(self):
        print('Graph reset')
        global liveGraph
        liveGraph.clear()

class METest(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("METest")
        MainWindow.setEnabled(True)

        global concInput
        global volOutput
        global timeLabel
        global testSelect
        global liveGraph
        global mainButton

        width = 800
        height = 600
        MainWindow.resize(width, height)
        MainWindow.setMinimumSize(QtCore.QSize(width, height))
        MainWindow.setMaximumSize(QtCore.QSize(width, height))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.pLayout = QtWidgets.QGridLayout() #Defines layout format.
        self.pLayout.setSpacing(10)

        liveGraph = live_Graph()
        mainButton = MainButton()
        resetButton = ResetButton()
        concInput = QtWidgets.QLineEdit()
        concLabel = QtWidgets.QLabel()
        volOutput = QtWidgets.QLabel()
        volLabel = QtWidgets.QLabel()
        timeLabel = QtWidgets.QLabel()

        testSelect = QtWidgets.QComboBox()

        test_types = ['Examine','Methanol','Ethanol']
        testSelect.addItems(test_types)
        concLabel.setText('PPM:')
        volLabel.setText('Volume:')
        timeLabel.setText('---')

        concInput.editingFinished.connect(update_Volume)
        testSelect.currentIndexChanged.connect(update_Volume)

        self.pLayout.addWidget(liveGraph,0,0,1,2)
        self.pLayout.addWidget(testSelect,1,0,1,2)
        self.pLayout.addWidget(concInput,2,1,1,1)
        self.pLayout.addWidget(concLabel,2,0,1,1)
        self.pLayout.addWidget(volOutput,3,1,1,1)
        self.pLayout.addWidget(volLabel,3,0,1,1)
        self.pLayout.addWidget(mainButton,4,0,1,1)
        self.pLayout.addWidget(timeLabel,4,1,1,1)
        self.pLayout.addWidget(resetButton,5,0,1,2)

        self.centralwidget.setLayout(self.pLayout)

try:
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = METest()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
finally:
    GPIO.cleanup()
    print('GPIO cleaned up.')
