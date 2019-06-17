import tkinter
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui_widget import *


HEIGHT = '640'
WIDTH = '480'

def main():

    root = Tk()
    root.geometry(HEIGHT + 'x' + WIDTH)
    root.resizable(0,0)

    simpleCounter = SimpleCounter(root)
    simpleCounter.placeWidget(0.1,0.1,0.4,0.4)

    setting_1 = SettingScrollBar(root,'temperature',0,1000)
    setting_1.placeWidget(0.1,0.5,0.4,0.1)





    root.mainloop()

main()
