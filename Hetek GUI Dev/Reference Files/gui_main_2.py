#Last edit: 28/05/2019
# -----> System Imports <-----
import os
import sys
import datetime
import time
import threading
# -----> Tkinter Imports <------
import tkinter as tk
from tkinter import ttk
# -----> Matplotlib Imports <------
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
# -----> Auxiliary Imports <------
from gui_widgets import *
from component_dev import *
# -----> RPi Imports <------
import RPi.GPIO as GPIO
import time
import os
import Adafruit_ADS1x15
import serial
from pathlib import Path

#################### Setup ####################
class Hetek():
    def __init__(self):
        ## Declare the components of the setup
        GPIO.setmode(GPIO.BCM)
        pinLA = 27
        self.linearActuator = LinearActuator(pinLA)

        adc = Adafruit_ADS1x15.ADS1115(0x48)    # Analog-Digital Converter
        MOS_adc_channel = 3
        self.mos = MOS(adc, MOS_adc_channel) # MOS Sensor

        ## Setup Variables
        self.printing_time = 1
        self.continueTest = False
        self.sampling_time = 0.1 # time between samples taken, determines sampling frequency

        self.sensing_delay_time = 9 # normall 9, time delay after beginning data acquisition till when the sensor is exposed to sample
        self.sensing_retract_time = 130 # normally 130, time allowed before sensor is retracted, no longer exposed to sample
        self.duration_of_signal = 300 # normally 300, time allowed for data acquisition per test run

        self.start_time = 0
        self.dataVector = []
        self.timeVector = []
        self.intitialized = False
        self.initialize()

    def combined_expose_collect(self):
        sampling_time_index = 1  # sampling_time_index is used to ensure that sampling takes place every interval of sampling_time, without drifting.
        if self.initialized == False:
            self.initialize()
        else:
            pass
        if (time.time() < (self.start_time + self.duration_of_signal)) and (self.continueTest == True):  # While time is less than duration of logged file
            if (time.time() > (self.start_time + (
                    self.sampling_time * sampling_time_index)) and (self.continueTest == True)):  # if time since last sample is more than the sampling time, take another sample
                xVal = (time.time() - self.start_time)
                yVal = self.mos.read()
                self.dataVector.append(yVal)  # Perform analog to digital function, reading voltage from first sensor channel
                self.timeVector.append(xVal)
                app.frames[DataPage].graph.addData(xVal,yVal) #Adds data to live graph
                self.initialized = False
                sampling_time_index += 1

            # If time is between 10-50 seconds and the Linear Actuator position sensor signal from the ADC indicates a retracted state, extend the sensor
            elif (time.time() >= (self.start_time + self.sensing_delay_time) and time.time() <= (
                    self.sensing_retract_time + self.start_time) and (self.continueTest == True)):
                self.linearActuator.extend()

            # If time is less than 10 seconds or greater than 50 seconds and linear actuator position sensor signal from the ADC indicates an extended state, retract the sensor
            elif (((time.time() < (self.sensing_delay_time + self.start_time)) or (
                    time.time() > (self.sensing_retract_time + self.start_time)))) and (self.continueTest == True):
                self.linearActuator.retract()
            # Otherwise, keep outputs off
            else:
                self.linearActuator.retract()
        else:
            print('Data capture ended.')
            app.frames[DataPage].progressbar.stop()
            self.initialized = False
            self.continueTest = False
            combinedVector = np.column_stack((self.timeVector, self.dataVector))

            # This section of code is used for generating the output file name. The file name will contain date/time of test, as well as concentration values present during test
            current_time = datetime.datetime.now()
            year = current_time.year
            month = current_time.month
            day = current_time.day
            createFolders(year, month, day)
            hour = current_time.hour
            minute = current_time.minute
            fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + 'Mo_Neg_nolid.csv'
            #fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '_bl.csv'
            np.savetxt(r'/home/pi/Documents/Tests/' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(fileName),
                       combinedVector, fmt='%.10f', delimiter=',')
        app.after(0, self.combined_expose_collect)
        pass

    def initialize(self):
        self.start_time = time.time()  # capture the time at which the test began. All time values can use start_time as a reference
        self.dataVector = []
        self.timeVector = []  # time values associated with data values
        self.initialized = True

    def data_collect(self):
        if self.continueTest == True:
            self.combined_expose_collect()

    def start_data_collect(self):
        self.continueTest = True
        app.frames[DataPage].progressbar.start(1000)
        print('Starting data capture.')

    def stop_data_collect(self):
        app.frames[DataPage].progressbar.stop()
        self.continueTest = False


