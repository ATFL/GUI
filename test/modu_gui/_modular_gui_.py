## This is an attempt to modularize tabs and better compatability.
import os
import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
## Import tab formats as required:
from parameter_settings import *
from display_graph import *

## -----> Configurations <-----
height = 640 #Window height
width = 480 #Window width
framePadding = 20


##------------------------------------------------------------------
## -----> Window <-----
master = tk.Tk()
master.title("ATFL GUI")
master.geometry(str(height)+"x"+str(width))
master.resizable(0,0)

## -----> Notebook <-----
tabControl = ttk.Notebook(master)
tabControl.pack(expand=1, fill='both')

##-----> Tabs <-----
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Parameters')
parameter_settings(tab1)

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='General')
display_graph(tab2)



master.mainloop()
