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

    # simpleCounter = SimpleCounter(root)
    # simpleCounter.widgetPos(0.1,0.1,0.8,0.8)

    # setting_1 = SettingScrollBar(root)
    # setting_1.widgetPos(0.1,0.1,0.8,0.2)

    graph = LiveGraph(root)
    graph.plotGraph()



    root.mainloop()

main()
