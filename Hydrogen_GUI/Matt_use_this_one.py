# This version of the code is designed to be used with the P-Type linear actuator.
# This code was made by editing the file H2_fix.py, which was designed to be used with
# the R-Type linear actuator.
#!/usr/bin/python3
#Last edit: 02/08/2019
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
from H2_components_v2_p import *
# -----> RPi Imports <------
import RPi.GPIO as GPIO
import time
import os
import Adafruit_ADS1x15 as ads
import serial
from pathlib import Path

#---->
import numpy as np
# import sklearn
# import pickle

global positionSensor

class PositionSensor():
    def __init__(self, adc, channel):
        # Choose a gain of 1 for reading voltages from 0 to 4.09V.
        # Or pick a different gain to change the range of voltages that are read:
        #  - 2/3 = +/-6.144V
        #  -   1 = +/-4.096V
        #  -   2 = +/-2.048V
        #  -   4 = +/-1.024V
        #  -   8 = +/-0.512V
        #  -  16 = +/-0.256V
        # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
        self.GAIN = 2 / 3
        self.adc = adc
        self.channel = channel
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144

    def read(self):
        self.conversion_value = (self.adc.read_adc(self.channel,gain=self.GAIN)/pow(2, 15))*6.144
        return self.conversion_value

    def print(self):
        self.read()
        print("\nReading from Linear Actuator Position Sensor: {}".format(self.conversion_value))


class LinearActuator:
    def __init__(self, LinActRetract,LinActExtend):
        self.LinActRetract = LinActRetract
        self.LinActExtend = LinActExtend
        self.extended_state = 3.9
        self.retracted_state = 1.2
        GPIO.setup(self.LinActRetract, GPIO.OUT)
        GPIO.setup(self.LinActExtend, GPIO.OUT)
        GPIO.output(self.LinActRetract, GPIO.LOW)
        GPIO.output(self.LinActExtend, GPIO.LOW)
        self.state = 'default'


    def extend(self):
        print('Extending linear actuator.')
        global positionSensor
        while (positionSensor.read() < self.extended_state):
            GPIO.output(LinActRetract, GPIO.LOW)
            GPIO.output(LinActExtend, GPIO.HIGH)
            print("i am looooopy")
        self.state = 'extended'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)
       

    def retract(self):
        global positionSensor
        print('Retracting linear actuator.')
        while (positionSensor.read() > self.retracted_state):
            GPIO.output(LinActRetract, GPIO.HIGH)
            GPIO.output(LinActExtend, GPIO.LOW)
        self.state = 'retracted'
        GPIO.output(LinActRetract, GPIO.LOW)
        GPIO.output(LinActExtend, GPIO.LOW)
       


# Analog-Digital Converter
adc = ads.ADS1115(0x48)

#################### Object Declaration ####################
GPIO.setmode(GPIO.BOARD)
# Linear Actuator
#pinLA = 37
#pinEnable = 15
#linearActuator = LinearActuator(pinLA,pinEnable)
LinActRetract = 15
LinActExtend = 13
linearActuator = LinearActuator(LinActRetract,LinActExtend)
# MOS Sensor
MOS_adc_channel = 0
mos = MOS(adc, MOS_adc_channel)
# Pressure sensor
press_adc_channel = 1
pressSensor = PressureSensor(adc,press_adc_channel)
# Position sensor
Lin_act_position_channel = 2
positionSensor = PositionSensor(adc, Lin_act_position_channel)

# Valves

# pinvalve1 = 12
# pinvalve2 = 16
# pinvalve3 = 18
# pinvalve4 = 22
# pinvalve5 = 36
# pinvalve6 = 40

pinvalve1 = 12
pinvalve2 = 22
pinvalve3 = 16
pinvalve4 = 18
pinvalve5 = 36
pinvalve6 = 40
valve1 = Valve('Valve1',pinvalve1) #Methane Tank to MFC
valve2 = Valve('Valve2',pinvalve2) #H2 Tank to MFC
valve3 = Valve('Valve3',pinvalve3) #Line Venting
valve4 = Valve('Valve4',pinvalve4) #Line Venting
valve5 = Valve('Valve5',pinvalve5) #Air into Chamber
valve6 = Valve('Valve6',pinvalve6) #Chamber Exhaust

################## EXPERIMENTAL STEPS ################


