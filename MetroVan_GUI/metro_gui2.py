#!/usr/bin/python3
#Last edit: 28/05/2019
# -----> System Imports <-----
import os
import sys
from time import *
import datetime
import shutil
import threading
# -----> Tkinter Imports <------
import tkinter as tk
from tkinter import ttk
# -----> Matplotlib Imports <------
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
# -----> Auxiliary Imports <------
from gui_widgets import *
from Metrovan_components import *
# -----> RPi Imports <------
import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15 as ads
import serial
from pathlib import Path
# ----->Metrovan Specific Imports <------
import busio
import adafruit_bme280
import adafruit_bme280_76
import digitalio
import adafruit_max31855
import board

#---->
import numpy as np
# import sklearn
# import pickle


def createFolders(year, month, day):
    ##  Get the path for the folders by year, month and day
    year_path = '/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/' + str(year)
    year_folder = Path(year_path)
    month_path = '/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/' + str(year) + '/' + str(month)
    month_folder = Path(month_path)
    day_path = '/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/' + str(year) + '/' + str(month) + '/' + str(day)
    day_folder = Path(day_path)
    ##  Start creating the folders, when the var complete == True, all the folders have been created
    complete = False
    while complete == False:
        if year_folder.is_dir():
            if month_folder.is_dir():
                if day_folder.is_dir():
                    complete = True
                else:
                    try:
                        print(day_path)
                        original_mask = os.umask(0x0000)
##                        desired_permission = 0777
                        os.makedirs(day_path, mode=0x0777)
                        complete = True
                    finally:
                        os.umask(original_mask)
            else:
                os.makedirs(month_path)
        else:
            os.makedirs(year_path)
    pass

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
MOS_adc_channel = 1
mos = MOS(adc, MOS_adc_channel)
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
valve1 = Valve('Valve1',pinvalve1) #Methane Tank to MFC
valve2 = Valve('Valve2',pinvalve2) #H2 Tank to MFC
valve3 = Valve('Valve3',pinvalve3) #Sample Gas into Chamber
valve4 = Valve('Valve4',pinvalve4) #Air into Chamber
valve5 = Valve('Valve5',pinvalve5) #Chamber Exhaust

#Stepper Motor Information
# Need to convert from BCM to BOARD 
DIR = 25   # Direction GPIO Pin
STEP = 24  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 400   # Steps per Revolution (360 / 7.5)
MODE = (15, 18, 23)   # Microstep Resolution GPIO Pins
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}

Stepper_Motor = StepperMotor(DIR, STEP, CW, CCW, SPR, MODE, RESOLUTION) 


#Max31855
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D21)
max31855 = adafruit_max31855.MAX31855(spi, cs)

# Bme280 (I2C Network)
# First BME 
##i2c = busio.I2C(board.SCL, board.SDA)
##bme280 = adafruit_bme280_76.Adafruit_BME280_I2C(i2c)
### Second BME 
##bme280_2 = adafruit_bme280.Adafruit_BME280_I2C(i2c)


################## EXPERIMENTAL STEPS METROVAN ################
# Low = b 
# High = a 

##EXTRACTION == Fill Thread?
    #V1-a
    #v2-a
    #v3-a
    #v4-b
    #stepper retract
    #v3-b

    
## Vaporization Test
# Vaporization Test == Data Capture Thread? 
    #Heater on
    #sleep(240)
    #Heater off
    #LA Extend
    #Data Capture
    #LA Retract (Continue Data capture)
    #sleep(__)
    #Finish data capture

##Cleanse == ?? Need to make new thread? 
    #v1-a
    #v2-a
    #v3-a
    #v4-b
    #v5-a

    #Repeat x times
        
        #stepper retract
        #v3-b
        #stepper extend
        #v3-a

    #v3-b
    #v2-b
    #pump on
    #sleep(_short time_)
    #v4-a
    #pump off
    #Heater on   -  maybe earlier
    #sleep(60)
    #Heater off

##Purge == Purge Thread
    #v5-b
    #pump on
    #sleep(__)
    #pump off
    #v5-a


#################### System Variables ####################



##############################################################
######## SAMPLE INJECTION CONCENTRATIONS #####################
methane_injection_conc = [80,160] #Whatever vales you need
hydrogen_injection_conc = [20,40] #whatever values you need

