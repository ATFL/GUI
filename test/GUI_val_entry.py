import tkinter as Tk
from tkinter import *
from tkinter import ttk

window = Tk()
canvas = Canvas(window)
canvas.pack()

@staticmethod
def show():
    l = Label(window,text=e.get())
    l.place(x=30,y=30)
    l.pack()

e = Entry(window)
e.insert(12,"123")
e.pack(side='left')
e.bind('<Return>',show)

window.mainloop()
