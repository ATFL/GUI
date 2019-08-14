#!/bin/

### THIS FILE CONTAINS ALL THE CODE TO START AND CONTROL THE EXPERIMENT, AS WELL
### AS THE REQUIRED BUTTONS AND GUI TOOLS

######### TO WORK WITH RASPBERRY PI ##############


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
from H2_components_v2 import *
# -----> RPi Imports <------
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ads
import serial
from pathlib import Path

#-----> Machine Learning <-----
import numpy as np
# import sklearn
# import pickle

#################### Object Declaration ####################
GPIO.setmode(GPIO.BOARD)
### Include the components required for your Setup
### i.e. Linear Actuator, Valve, Pump, Servo

################## EXPERIMENTAL STEPS ################
### Allows you to keep track of what your setup has to do
### purely Commented notes

#STEP 1: PURGE BOX::: V1:N V2:N V3:N V4:N V5:Y V6:Y
#STEP 2: FILL METHANE P1::: V1:Y V2:N V3:Y V4:N V5:N V6:N
#STEP 3: FILL METHANE P2::: V1:Y V2:N V3:N V4:Y V5:N V6:Y
#STEP 4: FILL H2 P1::: V1:N V2:Y V3:Y V4:N V5:N V6:N
#STEP 5: FILL H2 P2::: V1:N V2:Y V3:N V4:Y V5:N V6:Y
#STEP 6: TEST::: V1:N V2:N V3:N V4:N V5:N V6:N

#################### System Variables ####################

### Any Variables that your system requires such as
### timing, amounts, length, colours

#################### Data Array ####################
# DO NOT TOUCH #
### Normally For gas Sensing, we use this structure to obtain data
dataVector = []
timeVector = []

#################### GUI ####################
### This is where the GUI starts
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

        ### Our system has 3 pages, include how many ever your project needs
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
        ### This is a splash screen to start off on, not required.
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

        # self.contFill = tk.Button(self.run_and_stop, text='CONTINUE', bg=runBtn_color, activebackground=runBtn_color, command=lambda:start_fill_thread())
        # self.contFill.grid(row=0, column=0, sticky="nsew")

        self.runBtn = tk.Button(self.run_and_stop, text='RUN', bg=runBtn_color, activebackground=runBtn_color, command=lambda:multi_test_run())
        self.runBtn.grid(row=0, column=0, sticky="nsew")


        statusFrame = tk.LabelFrame(self, text ='Status')
        statusFrame.place(relx=0.8,rely=0.3,relheight=0.6,relwidth=0.2)

        responseFrame = tk.Frame(self)
        responseFrame.place(relx=0.8,rely=0,relheight=0.3,relwidth=0.2)


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

        #This is an example of how buttons are made. Place them how you need it
        buttonWidth = 0.4 #Relative width of buttons within the frame
        self.btn_1 = tk.Button(controlFrame, text='Extend Linear Actuator', command=lambda:linearActuator.extend())
        self.btn_1.place(relx=0,rely=0,relheight=0.1,relwidth=buttonWidth)
        self.btn_2 = tk.Button(controlFrame, text='Retract Linear Actuator', command=lambda:linearActuator.retract())
        self.btn_2.place(relx=0,rely=0.1,relheight=0.1,relwidth=buttonWidth)

def suppress_buttons():
    ### This function disables buttons when the program is running
    app.frames[ManualControlPage].btn_1.config(state='disabled')
    app.frames[HomePage].exitBtn.config(state='disabled')
    app.frames[HomePage].shutdownBtn.config(state='disabled')

def release_buttons():
    ### This function enables button after completion
    app.frames[ManualControlPage].btn_1.config(state='normal')
    app.frames[HomePage].exitBtn.config(state='normal')
    app.frames[HomePage].shutdownBtn.config(state='normal')

########## Experimental Functions ################
### This is where you include functions to control each STEP
### The following functions are examples on how to purge and fill chambers
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
        if valve5.state != True:
            valve5.enable()
        if valve6.state != True:
            valve6.enable()
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
    if linearActuator.state != 'retracted':
        linearActuator.retract()
    #########FILL METHANE############

    start_time = time.time()
    print("Filling Chamber with methane \n V1:Y V2:N V3:N V4:Y V5:N V6:N")
    while time.time() < (start_time + fill_methane_time[test_counter]) and continueTest == True:
        if valve1.state != True:
            valve1.enable()
        if valve2.state != False:
            valve2.disable()
        if valve3.state != False:
            valve3.disable()
        if valve4.state != True:
            valve4.enable()
        if valve5.state != False:
            valve5.disable()
        if valve6.state != True:
            valve6.enable()
        pass
    print("Done Filling Methane \n V1:N V2:N V3:N V4:N V5:N V6:N")
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

    ########END METHANE FILL########

    #######FILL HYDROGEN ##############

    start_time = time.time()
    print("Filling Chamber with Hydrogen \n V1:N V2:Y V3:N V4:Y V5:N V6:N")
    while time.time() < (start_time + fill_hydrogen_time[test_counter]) and continueTest == True:
        if valve1.state != False:
            valve1.disable()
        if valve2.state != True:
            valve2.enable()
        if valve3.state != False:
            valve3.disable()
        if valve4.state != True:
            valve4.enable()
        if valve5.state != False:
            valve5.disable()
        if valve6.state != False:
            valve6.disable()
        pass
    print("Done Filling Hydrogen \n V1:N V2:N V3:N V4:N V5:N V6:N")
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

### Here we have the function to start collecting data from sensors for gas sensing projects
### Modify accordingly
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

### The following functions are used for multithreading functionality. Remove if not needed
### Used in gas sensing projects
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

### This is used to ensure the GUI runs, and can handle errors
try:
    app = HetekGUI()
    app.mainloop()
except keyboardinterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