#STEP 1: PURGE BOX::: V1:N V2:N V3:N V4:N V5:Y V6:Y
#STEP 2: FILL METHANE P1::: V1:Y V2:N V3:Y V4:N V5:N V6:N
#STEP 3: FILL METHANE P2::: V1:Y V2:N V3:N V4:Y V5:N V6:Y
#STEP 4: FILL H2 P1::: V1:N V2:Y V3:Y V4:N V5:N V6:N
#STEP 5: FILL H2 P2::: V1:N V2:Y V3:N V4:Y V5:N V6:Y
#STEP 6: TEST::: V1:N V2:N V3:N V4:N V5:N V6:N

#################### System Variables ####################



##############################################################
######## SAMPLE INJECTION CONCENTRATIONS #####################
#hydrogen_injection_conc = [500, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990,1000] #Whatever vales you need
#methane_injection_conc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hydrogen_injection_conc = [1000,200]
methane_injection_conc = [0,0]
##############################################################
##############################################################

global test_counter
test_counter = 0
global num_tests
num_tests = len(methane_injection_conc)

##############################################

fill_methane_time = [0,0]
#fill_methane_time= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
methane_correction_factor = 0.72#found it on MKS website

methane_flow_factor = (60*2000*methane_correction_factor)/(10000000)

fill_hydrogen_time =  [0,0]
#fill_hydrogen_time= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hydrogen_correction_factor = 1.01#found it on MKS website

hydrogen_flow_factor = (60*2000*hydrogen_correction_factor)/(10000000)

for i in range(0, len(hydrogen_injection_conc)):
    fill_methane_time[i] = float(methane_injection_conc[i]*methane_flow_factor)
    fill_hydrogen_time[i] = float(hydrogen_injection_conc[i]*hydrogen_flow_factor)
    
print(fill_methane_time)
#########################################################\

# Testing Variables

#PURGING VARIABLES
#chamber_purge_time = 100 #normally 30 #Time to purge chamber: experiment with it
#
##########FILLING CHAMBER WITH TARGET GAS #############
## Filling Variables
#fill_line_clense_time = 20 #normally 20
#
#sampling_time = 0.1 # DO NOT TOUCHtime between samples taken, determines sampling frequency
#sensing_delay_time = 1 # normall 10, time delay after beginning data acquisition till when the sensor is exposed to sample
#sensing_retract_time = 51 # normally 40, time allowed before sensor is retracted, no longer exposed to sample
#duration_of_signal = 240 # normally 200, time allowed for data acquisition per test run



chamber_purge_time = 100#normally 30 #Time to purge chamber: experiment with it

#########FILLING CHAMBER WITH TARGET GAS #############
# Filling Variables
fill_line_clense_time = 10#normally 20

sampling_time = 0.1 # DO NOT TOUCHtime between samples taken, determines sampling frequency
sensing_delay_time = 10 # normall 10, time delay after beginning data acquisition till when the sensor is exposed to sample
sensing_retract_time = 50 # normally 40, time allowed before sensor is retracted, no longer exposed to sample
duration_of_signal = 250 #

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
projectName = 'Hydrogen Detection'
class HetekGUI(tk.Tk):
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

