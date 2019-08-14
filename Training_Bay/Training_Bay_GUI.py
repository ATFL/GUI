import os
#import system
import datetime
from time import *
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
#UNCOMMENT FOR RPI
from gui_widgets import *

# import RPi.GPIO as GPIO
# import time
# import Adafruit_ADS1x15 as ads
# import serial
# from pathlib import Path
# #---->
# import numpy as np
# # import sklearn
# # import pickle

#################### Color Settings ####################
warning_color = '#FFC300'
tabBar_color = '#85929E'
tabBarActive_color = '#AEB6BF'
runBtn_color = '#9DE55F'
stopBtn_color = '#FF4E4E'

class Training_Bay(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        self.title('Training Bay')
        self.geometry('640x480')

        canvas = tk.Frame(self)
        canvas.place(relx=0,rely=0,relheight=0.9,relwidth=1)
        canvas.grid_rowconfigure(0,weight=1)
        canvas.grid_columnconfigure(0,weight=1)

        self.tabBar = tk.Frame(self,bg = '#85929E')
        self.tabBar.place(relx=0, rely=0.9, relheight=0.1, relwidth=1)
        self.frames = {}

        # for f in (Home):   #,sensor1,sensor2,sensor3,sensor4,sensor5,sensor6,sensor7,sensor8)
        #     frame = f(canvas,self)
        #     self.frames[f] = frame #Add the created frame to the 'frames' dictionary.
        #     frame.grid(row=0, column=0, sticky="nsew") #Overlaps the frame in the same grid space.
        frame = Home(canvas,self)
        self.frames[1] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Home) #Sets the default page.

        self.attributes("-fullscreen", True)
        self.fullscreen = True
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

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

class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        control_btn = tk.Button(controller.tabBar, text='Home', bg=tabBar_color, activebackground=tabBarActive_color, bd=0, command=lambda: controller.show_frame(HomePage)) #Creates a control button in the tabs bar.
        control_btn.pack(side='left', expand= True, fill = 'both')

        for i in range(0,8):
            self.graph[i] = AutoLiveGraph(self,timeVector[i],DataVector[i])
            if i <4:
                self.graph[i].pack(side = LEFT)
            else:
                self.graph[i].pack(side= RIGHT)

class SensorPage(tk.Frame):
    def __init(self,parent,controller):
        tk.Frame.__init__(self,parent)
        control_btn = tk.Button(controller.tabBar, text='')
app = Training_Bay()
app.mainloop()
# except keyboardinterrupt:
#     print("Keyboard Error")
# finally:
#     print("No Error")
