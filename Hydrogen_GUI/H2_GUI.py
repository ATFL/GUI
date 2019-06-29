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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
# -----> Auxiliary Imports <------
from gui_widgets import *
from H2_components import *
# -----> RPi Imports <------
import RPi.GPIO as GPIO
import time
import os
import Adafruit_ADS1x15
import serial
from pathlib import Path

#---->
import numpy as np
import sklearn
import pickle

#################### Object Declaration ####################
GPIO.setmode(GPIO.BOARD)
# Linear Actuator
pinLA = 12
pinEnable = 18
linearActuator = LinearActuator(pinLA, pinEnable)
# Analog-Digital Converter
adc = Adafruit_ADS1x15.ADS1115(0x48)
# MOS Sensor
MOS_adc_channel = 0
mos = MOS(adc, MOS_adc_channel)
# Pressure sensor
press_adc_channel = 1
pressSensor = PressureSensor(adc,press_adc_channel)

# Valves

pinvalve1 = 10
pinvalve2 = 11
pinvalve3 = 12
pinvalve4 = 13
pinvalve5 = 14
pinvalve6 = 15

valve1 = Valve('Valve1',pinvalve1) #lets clean air into chamber
valve2 = Valve('Valve2',pinvalve2) #lets Methane into chamber
valve3 = Valve('Valve3',pinvalve3) #lets Hydrogen into chamber
valve4 = Valve('Valve4',pinvalve4) #venting valve to clean methane fill line
valve5 = Valve('Valve5',pinvalve5) #venting valve to clean hydrogen fill line
valve6 = Valve('Valve6',pinvalve6) #output vent valve

################## EXPERIMENTAL STEPS ################


#STEP 1: PURGE BOX::: V1:Y V2:N V3:N V4:N V5:N V6:Y
#STEP 2: CLENSE FILL LINE::: V1:N V2:N V3:N V4:Y V5:Y V6:N
#STEP 3: FILL CHAMBER::: V1:N V2:Y V3:Y V4:N V5:N V6:Y
#STEP 4: TEST::: V1:N V2:N V3:N V4:N V5:N V6:N

#################### System Variables ####################

#PURGING VARIABLES
chamber_purge_time = 120 #Time to purge chamber: experiment with it


#########FILLING CHAMBER WITH TARGET GAS #############
# Filling Variables
fill_line_clense_time = 20


######## SAMPLE INJECTION CONCENTRATIONS ##########
methane_injection_conc = 1000 #Whatever vales you need
hydrogen_injection_conc = 1000 #whatever values you need
##############################################33333

fill_methane_time = 0
methane_correction_factor = #found it on MKS website
methane_flow_rate = #what the value on the MFC is set to
methane_injection_amount = methane_injection_conc / 500 # mL
fill_methane_time = ( 60 * ( 1 / methane_correction_factor ) * metane_injection_amount ) / methane_flow_rate  # Time in seconds

fill_hydrogen_time =  0
hydrogen_correction_factor = #found it on MKS website
hydrogen_flow_rate = #what the value on the MFC is set to
hydrogen_injection_amount = hydrogen_injection_conc / 500 # mL
fill_hydrogen_time = ( 60 * ( 1 / hydrogen_correction_factor ) * hydrogen_injection_amount ) / methane_flow_rate  # Time in seconds

#########################################################\

# Testing Variables
sampling_time = 0.1 # tim50e between samples taken, determines sampling frequency
sensing_delay_time = 5 # normall 5, time delay after beginning data acquisition till when the sensor is exposed to sample
sensing_retract_time = 50 # normally 50, time allowed before sensor is retracted, no longer exposed to sample
duration_of_signal = 200 # normally 150, time allowed for data acquisition per test run