#        valve1.enable()
#        time.sleep(0.2)
#        valve2.enable()
#        time.sleep(0.2)
#        valve3.enable()
#        time.sleep(0.2)
#        valve4.enable()
#        time.sleep(0.2)
#        valve5.enable()
#        time.sleep(0.2)
#        valve6.enable()
#        time.sleep(0.2)

        valve1.disable()
        valve2.disable()
        valve3.disable()
        valve4.disable()
        valve5.disable()
        valve6.disable()
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

        intro = '''Microfluidic-based natural gas detector. Developed by ATF Lab
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
        testLBL = tk.Label(statusFrame,text = 'Test: ')
        meConcLBL = tk.Label(statusFrame,text = 'Methane Concentration: ')
        H2ConcLBL = tk.Label(statusFrame,text = 'Hydrogen Concentration: ')
        meFillTime = tk.Label(statusFrame,text = 'Methane Fill Time: ')
        H2FillTime = tk.Label(statusFrame,text = 'Hydrogen Fill Time: ')
        testLBL.place(relx = 0.1, rely = 0, relheight = 0.1, relwidth = 0.1)
        meConcLBL.place(relx = 0.1, rely = 0.1, relheight = 0.1, relwidth = 0.5)
        H2ConcLBL.place(relx = 0.1, rely = 0.2, relheight = 0.1, relwidth = 0.5)
        meFillTime.place(relx = 0.1, rely = 0.3, relheight = 0.1, relwidth = 0.4)
        H2FillTime.place(relx = 0.1, rely = 0.4, relheight = 0.1, relwidth = 0.4)

        responseFrame = tk.Frame(self)
        responseFrame.place(relx=0.8,rely=0,relheight=0.3,relwidth=0.2)
        self.naturalGasLabel = tk.Label(responseFrame, text = '', relief='groove', borderwidth=2, anchor='center')
        self.naturalGasLabel.place(relx=0,rely=0,relheight=0.7,relwidth=1)
        self.orig_color = self.naturalGasLabel.cget("background") # Store the original color of the label.

        ppmDisplay = tk.Frame(responseFrame, relief='groove', borderwidth=2)
        ppmDisplay.place(relx=0,rely=0.7,relheight=0.3,relwidth=1)
        ppmLabel = tk.Label(ppmDisplay, text = 'PPM:')
        ppmLabel.place(relx=0,rely=0,relheight=1,relwidth=0.3)
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
        self.btn_4 = tk.Button(controlFrame, text='Read Pressure', command=lambda:pressSensor.print())
        self.btn_4.place(relx=0,rely=0.3,relheight=0.1,relwidth=buttonWidth)

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
        self.btn_10 = tk.Button(controlFrame, text='Valve 6 Enable', command=lambda:valve6.enable())
        self.btn_10.place(relx=buttonWidth,rely=0.5,relheight=0.1,relwidth=buttonWidth/2)

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
        self.btn_16 = tk.Button(controlFrame, text='Valve 6 Disable', command=lambda:valve6.disable())
        self.btn_16.place(relx=buttonWidth*3/2,rely=0.5,relheight=0.1,relwidth=buttonWidth/2)
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
    app.frames[ManualControlPage].btn_10.config(state='disabled')
    app.frames[ManualControlPage].btn_11.config(state='disabled')
    app.frames[ManualControlPage].btn_12.config(state='disabled')
    app.frames[ManualControlPage].btn_13.config(state='disabled')
    app.frames[ManualControlPage].btn_14.config(state='disabled')
    app.frames[ManualControlPage].btn_15.config(state='disabled')
    app.frames[ManualControlPage].btn_16.config(state='disabled')
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
    app.frames[ManualControlPage].btn_10.config(state='normal')
    app.frames[ManualControlPage].btn_11.config(state='normal')
    app.frames[ManualControlPage].btn_12.config(state='normal')
    app.frames[ManualControlPage].btn_13.config(state='normal')
    app.frames[ManualControlPage].btn_14.config(state='normal')
    app.frames[ManualControlPage].btn_15.config(state='normal')
    app.frames[ManualControlPage].btn_16.config(state='normal')
    app.frames[HomePage].exitBtn.config(state='normal')
    app.frames[HomePage].shutdownBtn.config(state='normal')

def purge_system():

    start_time = time.time()
    print("Purging System \n V1:N V2:N V3:N V4:N V5:Y V6:Y")
    while time.time() < (start_time + chamber_purge_time) and continueTest == True:
        if linearActuator.state != 'retracted':
            linearActuator.retract()
        if valve1.state != False:
            valve1.disable()
        if valve2.state != False:
            valve2.disable()
        if valve3.state != False:
            valve3.disable()
        if valve4.state != False:
            valve4.disable()
        if valve6.state != True:
            valve6.enable()
        if valve5.state != True:
            valve5.enable()

    print("Done purging \n V1:N V2:N V3:N V4:N V5:N V6:N")
    if linearActuator.state != 'retracted':
        linearActuator.retract()
    if valve1.state != False:
        valve1.disable()
    if valve2.state != False:
        valve2.disable()
    if valve3.state != False:
        valve3.disable()
    if valve4.state != False:
        valve4.disable()
    if valve5.state != False:
        valve5.disable()
    if valve6.state != False:
        valve6.disable()
    pass

def fill_chamber():
#    if linearActuator.state != 'retracted':
#        linearActuator.retract()
#    #########FILL METHANE and Hydrogen############

    start_time = time.time() #Methane and Hydrogen Fill Line Clensing
    print("Cleansing Line \n V1:N V2:N V3:Y V4:Y V5:N V6:N")
    while time.time() < (start_time + fill_line_clense_time) and continueTest == True:
        if valve1.state != False:
            valve1.disable()
        if valve2.state != False:
            valve2.disable()
        if valve3.state != True:
            valve3.enable()
        if valve4.state != True:
            valve4.enable()
        if valve5.state != False:
            valve5.disable()
        if valve6.state != False:
            valve6.disable()
        pass
#    
    # Filling the chamber
    start_time = time.time()
    print("Filling Chamber Hydrogen\n V1:Y V2:N V3:N V4:Y V5:N V6:N")
    while time.time() < ( start_time + fill_hydrogen_time[test_counter]) and continueTest == True:
        if valve1.state != False:
            valve1.disable()
        if valve2.state != True:
            valve2.enable()
        if valve3.state != False:
            valve3.disable()
        if valve4.state != False:
            valve4.disable()
        if valve5.state != False:
            valve5.disable()
        if valve6.state != False:
            valve6.disable()
        pass
    
    start_time = time.time()
    print("Hydrogen Closed, Methane Only\n V1:Y V2:N V3:N V4:Y V5:N V6:N")
    while time.time() > (start_time + fill_hydrogen_time[test_counter]) and time.time() < ( start_time + fill_methane_time[test_counter]) and continueTest == True:
        if valve1.state != True:
            valve1.enable()
        if valve2.state != False:
            valve2.disable()
        if valve3.state != False:
            valve3.disable()
        if valve4.state != False:
            valve4.disable()
        if valve5.state != False:
            valve5.disable()
        if valve6.state != False:
            valve6.disable()
        pass

    print("Done Filling Methane, both gases closed \n V1:N V2:N V3:N V4:N V5:N V6:N")


    ########END GAS FILL########



def collect_data(xVector,yVector):
    start_time = time.time()  # Local value. Capture the time at which the test began. All time values can use start_time as a reference
    dataVector = yVector
    timeVector = xVector
    dataVector.clear()

    timeVector.clear()
    sampling_time_index = 1

    # Initial state checks
    if linearActuator.state != 'retracted':
        linearActuator.retract()
    if valve1.state != False:
        valve1.disable()
    if valve2.state != False:
        valve2.disable()
    if valve3.state != False:
        valve3.disable()
    if valve4.state != False:
        valve4.disable()
    if valve5.state != False:
        valve5.disable()
    if valve6.state != False:
        valve6.disable()

    start_time = time.time()
    print('Starting data capture.')
    while (time.time() < (start_time + duration_of_signal)) and (continueTest == True):  # While time is less than duration of logged file
        if (time.time() > (start_time + (sampling_time * sampling_time_index)) and (continueTest == True)):  # if time since last sample is more than the sampling time, take another sample
            dataVector.append(mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
#            dataVector2.append(methane_injection_conc[testcounter])
#            dataVector3.append(hydrogen_injection_conc[testcounter])
            timeVector.append(time.time() - start_time)
            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        elif (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (continueTest == True)):
            if linearActuator.state != 'extended':
                linearActuator.extend()
                print("The linear actuator should be extended")

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        elif (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (continueTest == True):
            if linearActuator.state != 'retracted':
                linearActuator.retract()
                print("The linear actuator should be retracted")

        # Otherwise, keep outputs off
        else:
            if linearActuator.state != 'retracted':
                linearActuator.retract()
    time_len = len(timeVector)
    methConc_array = np.ndarray(shape=(time_len,1))
    methConc_array.fill(methane_injection_conc[test_counter])
    H2Conc_array = np.ndarray(shape=(time_len,1))
    H2Conc_array.fill(hydrogen_injection_conc[test_counter])
    combinedVector = np.column_stack((timeVector, dataVector,methConc_array,H2Conc_array))

    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = strftime("testsH2/%a%d%b%Y%H%M%S.csv",localtime())
    np.savetxt(filename,combinedVector, fmt='%.10f', delimiter=',')
    print("Test ",test_counter + 1," File Saved")


    pass

def multi_test_run():
    global num_tests
    #num_tests = len(methane_injection_conc)
    global test_counter
    if test_counter < num_tests:
        start_purge_thread()
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
    app.frames[DataPage].naturalGasLabel.config(bg=app.frames[DataPage].orig_color)
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
        if continueTest ==True:
            start_fill_thread()

def start_fill_thread():
    suppress_buttons()
    app.frames[DataPage].stopBtn.tkraise()
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
        #app.frames[DataPage].progressbar.stop()
        app.frames[DataPage].graph.update(timeVector,dataVector)
        # release_buttons()
        # app.frames[DataPage].runBtn.tkraise()
        # app.frames[DataPage].status.set('  System ready.')
        global test_counter
        test_counter += 1
        multi_test_run()
def end_testing():
    if purge_thread.is_alive() or fill_thread.is_alive() or data_thread.is_alive():
        global continueTest
        continueTest = False #Set the test flag to false, stops testing.
        release_buttons()
        app.frames[DataPage].runBtn.tkraise()
        app.frames[DataPage].status.set('  System ready.')
try:
    app = HetekGUI()
    app.mainloop()
except keyboardinterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()