# methane_injection_conc=[80,160,240,320,400,480,560,640,720,800]
# hydrogen_injection_conc=[20,40,60,80,100,120,140,160,180,200]
##############################################################
##############################################################
def findDaBaseline():
    global baseline
    baseline_counter = 1
    baseline_val = 0
    while baseline_counter < 101:
        baseline_val += mos.read()
        baseline_counter +=1
    baseline = baseline_val/baseline_counter
    return baseline
global test_counter
test_counter = 0
global num_tests
num_tests = len(methane_injection_conc)
global baseline
baseline = findDaBaseline()

##############################################

fill_methane_time = [0,0]
#fill_methane_time = [0,0,0,0,0,0,0,0,0,0]

methane_correction_factor = 0.72#found it on MKS website
methane_flow_rate = 10#what the value on the MFC is set to
methane_flow_factor = 60/(500*methane_correction_factor*methane_flow_rate)

fill_hydrogen_time =  [0,0]
#fill_hydrogen_time = [0,0,0,0,0,0,0,0,0,0]

hydrogen_correction_factor = 1.01#found it on MKS website
hydrogen_flow_rate = 10#what the value on the MFC is set to
hydrogen_flow_factor = 60/(500*hydrogen_correction_factor*hydrogen_flow_rate)

for i in range(0, len(hydrogen_injection_conc)-1):
    fill_methane_time[i] = int(methane_injection_conc[i]*methane_flow_factor)
    fill_hydrogen_time[i] = int(hydrogen_injection_conc[i]*hydrogen_flow_factor)
#########################################################\

# Testing Variables

#PURGING VARIABLES
chamber_purge_time = 30 #normally 30 #Time to purge chamber: experiment with it

#########FILLING CHAMBER WITH TARGET GAS #############
# Filling Variables
fill_line_clense_time = 20 #normally 20

sampling_time = 0.1 # DO NOT TOUCHtime between samples taken, determines sampling frequency
sensing_delay_time = 1 # normall 1, time delay after beginning data acquisition till when the sensor is exposed to sample
sensing_retract_time = 43 # normally 43, time allowed before sensor is retracted, no longer exposed to sample
duration_of_signal = 300 # normally 300, time allowed for data acquisition per test run

#total_time = chamber_purge_time + fill_line_clense_time + max(fill_methane_time,fill_hydrogen_time) + duration_of_signal

######### TESTING ARRAY #########################


#################### Data Array ####################
# DO NOT TOUCH #
dataVector = []
timeVector = []
#################### Color Settings ####################
warning_color = '#FFC300'
tabBar_color = '#85929E'
tabBarActive_color = '#AEB6BF'
runBtn_color = '#9DE55F'
stopBtn_color = '#FF4E4E'

