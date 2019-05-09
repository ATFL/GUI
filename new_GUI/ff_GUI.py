import tkinter as Tk
from tkinter import *
from tkinter import ttk

""" Step 1. One window with four frames """

"""create the window, size, color, and packing"""


w, h = 640,480  #Window Size
window = Tk()
window.title("ATFL - Metro Vancouver") #Include the name of the window


"""create the tabs, the windows and the names"""


upperLeft = Frame(width=50, height=50, bg="red", colormap="new")
upperLeft.pack(anchor = NW, side = LEFT )


upperRight = Frame(width = 50, height = 50, bg = "blue", colormap= "new")
upperRight.pack(anchor = NE, side = RIGHT)


lowerLeft = Frame(width = 50, height = 50, bg = "green", colormap = "new")
lowerLeft.pack(anchor = SW, side = LEFT)

lowerRight = Frame(width = 50, height = 50, bg = "orange", colormap = "new")
lowerRight.pack(anchor = SE, side = RIGHT) 

""" Step 2. One window with four tabs"""


""" Step 3. One window with four tabs live stream"""

window.mainloop()
