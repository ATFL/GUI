#!/usr/bin/python3
#Last edit: 28/05/2019
# -----> System Imports <-----
import os
import sys
import time
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
from hetek_components import *
# -----> RPi Imports <------
import RPi.GPIO as GPIO
import time
import os
import Adafruit_ADS1x15
import serial
from pathlib import Path
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
# Temperature sensor
Temp_adc_channel = 1
temperatureSensor = TemperatureSensor(adc, Temp_adc_channel)
# Valves
pinInValve = 3
inValve = Valve('Inlet Valve', pinInValve)
pinOutValve = 10
outValve = Valve('Outlet Valve', pinOutValve)
# Pump
pinPump = 16
pump = Pump(pinPump)
#################### System Variables ####################
# Purging Variables
clean_chamber_purge_time = 30 # normally 30s
sensing_chamber_purge_time = 60 # normally 60s
# Filling Variables
chamber_fill_time = 45 # normally 45, fill the sensing chamber with the outlet valve open.
chamber_force_fill_time = 1 # normally .5, fill the sensing chamber without an outlet.

# Testing Variables
sampling_time = 0.1 # time between samples taken, determines sampling frequency
sensing_delay_time = 10 # normall 10, time delay after beginning data acquisition till when the sensor is exposed to sample
sensing_retract_time = 60 # normally 60, time allowed before sensor is retracted, no longer exposed to sample
duration_of_signal = 150 # normally 150, time allowed for data acquisition per test run
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
        self.btn_7 = tk.Button(controlFrame, text='Switch Outlet Valve', command=lambda:outValve.switch())
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

def createFolders(year, month, day):
    ##  Get the path for the folders by year, month and day
    year_path = '/home/pi/Documents/Tests/' + str(year)
    year_folder = Path(year_path)
    month_path = '/home/pi/Documents/Tests/' + str(year) + '/' + str(month)
    month_folder = Path(month_path)
    day_path = '/home/pi/Documents/Tests/' + str(year) + '/' + str(month) + '/' + str(day)
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

def purge_system():
    if linearActuator.state != 'default':
        linearActuator.default()

    # Purge the sensing chamber.
    start_time = time.time() # Time at which the purging starts.
    while time.time() < (start_time + sensing_chamber_purge_time) and continueTest == True:
        if pump.state != True:
            pump.enable()
        if inValve.state != True:
            inValve.enable()
        if outValve.state != True:
            outValve.enable()

    # Purge the clean chamber.
    start_time = time.time() #Reset the time at which purging starts.
    while time.time() < (start_time + clean_chamber_purge_time) and continueTest == True:
        if pump.state != True:
            pump.enable()
        if inValve.state != False:
            inValve.disable()
        if outValve.state != False:
            outValve.disable()

    pump.disable() # Turn off the pump after purging.
    pass

def fill_chamber():
    if linearActuator.state != 'retracted':
        linearActuator.retract()

    # Fill the sensing chamber normally.
    start_time = time.time()
    while time.time() < (start_time + chamber_fill_time) and continueTest == True:
        if pump.state != True:
            pump.enable()
        if inValve.state != True:
            inValve.enable()
        if outValve.state != True:
            outValve.enable()

    # Focfully fill the sensing chamber.
    start_time = time.time()
    while time.time() < (start_time + chamber_force_fill_time) and continueTest == True:
        if pump.state != True:
            pump.enable()
        if inValve.state != True:
            inValve.enable()
        if outValve.state != False:
            outValve.disable()

    pump.disable()
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
    if inValve.state != True:
        inValve.enable()
    if outValve.state != False:
        outValve.disable()

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

    combinedVector = np.column_stack((timeVector, dataVector))

    # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    createFolders(year, month, day)
    hour = current_time.hour
    minute = current_time.minute
    fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + 'Hetek_HH.csv'
    #fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_bl.csv'
    np.savetxt(r'/home/pi/Documents/Tests/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(fileName),
               combinedVector, fmt='%.10f', delimiter=',')
    pass

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
    app.frames[DataPage].progressbar.start((clean_chamber_purge_time+sensing_chamber_purge_time)*10)
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
    app.frames[DataPage].progressbar.start((chamber_fill_time+chamber_force_fill_time)*10)
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
        app.frames[DataPage].naturalGasLabel.config(bg=warning_color)
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