#################### GUI ####################
projectName = 'MetroVan Project'
class MVGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) #Passes all aguments to the parent class.

        self.title(projectName + ' GUI') #Title of the master window.
        self.geometry('640x480') #Initial size of the master window.
        # self.resizable(0,0) #The allowance for the master window to be adjusted by.

        canvas = tk.Frame(self) #Creates the area for which pages will be displayed.
        canvas.place(relx=0, rely=0, relheight=0.9, relwidth=1) #Defines the area which each page will be displayed.
        canvas.grid_rowconfigure(0, weight=1) #DO NOT ADJUST. Forces each frame to overlap.
        canvas.grid_columnconfigure(0, weight=1) #DO NOT ADJUST. Forces each frame to overlap.

        self.tabBar = tk.Frame(self, bg=tabBar_color) #Creates the area for which control buttons will be placed.
        self.tabBar.place(relx=0, rely=0.9, relheight=0.1, relwidth=1) #Defines the area for which control buttons will be placed.

        self.frames = {} #Dictonary to store each frame after creation.

        for f in (HomePage, DataPage, ManualControlPage): #For pages to be added, do the following:
            frame = f(canvas,self) #Creates a frame of the above classes.
            self.frames[f] = frame #Add the created frame to the 'frames' dictionary.
            frame.grid(row=0, column=0, sticky="nsew") #Overlaps the frame in the same grid space.
        self.show_frame(HomePage) #Sets the default page.

        #Setup controls for fullscreen
        self.attributes("-fullscreen", True)
        self.fullscreen = True
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        valve1.disable()
        valve2.disable()
        valve3.disable()
        valve4.disable()
        valve5.disable()
        #valve6.disable()
        print('System ready.')

    def show_frame(self, cont): #Control buttons will run this command for their corresponding pages.
        frame = self.frames[cont] #Obtain frame object from the dictionary.
        frame.tkraise()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen  # Just toggling the boolean.
        self.attributes("-fullscreen", self.fullscreen) #Pass the fullcreen boolean to tkinter.
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"

    def shutdown(self):
        os.system("sudo shutdown -h now")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Home', bg=tabBar_color, activebackground=tabBarActive_color, bd=0, command=lambda: controller.show_frame(HomePage)) #Creates a control button in the tabs bar.
        control_btn.pack(side='left', expand= True, fill = 'both')

        title = tk.Label(self, text=projectName, font=14, relief='solid')
        title.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.15)

        intro = '''Microfluidic-based Hydrogen Sulfide detector. Developed by ATF Lab
        [F11: Toggle Fullscreen]
        [Esc: Exit Fullscreen]'''

        introduction = tk.Label(self, text=intro, anchor='n')
        introduction.place(relx=0.1,rely=0.55,relheight=0.35,relwidth=0.8)

        #Hash this out if no such functionallity is required. Or if there are bugs.
        self.exitBtn = tk.Button(self, text='Exit Fullscreen', command=lambda:controller.end_fullscreen())
        self.exitBtn.place(relx=0.1,rely=0.8,relheight=0.2,relwidth=0.3)
        self.shutdownBtn = tk.Button(self, text='Shutdown', command=lambda:controller.shutdown())
        self.shutdownBtn.place(relx=0.6,rely=0.8,relheight=0.2,relwidth=0.3)

class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Data', bg=tabBar_color, activebackground=tabBarActive_color, bd=0, command=lambda: controller.show_frame(DataPage))
        control_btn.pack(side='left', expand= True, fill = 'both')

        self.graph = AutoLiveGraph(self, timeVector, dataVector)
        self.graph.place(relx=0,rely=0,relheight=0.9,relwidth=0.8)

        self.status = tk.StringVar()
        self.status.set('  System ready.')

        self.progressTitle = tk.Label(self, textvariable = self.status, anchor='w')
        self.progressTitle.place(relx=0,rely=0.9,relheight=0.07,relwidth=0.8)

        #self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', maximum=100)
        #self.progressbar.place(relx=0,rely=0.97,relheight=0.03,relwidth=0.8)

        self.run_and_stop = tk.Frame(self)
        self.run_and_stop.place(relx=0.8,rely=0.9,relheight=0.1,relwidth=0.2)
        self.run_and_stop.grid_rowconfigure(0, weight=1) #DO NOT ADJUST. Forces buttons to overlap.
        self.run_and_stop.grid_columnconfigure(0, weight=1) #DO NOT ADJUST.

        self.stopBtn = tk.Button(self.run_and_stop, text='STOP', bg=stopBtn_color, activebackground=stopBtn_color, command=lambda:end_testing())
        self.stopBtn.grid(row=0, column=0, sticky="nsew")

        self.contFill = tk.Button(self.run_and_stop, text='CONTINUE', bg=runBtn_color, activebackground=runBtn_color, command=lambda:start_fill_thread())
        self.contFill.grid(row=0, column=0, sticky="nsew")

        self.runBtn = tk.Button(self.run_and_stop, text='RUN', bg=runBtn_color, activebackground=runBtn_color, command=lambda:multi_test_run())
        self.runBtn.grid(row=0, column=0, sticky="nsew")


        statusFrame = tk.LabelFrame(self, text ='Status')
        statusFrame.place(relx=0.8,rely=0.3,relheight=0.6,relwidth=0.2)