total_time = chamber_purge_time + fill_line_clense_time + max(fill_methane_time,fill_hydrogen_time) + duration_of_signal

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
projectName = 'Hetek Project'
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

        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', maximum=100)
        self.progressbar.place(relx=0,rely=0.97,relheight=0.03,relwidth=0.8)

        self.run_and_stop = tk.Frame(self)
        self.run_and_stop.place(relx=0.8,rely=0.9,relheight=0.1,relwidth=0.2)
        self.run_and_stop.grid_rowconfigure(0, weight=1) #DO NOT ADJUST. Forces buttons to overlap.
        self.run_and_stop.grid_columnconfigure(0, weight=1) #DO NOT ADJUST.

        self.stopBtn = tk.Button(self.run_and_stop, text='STOP', bg=stopBtn_color, activebackground=stopBtn_color, command=lambda:end_testing())
        self.stopBtn.grid(row=0, column=0, sticky="nsew")

        self.contFill = tk.Button(self.run_and_stop, text='CONTINUE', bg=runBtn_color, activebackground=runBtn_color, command=lambda:start_fill_thread())
        self.contFill.grid(row=0, column=0, sticky="nsew")

        self.runBtn = tk.Button(self.run_and_stop, text='RUN', bg=runBtn_color, activebackground=runBtn_color, command=lambda:start_purge_thread())
        self.runBtn.grid(row=0, column=0, sticky="nsew")


        statusFrame = tk.LabelFrame(self, text ='Status')
        statusFrame.place(relx=0.8,rely=0.3,relheight=0.6,relwidth=0.2)

        responseFrame = tk.Frame(self)
        responseFrame.place(relx=0.8,rely=0,relheight=0.3,relwidth=0.2)
        self.naturalGasLabel = tk.Label(responseFrame, text = 'Natural Gas\n Detected', relief='groove', borderwidth=2, anchor='center')
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
        self.btn_3 = tk.Button(controlFrame, text='Default Linear Actuator', command=lambda:linearActuator.default())
        self.btn_3.place(relx=0,rely=0.2,relheight=0.1,relwidth=buttonWidth)
        self.btn_4 = tk.Button(controlFrame, text='Read MOS', command=lambda:mos.print())
        self.btn_4.place(relx=0,rely=0.3,relheight=0.1,relwidth=buttonWidth)
        self.btn_5 = tk.Button(controlFrame, text='Read Temperature Sensor', command=lambda:temperatureSensor.print())
        self.btn_5.place(relx=0,rely=0.4,relheight=0.1,relwidth=buttonWidth)
        self.btn_6 = tk.Button(controlFrame, text='Switch Inlet Valve', command=lambda:inValve.switch())
        self.btn_6.place(relx=0,rely=0.5,relheight=0.1,relwidth=buttonWidth)
        self.btn_7 = tk.Button(controlFrame, text='Switch Outlet Valve', command=lambda:inValve.switch())
        self.btn_7.place(relx=0,rely=0.6,relheight=0.1,relwidth=buttonWidth)
        self.btn_8 = tk.Button(controlFrame, text='Switch Pump', command=lambda:pump.switch())
        self.btn_8.place(relx=0,rely=0.7,relheight=0.1,relwidth=buttonWidth)

        lbl_1 = tk.Label(controlFrame, text='  Extend the linear actuator to the sensing chamber.', anchor='w')
        lbl_1.place(relx=buttonWidth,rely=0,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_2 = tk.Label(controlFrame, text='  Retract the linear actuator to the clean chamber.', anchor='w')
        lbl_2.place(relx=buttonWidth,rely=0.1,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_3 = tk.Label(controlFrame, text='  Reset the linear to the default (center) position.', anchor='w')
        lbl_3.place(relx=buttonWidth,rely=0.2,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_4 = tk.Label(controlFrame, text='  Read the current value of the MOS (gas) sensor.', anchor='w')
        lbl_4.place(relx=buttonWidth,rely=0.3,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_5 = tk.Label(controlFrame, text='  Read the current internal temperature of the device.', anchor='w')
        lbl_5.place(relx=buttonWidth,rely=0.4,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_6 = tk.Label(controlFrame, text='   Toggle the inlet valve.', anchor='w')
        lbl_6.place(relx=buttonWidth,rely=0.5,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_7 = tk.Label(controlFrame, text='   Toggle the outlet valve.', anchor='w')
        lbl_7.place(relx=buttonWidth,rely=0.6,relheight=0.1,relwidth=(1-buttonWidth))
        lbl_8 = tk.Label(controlFrame, text='  Toggle the pump.', anchor='w')
        lbl_8.place(relx=buttonWidth,rely=0.7,relheight=0.1,relwidth=(1-buttonWidth))

        # # TODO: add more buttons1

def suppress_buttons():
    app.frames[ManualControlPage].btn_1.config(state='disabled')
    app.frames[ManualControlPage].btn_2.config(state='disabled')
    app.frames[ManualControlPage].btn_3.config(state='disabled')
    app.frames[ManualControlPage].btn_4.config(state='disabled')
    app.frames[ManualControlPage].btn_5.config(state='disabled')
    app.frames[ManualControlPage].btn_6.config(state='disabled')
    app.frames[ManualControlPage].btn_7.config(state='disabled')
    app.frames[ManualControlPage].btn_8.config(state='disabled')
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
    app.frames[HomePage].exitBtn.config(state='normal')
    app.frames[HomePage].shutdownBtn.config(state='normal')

def purge_system():
    print("Test will take %d seconds",total_time)
    start_time = time.time()
    while time.time() < (start_time + chamber_purge_time) and continueTest == True:
        if linearActuator.state != 'extended':
            linearActuator.extend()
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
        if valve6.state != True:
            valve6.enable()

    linearActuator.retract()
    pass

def fill_chamber():
    if linearActuator.state != 'retracted':
        linearActuator.retract()
    #Cleansing Fill Lines
    start_time = time.time()
    while time.time() < (start_time + fill_line_clense_time) and continueTest == True:
        if valve1.state != False:
            valve1.disable()
        if valve2.state != False:
            valve2.disable()
        if valve3.state != False:
            valve3.disable()
        if valve4.state != True:
            valve4.enable()
        if valve5.state != True:
            valve5.enable()
        if valve6.state != False:
            valve6.disable()

    # Filling the chamber
    start_time = time.time()

    if fill_methane_time > fill_hydrogen_time:
        while time.time() < (start_time + fill_hydrogen_time) and continueTest == True:
            if valve1.state != False:
                valve1.disable()
            if valve2.state != True:
                valve2.enable()
            if valve3.state != True:
                valve3.enable()
            if valve4.state != False:
                valve4.disable()
            if valve5.state != False:
                valve5.disable()
            if valve6.state != True:
                valve6.enable()
        while time.time() > (start_time + fill_hydrogen_time) and time.time() < (start_time + fill_methane_time) and continueTest == True:
            valve3.disable()
        pass

    elif fill_hydrogen_time > fill_methane_time:
        while time.time() < (start_time + fill_methane_time) and continueTest == True:
            if valve1.state != False:
                valve1.disable()
            if valve2.state != True:
                valve2.enable()
            if valve3.state != True:
                valve3.enable()
            if valve4.state != False:
                valve4.disable()
            if valve5.state != False:
                valve5.disable()
            if valve6.state != True:
                valve6.enable()
        while time.time() > (start_time + fill_methane_time) and time.time() < (start_time + fill_hydrogen_time) and continueTest == True:
            valve2.disable()
        pass

    pass

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

    print('Starting data capture.')
    while (time.time() < (start_time + duration_of_signal)) and (continueTest == True):  # While time is less than duration of logged file
        if (time.time() > (start_time + (sampling_time * sampling_time_index)) and (continueTest == True)):  # if time since last sample is more than the sampling time, take another sample
            dataVector.append(mos.read())  # Perform analog to digital function, reading voltage from first sensor channel
            timeVector.append(time.time() - start_time)
            sampling_time_index += 1

        # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
        elif (time.time() >= (start_time + sensing_delay_time) and time.time() <= (
                sensing_retract_time + start_time) and (continueTest == True)):
            if linearActuator.state != 'retracted':
                linearActuator.retract()

        # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
        elif (((time.time() < (sensing_delay_time + start_time)) or (
                time.time() > (sensing_retract_time + start_time)))) and (continueTest == True):
            if linearActuator.state != 'extended':
                linearActuator.extend()

        # Otherwise, keep outputs off
        else:
            if linearActuator.state != 'extended':
                linearActuator.extend()

    combinedVector = np.column_stack((timeVector, dataVector))

    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    filename = strftime("testsP/%a %d %b %Y %H%M%S.csv",localtime())
    np.savetxt(filename,combinedVector, fmt='%.10f', delimiter=',')



    pass

# def multi_test_run():
#
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
    app.frames[DataPage].progressbar.start((chamber_purge_time)*10)
    purge_thread.start()
    app.after(20, check_purge_thread)

def check_purge_thread():
    if purge_thread.is_alive():
        app.after(20, check_purge_thread)
    else:
        app.frames[DataPage].progressbar.stop()
        if continueTest ==True:
            app.frames[DataPage].contFill.tkraise()

def start_fill_thread():
    suppress_buttons()
    app.frames[DataPage].stopBtn.tkraise()
    global fill_thread
    global continueTest
    continueTest = True
    fill_thread = threading.Thread(target=fill_chamber)
    fill_thread.daemon = True
    app.frames[DataPage].status.set('  Filling sample chamber...')
    app.frames[DataPage].progressbar.start(max(fill_methane_time,fill_hydrogen_time)*10)
    fill_thread.start()
    app.after(20, check_fill_thread)

def check_fill_thread():
    if fill_thread.is_alive():
        app.after(20, check_fill_thread)
    else:
        app.frames[DataPage].progressbar.stop()
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
    app.frames[DataPage].progressbar.start(duration_of_signal*10)
    data_thread.start()
    app.after(20, check_data_thread)

def check_data_thread():
    if data_thread.is_alive():
        app.after(20, check_data_thread)
    else:
        app.frames[DataPage].progressbar.stop()
        app.frames[DataPage].graph.update(timeVector,dataVector)
        release_buttons()
        app.frames[DataPage].runBtn.tkraise()
        app.frames[DataPage].status.set('  System ready.')

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
