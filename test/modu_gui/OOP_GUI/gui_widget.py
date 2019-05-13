import tkinter
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Widget(Frame):
    def __init__(self, master):
        self.frame = Frame(master)

    def placeWidget(self, relx, rely, relw, relh):
        self.frame.place(relx=relx, rely=rely, relwidth=relw, relheight=relh)

class SimpleCounter(Widget):
    _value = 0

    def __init__(self,master):
        super().__init__(master)
        self.Var = StringVar()
        self.Var.set(self._value)

        countButton = Button(self.frame, text='Count', command = lambda: self.countPress())
        countButton.place(relx=0.5, rely=0, relheight=0.5, relwidth=0.5)

        resetButton = Button(self.frame, text='Reset', command = lambda: self.resetPress())
        resetButton.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5)

        display = Label(self.frame, anchor='center', textvariable=self.Var)
        display.place(relx=0, rely=0, relheight=1, relwidth=0.5)

    def countPress(self):
        self._value = self._value + 1
        self.Var.set(self._value)

    def resetPress(self):
        self._value = 0
        self.Var.set(self._value)

    def get(self):
        return self._value

    def set(self, number):
        self._value = number
        self.Var.set(self._value)


class SettingScrollBar(Widget):
    _value = 0
    _variableName = ' '

    def __init__(self, master):
        super().__init__(master)
        self.var = IntVar()
        self.var.set(self._value)
        self.name = StringVar()
        self.name.set(self._variableName)

        display = Label(self.frame, anchor='center', textvariable= self.var, bg='light blue')
        display.place(relx=0.8, rely=0, relheight=0.6, relwidth=0.2)

        settingName = Label(self.frame, anchor='center', textvariable= self.name, bg='sky blue')
        settingName.place(relx=0, rely=0, relheight=0.6, relwidth=0.8)

        scale = Scale(self.frame,orient='horizontal', showvalue=0, width=30, variable= self.var,  bg='light grey')
        scale.place(relx=0.1, rely=0.6, relheight=0.4, relwidth=0.8)

        Lbutton = Button(self.frame, text='<', command= lambda: self.LPress(),  bg='grey')
        Lbutton.place(relx=0, rely=0.6, relheight=0.4, relwidth=0.1)
        Rbutton = Button(self.frame, text='>', command= lambda: self.RPress(),  bg='grey')
        Rbutton.place(relx=0.9, rely=0.6, relheight=0.4, relwidth=0.1)

    def LPress(self):
        self._value = self.var.get()
        if self._value > 0:
            self._value = self._value - 1
        self.var.set(self._value)

    def RPress(self):
        self._value = self.var.get()
        if self._value < 100:
            self._value = self._value + 1
        self.var.set(self._value)

    def get(self):
        return self._value

    def set(self, num):
        self._value = num
        self.var.set(self._value)

    def variable1(self, name):
        self._variableName = str(name)
        self.name.set(self._variableName)

class LiveGraph(Widget):
    def __init__(self, master):
        super().__init__(master)

    def plotGraph(self):
        fig = Figure(figsize=(5,5), dpi=100)
        data = fig.add_subplot(111)
        data.plot([1,2,3,4,5,6,7,8], [5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(fig, self.frame)
        canvas.show()
        canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)


    def matplotCanvas(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        # canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