#################### GUI ####################
projectName = 'Hetek Project'
class HetekGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) #Passes all aguments to the parent class.

        self.title(projectName + ' GUI') #Title of the master window.
        self.geometry('640x480') #Initial size of the master window.
        # self.resizable(0,0) #The allowance for the master window to be adjusted by.

        canvas = tk.Frame(self) #Creates the area for which pages will be displayed.
        canvas.place(relx=0, rely=0, relheight=0.95, relwidth=1) #Defines the area which each page will be displayed.
        canvas.grid_rowconfigure(0, weight=1) #DO NOT ADJUST. Forces each frame to overlap.
        canvas.grid_columnconfigure(0, weight=1) #DO NOT ADJUST. Forces each frame to overlap.

        self.tabBar = tk.Frame(self) #Creates the area for which control buttons will be placed.
        self.tabBar.place(relx=0, rely=0.95, relheight=0.05, relwidth=1) #Defines the area for which control buttons will be placed.

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

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Home', command=lambda: controller.show_frame(HomePage)) #Creates a control button in the tabs bar.
        control_btn.pack(side='left', expand= True, fill = 'both')

        title = tk.Label(self, text=projectName, font=14, relief='solid')
        title.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.15)

        intro = '''Hetek stuff to be determined.
        [F11: Toggle Fullscreen]
        [Esc: Exit Fullscreen]'''

        introduction = tk.Label(self, text=intro, anchor='n')
        introduction.place(relx=0.1,rely=0.55,relheight=0.5,relwidth=0.8)

class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Data', command=lambda: controller.show_frame(DataPage))
        control_btn.pack(side='left', expand= True, fill = 'both')

        self.graph = LiveGraph(self)
        self.graph.place(relx=0,rely=0,relheight=0.9,relwidth=1)

        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', maximum=setup.duration_of_signal)
        self.progressbar.place(relx=0,rely=0.95,relheight=0.05,relwidth=0.8)

        runBtn = tk.Button(self, text='Run', command=lambda:setup.start_data_collect())
        runBtn.place(relx=0.8,rely=0.9,relheight=0.05,relwidth=0.2)

        stopBtn = tk.Button(self, text='Stop', command=lambda:setup.stop_data_collect())
        stopBtn.place(relx=0.8,rely=0.95,relheight=0.05,relwidth=0.2)
class ManualControlPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Manual Controls', command=lambda: controller.show_frame(ManualControlPage))
        control_btn.pack(side='left', expand= True, fill = 'both')

        #Create a termial within a parent frame.
        terminal = tk.Frame(self)
        CoreGUI(terminal)
        terminal.place(relx=0,rely=0,relheight=0.8,relwidth=1)

        controlFrame = tk.LabelFrame(self, text='System')
        controlFrame.place(relx=0,rely=0.8,relheight=0.2,relwidth=1)
        leftControlFrame = tk.Frame(controlFrame)
        leftControlFrame.place(relx=0,rely=0,relheight=1,relwidth=0.5)
        rightControlFrame = tk.Frame(controlFrame)
        rightControlFrame.place(relx=0.5,rely=0,relheight=1,relwidth=0.5)

        buttonWidth = 0.3 #Relative width of buttons within the frame
        btn_1 = tk.Button(leftControlFrame, text='1', command=lambda:'none')
        btn_1.place(relx=0,rely=0,relheight=0.45,relwidth=buttonWidth)
        btn_2 = tk.Button(leftControlFrame, text='2', command=lambda:'none')
        btn_2.place(relx=0,rely=0.5,relheight=0.45,relwidth=buttonWidth)
        btn_3 = tk.Button(rightControlFrame, text='3', command=lambda:'none')
        btn_3.place(relx=0,rely=0,relheight=0.45,relwidth=buttonWidth)
        btn_4 = tk.Button(rightControlFrame, text='4', command=lambda:'none')
        btn_4.place(relx=0,rely=0.5,relheight=0.45,relwidth=buttonWidth)

        lbl_1 = tk.Label(leftControlFrame, text='1')
        lbl_1.place(relx=buttonWidth,rely=0,relheight=0.45,relwidth=(1-buttonWidth))
        lbl_2 = tk.Label(leftControlFrame, text='2')
        lbl_2.place(relx=buttonWidth,rely=0.5,relheight=0.45,relwidth=(1-buttonWidth))
        lbl_3 = tk.Label(rightControlFrame, text='3')
        lbl_3.place(relx=buttonWidth,rely=0,relheight=0.45,relwidth=(1-buttonWidth))
        lbl_4 = tk.Label(rightControlFrame, text='4')
        lbl_4.place(relx=buttonWidth,rely=0.5,relheight=0.45,relwidth=(1-buttonWidth))

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
#
# def start_test_thread():
#     global test_thread
#     test_thread = threading.Thread(target=setup.combined_expose_collect)
#     test_thread.daemon = True
#     app.frames[DataPage].progressbar.start(1000)
#     test_thread.start()
#     app.after(20, check_test_thread)
#
# def check_test_thread():
#     if test_thread.is_alive():
#         app.after(20, check_test_thread)
#     else:
#         app.frames[DataPage].progressbar.stop()




#--------------------------------------
try:
    setup = Hetek()
    app = HetekGUI()
    app.after(0,setup.combined_expose_collect)
    app.mainloop()
except keyboardinterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