##        testLBL = tk.Label(statusFrame,text = 'Test: ')
#        meConcLBL = tk.Label(statusFrame,text = 'Methane Concentration: ')
#        H2ConcLBL = tk.Label(statusFrame,text = 'Hydrogen Concentration: ')
#        meFillTime = tk.Label(statusFrame,text = 'Methane Fill Time: ')
#        H2FillTime = tk.Label(statusFrame,text = 'Hydrogen Fill Time: ')
##        testLBL.place(relx = 0.1, rely = 0, relheight = 0.1, relwidth = 0.1)
#        meConcLBL.place(relx = 0.1, rely = 0.1, relheight = 0.1, relwidth = 0.5)
#        H2ConcLBL.place(relx = 0.1, rely = 0.2, relheight = 0.1, relwidth = 0.5)
#        meFillTime.place(relx = 0.1, rely = 0.3, relheight = 0.1, relwidth = 0.4)
#        H2FillTime.place(relx = 0.1, rely = 0.4, relheight = 0.1, relwidth = 0.4)

        responseFrame = tk.Frame(self)
        responseFrame.place(relx=0.8,rely=0,relheight=0.3,relwidth=0.2)
        self.naturalGasLabel = tk.Label(responseFrame, text = 'Hydrogen Sulfide\n', relief='groove', borderwidth=2, anchor='center')
        self.naturalGasLabel.place(relx=0,rely=0,relheight=0.7,relwidth=1)
        self.orig_color = self.naturalGasLabel.cget("background") # Store the original color of the label.

        ppmDisplay = tk.Frame(responseFrame, relief='groove', borderwidth=2)
        ppmDisplay.place(relx=0,rely=0.7,relheight=0.3,relwidth=1)
       # ppmLabel = tk.Label(ppmDisplay, text = 'PPM:')
       # ppmLabel.place(relx=0,rely=0,relheight=1,relwidth=0.3)
        self.ppmVar = tk.IntVar()
        self.ppmVar.set(0)
        ppmDisplay = tk.Label(ppmDisplay, textvariable = self.ppmVar, anchor='w')
        ppmDisplay.place(relx=0.3,rely=0,relheight=1,relwidth=0.7)

class ManualControlPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Manual Controls', bg=tabBar_color, activebackground=tabBarActive_color, bd=0, command=lambda: controller.show_frame(ManualControlPage))
        control_btn.pack(side='left', expand= True, fill = 'both')

        #Create a termial within a parent frame.
        terminal = tk.Frame(self)
        CoreGUI(terminal)
        terminal.place(relx=0.7,rely=0,relheight=1,relwidth=0.3)

        controlFrame = tk.LabelFrame(self, text='System')
        controlFrame.place(relx=0,rely=0,relheight=1,relwidth=0.7)
        leftControlFrame = tk.Frame(controlFrame)
        leftControlFrame.place(relx=0,rely=0,relheight=1,relwidth=0.5)
        rightControlFrame = tk.Frame(controlFrame)
        rightControlFrame.place(relx=0.5,rely=0,relheight=1,relwidth=0.5)

        buttonWidth = 0.4 #Relative width of buttons within the frame
        self.btn_1 = tk.Button(controlFrame, text='Extend Linear Actuator', command=lambda:linearActuator.extend())
        self.btn_1.place(relx=0,rely=0,relheight=0.1,relwidth=buttonWidth)
        self.btn_2 = tk.Button(controlFrame, text='Retract Linear Actuator', command=lambda:linearActuator.retract())
        self.btn_2.place(relx=0,rely=0.1,relheight=0.1,relwidth=buttonWidth)
        self.btn_3 = tk.Button(controlFrame, text='Read MOS', command=lambda:mos.print())
        self.btn_3.place(relx=0,rely=0.2,relheight=0.1,relwidth=buttonWidth)
