import tkinter as Tk
from tkinter import *
from tkinter import ttk

""" Import the appropriate functions for the tasks needed"""

from motor_print import run_motor

"""create the window, size, color, and packing"""


w, h = 800, 455 #Window Size
window = Tk()
window.title("ATFL - Metro Vancouver") #Include the name of the window
canvas = Canvas(window)
canvas.pack()

"""create the tabs, the windows and the names"""



tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl) #making a frame
tabControl.add(tab1, text='Main Screen') #properties of the Frame

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Advanced')

tabControl.pack(expand=1, fill='both')


"""include the appropriate functions that are going to be used"""

run_count = 0
def push_button ():
    global run_count #need this to have a counter
    run_motor()
    run_count += 1
    print("done run " + str(run_count)) #make sure the value is in string format

"""Ordering and structure of tabs"""


b = Button(tab1, text="Run Motor", command=push_button)
b.pack()

c = Button(tab2, text="Run Valve", command =push_button)
c.pack()


"""Final code"""

canvas.configure(background='black')
window.mainloop()
