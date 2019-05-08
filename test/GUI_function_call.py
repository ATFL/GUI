from motor_print import run_motor
import tkinter as Tk
from tkinter import *

run_count = 0
def push_button ():
    global run_count #need this to have a counter
    run_motor()
    run_count += 1
    print("done run " + str(run_count)) #make sure the value is in string format

master = Tk()

b = Button(master, text="Run Motor", command=push_button)
b.pack()

master.mainloop()
