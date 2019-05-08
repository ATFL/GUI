import tkinter as Tk
from tkinter import *
from tkinter import ttk
from motor_print import run_motor

master = Tk()

master.title("ATFL GUI")

w,h = 500,500
canvas = Canvas(master, width=w, height=h)
canvas.pack()
tabControl = ttk.Notebook(master)

tab1 = ttk.Frame(tabControl) #making a frame
tabControl.add(tab1, text='Main Screen') #properties of the fram
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Advanced')

tabControl.pack(expand=1, fill='both')

run_count = 0
def push_button ():
    global run_count #need this to have a counter
    run_motor()
    run_count += 1
    print("done run " + str(run_count)) #make sure the value is in string format


b = Button(tab1, text="Run Motor", command=push_button)
b.pack()

c = Button(tab2, text="Run Valve", command =push_button)
c.pack()

canvas.configure(background='black')
master.mainloop()