#        self.btn_4 = tk.Button(controlFrame, text='Read Pressure', command=lambda:pressSensor.print())
#        self.btn_4.place(relx=0,rely=0.3,relheight=0.1,relwidth=buttonWidth)
        self.btn_4 = tk.Button(controlFrame, text='Enable Pump', command=lambda:pump.enable())
        self.btn_4.place(relx=0,rely=0.3,relheight=0.1,relwidth=buttonWidth)
        self.btn_17 = tk.Button(controlFrame, text = "Disable Pump", command=lambda:pump.disable())
        self.btn_17.place(relx=0, rely=0.4,relheight=0.1,relwidth = buttonWidth)
        self.btn_18 = tk.Button(controlFrame, text = "Extend Stepper Motor", command=lambda:Stepper_Motor.extend())
        self.btn_18.place(relx=0, rely=0.5, relheight = 0.1, relwidth = buttonWidth) 
        self.btn_19 = tk.Button(controlFrame, text = "Retract Stepper Motor", command = lambda:Stepper_Motor.retract())
        self.btn_19.place(relx=buttonWidth, rely = 0.5, relheight = 0.1, relwidth = buttonWidth)
        self.btn_20= tk.Button(controlFrame, text = "Turn on Heater", command=lambda:Metro_Heater.heat())
        self.btn_20.place(relx=0, rely = 0.6, relheight = 0.1, relwidth = buttonWidth) 
        self.btn_21 = tk.Button(controlFrame, text = "Turn off Heater", command=lambda:Metro_Heater.cool())
        self.btn_21.place(relx=buttonWidth, rely = 0.6, relheight = 0.1, relwidth = buttonWidth)
        self.btn_22 = tk.Button(controlFrame, text = "Purge System", command=lambda:purge_system_raw())
        self.btn_22.place(relx=0, rely=0.7, relheight = 0.1, relwidth = buttonWidth) 
        self.btn_23 = tk.Button(controlFrame, text = "Fill Chambers", command=lambda:fill_chamber())
        self.btn_23.place(relx=0, rely=0.8, relheight = 0.1, relwidth = buttonWidth) 
        self.btn_24 = tk.Button(controlFrame, text = "Cleanse Lines", command=lambda:cleanse_chamber())
        self.btn_24.place(relx=0,rely=0.9, relheight = 0.1, relwidth = buttonWidth)

        self.btn_5 = tk.Button(controlFrame, text='Valve 1 Enable', command=lambda:valve1.enable())
        self.btn_5.place(relx=buttonWidth,rely=0,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_6 = tk.Button(controlFrame, text='Valve 2 Enable', command=lambda:valve2.enable())
        self.btn_6.place(relx=buttonWidth,rely=0.1,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_7 = tk.Button(controlFrame, text='Valve 3 Enable', command=lambda:valve3.enable())
        self.btn_7.place(relx=buttonWidth,rely=0.2,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_8 = tk.Button(controlFrame, text='Valve 4 Enable', command=lambda:valve4.enable())
        self.btn_8.place(relx=buttonWidth,rely=0.3,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_9 = tk.Button(controlFrame, text='Valve 5 Enable', command=lambda:valve5.enable())
        self.btn_9.place(relx=buttonWidth,rely=0.4,relheight=0.1,relwidth=buttonWidth/2)
       

        self.btn_11 = tk.Button(controlFrame, text='Valve 1 Disable', command=lambda:valve1.disable())
        self.btn_11.place(relx=buttonWidth*3/2,rely=0,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_12 = tk.Button(controlFrame, text='Valve 2 Disable', command=lambda:valve2.disable())
        self.btn_12.place(relx=buttonWidth*3/2,rely=0.1,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_13 = tk.Button(controlFrame, text='Valve 3 Disable', command=lambda:valve3.disable())
        self.btn_13.place(relx=buttonWidth*3/2,rely=0.2,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_14 = tk.Button(controlFrame, text='Valve 4 Disable', command=lambda:valve4.disable())
        self.btn_14.place(relx=buttonWidth*3/2,rely=0.3,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_15 = tk.Button(controlFrame, text='Valve 5 Disable', command=lambda:valve5.disable())
        self.btn_15.place(relx=buttonWidth*3/2,rely=0.4,relheight=0.1,relwidth=buttonWidth/2)
        self.btn_16 = tk.Button(controlFrame, text='Read All Sensors', command=lambda:read_All_Sensors())
        self.btn_16.place(relx=buttonWidth,rely=0.7,relheight=0.1,relwidth=buttonWidth)
def suppress_buttons():
    app.frames[ManualControlPage].btn_1.config(state='disabled')
    app.frames[ManualControlPage].btn_2.config(state='disabled')
    app.frames[ManualControlPage].btn_3.config(state='disabled')
    app.frames[ManualControlPage].btn_4.config(state='disabled')
    app.frames[ManualControlPage].btn_5.config(state='disabled')
    app.frames[ManualControlPage].btn_6.config(state='disabled')
    app.frames[ManualControlPage].btn_7.config(state='disabled')
    app.frames[ManualControlPage].btn_8.config(state='disabled')
    app.frames[ManualControlPage].btn_9.config(state='disabled')
##    app.frames[ManualControlPage].btn_10.config(state='disabled')
    app.frames[ManualControlPage].btn_11.config(state='disabled')
    app.frames[ManualControlPage].btn_12.config(state='disabled')
    app.frames[ManualControlPage].btn_13.config(state='disabled')
    app.frames[ManualControlPage].btn_14.config(state='disabled')
    app.frames[ManualControlPage].btn_15.config(state='disabled')
    app.frames[ManualControlPage].btn_16.config(state='disabled')
    app.frames[ManualControlPage].btn_17.config(state='disabled')
    app.frames[ManualControlPage].btn_18.config(state='disabled')
    app.frames[ManualControlPage].btn_19.config(state='disabled')  
    app.frames[ManualControlPage].btn_20.config(state='disabled')
    app.frames[ManualControlPage].btn_21.config(state='disabled')
    app.frames[ManualControlPage].btn_22.config(state='disabled')
    app.frames[ManualControlPage].btn_23.config(state='disabled')
    app.frames[ManualControlPage].btn_24.config(state='disabled')
    app.frames[HomePage].exitBtn.config(state='disabled')
    app.frames[HomePage].shutdownBtn.config(state='disabled')

def release_buttons():
    app.frames[ManualControlPage].btn_1.config(state='normal')
    app.frames[ManualControlPage].btn_2.config(state='normal')
    app.frames[ManualControlPage].btn_3.config(state='normal')
    app.frames[ManualControlPage].btn_4.config(state='normal')
    app.frames[ManualControlPage].btn_5.config(state='normal')
    app.frames[ManualControlPage].btn_6.config(state='normal')
    app.frames[ManualControlPage].btn_7.config(state='normal')
    app.frames[ManualControlPage].btn_8.config(state='normal')
    app.frames[ManualControlPage].btn_9.config(state='normal')
##    app.frames[ManualControlPage].btn_10.config(state='normal')
    app.frames[ManualControlPage].btn_11.config(state='normal')
    app.frames[ManualControlPage].btn_12.config(state='normal')
    app.frames[ManualControlPage].btn_13.config(state='normal')
    app.frames[ManualControlPage].btn_14.config(state='normal')
    app.frames[ManualControlPage].btn_15.config(state='normal')
    app.frames[ManualControlPage].btn_16.config(state='normal')
    app.frames[ManualControlPage].btn_17.config(state='normal')
    app.frames[ManualControlPage].btn_18.config(state='normal')
    app.frames[ManualControlPage].btn_19.config(state='normal')
    app.frames[ManualControlPage].btn_20.config(state='normal')
    app.frames[ManualControlPage].btn_21.config(state='normal')
    app.frames[ManualControlPage].btn_22.config(state='normal')
    app.frames[ManualControlPage].btn_23.config(state='normal')
    app.frames[ManualControlPage].btn_24.config(state='normal')
    app.frames[HomePage].exitBtn.config(state='normal')
    app.frames[HomePage].shutdownBtn.config(state='normal')

def read_All_Sensors():
    mos.print()
##    read_BME(bme280)
##    read_BME(bme280_2)
    read_MAX31855(max31855)
    
def purge_system():

    start_time = time.time()
    print("Purging System")
    if valve5.state != True: 
        valve5.enable()
    linearActuator.purge()
    pump.enable() 
    while time.time() < (start_time + chamber_purge_time) and continueTest == True:
        # wait patiently for the purging to be finished
        pass 
    pump.disable()
    if valve5.state != False: 
        valve5.disable() 
    print("Done purging")

def purge_system_raw():
    start_time = time.time()
    print("Purging System")
    if valve5.state != True: 
        valve5.enable()
    linearActuator.purge()
    pump.enable() 
    while time.time() < (start_time + chamber_purge_time):
        # wait patiently for the purging to be finished
        pass 
    pump.disable()
    if valve5.state != False: 
        valve5.disable() 
    print("Done purging")
    
def fill_chamber():
    if linearActuator.state != 'retracted':
        linearActuator.retract()
    #########FILL H2S ############
   
    # Filling the chamber
    
    stepperMotorRT= 10  # Time it takes for the stepper motor to fully complete the retraction process
    stepperMotorET = 10 # Time it takes for the stepper motor to fully complete the extension process 
    print("Filling Chamber")
    if valve1.state != True:
        valve1.enable()
    if valve2.state != True:
        valve2.enable()
    if valve3.state != True:
        valve3.enable()
    if valve4.state != False:
        valve4.disable()
    if valve5.state != True:
        valve5.enable()
    
    for x in range (4):
        start_time = time.time()
        Stepper_Motor.retract()
        while (time.time() - start_time < stepperMotorRT) and continueTest == True:
            # wait patiently for the Stepper Motor to finish retracting 
            pass
    if valve3.state != False: 
        valve3.disable()
    for x in range (4):
        start_time = time.time()
        Stepper_Motor.extend()
        while (time.time() - start_time < stepperMotorRT) and continueTest == True:
            # wait patiently fo  r the Stepper Motor to finish retracting 
            pass
    
   
   
    ########END FILL########

def cleanse_chamber(): 
    start_time = time.time()
    Metro_Heater.heat()
    stepperMotorRT= 10  # Time it takes for the stepper motor to fully complete the retraction process
    stepperMotorET = 10 # Time it takes for the stepper motor to fully complete the extension process 
    print("Cleansing lines") 
    CCT = 3 # The number of times you repeat the stepper motor cycle 
    if valve1.state != False: 
        valve1.disable()
    if valve2.state != False: 
        valve2.disable() 
    if valve3.state != False: 
        valve3.disable() 
    if valve4.state != True: 
        valve4.enable() 
    if valve5.state != False: 
        valve5.disable() 
    Metro_Heater.heat()
    cleanse_time = 15
    start_time = time.time()
    pump.enable()
    while (time.time() - start_time < cleanse_time):
        pass
    if valve4.state != False:
        valve4.disable()
    start_time = time.time()
    while(time.time() - start_time < cleanse_time):
        pass
    if valve4.state != True:
        valve4.enable()
    pump.disable()
    if valve3.state!= True:
        valve3.enable()
    if valve2.state!= True:
        valve2.enable()
      
    Stepper_Motor.retract()
    start_time = time.time()
    while (time.time() - start_time < stepperMotorRT):
        # wait patiently for the Stepper Motor to finish retracting
        pass
    
    if valve3.state !=False:
        valve3.disable()
    Stepper_Motor.extend()
    start_time = time.time()
    while (time.time() - start_time < stepperMotorET):
            # wait patiently for the Stepper Motor to finish extending
        pass
    if valve2.state != False:
        valve2.disable()
    pump.enable()
    start_time = time.time()
    while(time.time() - start_time < cleanse_time):
        pass
    pump.disable()
    start_time = time.time()
    heat_time = 20
    while time.time() - start_time < heat_time:
        pass
    Metro_Heater.cool()
    if valve1.state != True:
        valve1.enable()



def collect_data(xVector,yVector):
    heat_start_time = time.time()  # Local value. Capture the time at which the test began. All time values can use start_time as a reference
    dataVector = yVector
    timeVector = xVector
    dataVector.clear()
    timeVector.clear()
    sampling_time_index = 1
    Metro_Heater.heat()
    global baseline
    # Initial Heating Portion
    while (time.time() - heat_start_time < 300): #Vaporization time
        pass
   
    
    start_time = time.time() 
    print('Starting data capture.')
    while (time.time() < (start_time + duration_of_signal)) and (continueTest == True):  # While time is less than duration of logged file
        if (time.time() > (start_time + (sampling_time * sampling_time_index)) and (continueTest == True)):  # if time since last sample is more than the sampling time, take another sample
            dataVector.append(mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
            timeVector.append(time.time() - start_time)
            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        elif (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (continueTest == True)):
            if linearActuator.state != 'extended':
                linearActuator.extend()

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        elif (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (continueTest == True):
            if linearActuator.state != 'retracted':
                linearActuator.retract()

        # Otherwise, keep outputs off
        else:
            if linearActuator.state != 'retracted':
                linearActuator.retract()
                
##    dataVector[:] = [x * (-1) for x in dataVector]
##    dataVector[:] = [x + (2*baseline) for x in dataVector]
    combinedVector = np.column_stack((timeVector, dataVector))
##    current_time = datetime.datetime.now()
##    year = current_time.year
##    month = current_time.month
##    day = current_time.day
##    createFolders(year, month, day)
##    hour = current_time.hour
##    minute = current_time.minute
##    fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + 'H2S_Test.csv'
##    #fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_bl.csv'
##    np.savetxt(r'/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(fileName), combinedVector, fmt='%.10f', delimiter=',')
##    pass
##    print("Data has been saved!") 
##    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = strftime("/home/pi/Documents/gui/MetroVan_GUI/tests_H2S/%a%d%b%Y%H%M%S.csv",localtime())
    np.savetxt(filename,combinedVector, fmt='%.10f', delimiter=',')
    print("Test ",test_counter + 1," File Saved")


    pass
    Metro_Heater.cool()
def multi_test_run():
    global num_tests
    #num_tests = len(methane_injection_conc)
    global test_counter
    if test_counter < num_tests:
        start_fill_thread()
        pass
    else:
        global continueTest
        continueTest = False #Set the test flag to false, stops testing.
        release_buttons()
        app.frames[DataPage].runBtn.tkraise()
        app.frames[DataPage].status.set('  System ready.')
        print(num_tests," Tests Completed")
        end_testing()
# def pressue_check_thread():
#     if pressSensor.read() > press_threshold:


def start_purge_thread():
    suppress_buttons()
    app.frames[DataPage].stopBtn.tkraise()
    global purge_thread
    global continueTest
    continueTest = True
    purge_thread = threading.Thread(target=purge_system)
    purge_thread.daemon = True
    app.frames[DataPage].status.set('  Purging chambers...')
    #app.frames[DataPage].progressbar.start((chamber_purge_time)*10)
    purge_thread.start()
    app.after(20, check_purge_thread)

def check_purge_thread():
    if purge_thread.is_alive():
        app.after(20, check_purge_thread)
    else:
        #app.frames[DataPage].progressbar.stop()
        app.frames[DataPage].graph.update(timeVector,dataVector)
        # release_buttons()
        # app.frames[DataPage].runBtn.tkraise()
        # app.frames[DataPage].status.set('  System ready.')
        end_testing()

def start_fill_thread():
    suppress_buttons()
    app.frames[DataPage].stopBtn.tkraise()
    app.frames[DataPage].naturalGasLabel.config(bg=app.frames[DataPage].orig_color)
    global fill_thread
    global continueTest
    continueTest = True
    fill_thread = threading.Thread(target=fill_chamber)
    fill_thread.daemon = True
    app.frames[DataPage].status.set('  Filling sample chamber...')
    #app.frames[DataPage].progressbar.start(max(fill_methane_time,fill_hydrogen_time)*10)
    fill_thread.start()
    app.after(20, check_fill_thread)

def check_fill_thread():
    if fill_thread.is_alive():
        app.after(20, check_fill_thread)
    else:
        #app.frames[DataPage].progressbar.stop()
        if continueTest == True:
            start_data_thread()

def start_cleanse_thread(): 
    suppress_buttons()
    global cleanse_thread
    global continueTest 
    continueTest = True
    cleanse_thread = threading.Thread(target = cleanse_chamber)
    cleanse_thread.daemon = True
    app.frames[DataPage].status.set('   Cleansing lines    ')
    cleanse_thread.start()
    app.after(20, check_cleanse_thread)

def check_cleanse_thread(): 
    if cleanse_thread.is_alive(): 
        app.after(20, check_cleanse_thread)
    else: 
        if continueTest == True: 
            start_purge_thread()
            
def start_data_thread():
    suppress_buttons()
    global data_thread
    global continueTest
    continueTest = True
    data_thread = threading.Thread(target=collect_data,args=(timeVector,dataVector))
    data_thread.daemon = True
    app.frames[DataPage].status.set('  Capturing data...')
    #app.frames[DataPage].progressbar.start(duration_of_signal*10)
    data_thread.start()
    app.after(20, check_data_thread)

def check_data_thread():
    if data_thread.is_alive():
        app.after(20, check_data_thread)
    else:
        if continueTest == True: 
            start_cleanse_thread()
        #app.frames[DataPage].progressbar.stop()
        
        
def end_testing():
    #if purge_thread.is_alive() or fill_thread.is_alive() or data_thread.is_alive():
    global continueTest
    continueTest = False #Set the test flag to false, stops testing.
    release_buttons()
    app.frames[DataPage].runBtn.tkraise()
    app.frames[DataPage].status.set('  System ready.')

    
    
app = MVGUI()
app.mainloop()

linearActuator.endLinAc()
GPIO.cleanup()
##try:
##    app = MVGUI()
##    app.mainloop()
##except keyboardinterrupt:
##    GPIO.cleanup()
##finally:
##    GPIO.cleanup()

