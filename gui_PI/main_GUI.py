#! /usr/bin/python3
import datetime
import os
import tkinter
from tkinter import ttk
from gui_widget import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import random
style.use('ggplot')


w, h = 640, 480 #Window Size
window = Tk()
window.title("ATFL - Metro Vancouver") #Include the nameof the window
window.geometry("500x350")
canvas = Canvas(window)
canvas.pack(expand = False, fill ='both')

"""create the tabs, the windows and the names"""


tabControl = ttk.Notebook(canvas)

tab1 = ttk.Frame(tabControl) #making a frame
tabControl.add(tab1, text='Screen 1') #properties of the Frame



left = Frame(tab1, borderwidth=2, relief="solid")
right = Frame(tab1, borderwidth=2, relief="solid")
box1 = Frame(left, borderwidth=2, relief="solid")

newGraph = Figure()
newGraph.set_size_inches(2,2,forward=True)
newPlot = newGraph.add_subplot(111)

xList = [1,2,3,4,5,6,7,8]
yList = [5,6,1,3,8,9,3,5]

newPlot.plot(xList, yList)
newCanvas = FigureCanvasTkAgg(newGraph, box1)
newCanvas.draw()
newCanvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)
newToolbar = NavigationToolbar2Tk(newCanvas,box1)
newToolbar.update()
newCanvas._tkcanvas.pack(side=TOP, fill = BOTH, expand = True)



def purge1Callback():
    print ("This will be replaced with the required purge 1 actions")
    
def purge2Callback():
    print("This will be replaced with the required purge 2 actions")

def runCallback():
    print("This will be replaced with the required run actions")
    
def stopCallback():
    print("This will be replaced with the required stop actions")
    
box2 = Button(right, text = "Purge 1", font= ("Verdana", 7), command = purge1Callback)
box3 = Button(right, text = "Purge 2", font = ("Verdana",7), command = purge2Callback)
box4 = Button(right, text = "Run", font = ("Verdana", 7), command = runCallback)
box5 = Button(right, text = "Stop", font= ("Verdana", 7), command = stopCallback)

label1 = Canvas(box1)


left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
box1.pack(expand=True, fill="both", padx=10, pady=10)
label1.pack()
box2.pack(expand = True, fill = "both", padx =10, pady= 10)
box3.pack(expand = True, fill = "both", padx = 10, pady = 10)
box4.pack(expand = True, fill = "both", padx = 10, pady = 10)
box5.pack(expand = True, fill = "both", padx = 10, pady = 10)

#-----> Tab 2 <-----


tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Screen 2')

left2 = Frame(tab2, borderwidth=2, relief="solid")
right2 = Frame(tab2, borderwidth=2, relief="solid")
bottom2 = Frame(tab2, borderwidth=2, relief = "solid")
t2box1 = Frame(left2, borderwidth=2, relief="solid")
t2box2 = Frame(left2, borderwidth=2, relief="solid")
t2box3 = Frame(left2, borderwidth=2, relief = "solid")
t2box4 = Frame(right2, borderwidth=2, relief = "solid")
t2box5 = Frame(right2, borderwidth=2, relief = "solid")
t2box6 = Frame(right2, borderwidth=2, relief = "solid")


t2Label1 = Label(t2box1, text="First Value")
t2Label1.config(font = ("Verdana", 7))

t2Label2 = Label(t2box2, text="Second Value")
t2Label2.config(font = ("Verdana",7))

t2Label3 = Label(t2box3, text="Third Value")
t2Label3.config(font = ("Verdana", 7))


t2Label4 = Label(t2box4, text="Fourth Value")
t2Label4.config(font=("Verdana", 7))


t2Label5 = Label(t2box5, text="Fifth Value")
t2Label5.config(font = ("Verdana", 7))

t2Label6= Label(t2box6, text="Sixth Value")
t2Label6.config(font = ("Verdana", 7))


setting_1 = SettingScrollBar(t2box1, 'Temperature', 0, 100)
setting_1.placeWidget(0.1, 0.4, 0.8, 0.5)

setting_2 = SettingScrollBar(t2box2, 'Pressure', 0, 30)
setting_2.placeWidget(0.1, 0.4, 0.8, 0.5) 

setting_3 = SettingScrollBar(t2box3, 'Temperature', 0, 50) 

setting_3.placeWidget(0.1, 0.4, 0.8, 0.5)

setting_4 = SettingScrollBar(t2box4, 'Temperature', 0, 50)
setting_4.placeWidget(0.1, 0.4, 0.8, 0.5) 

setting_5 = SettingScrollBar(t2box5, 'Temperature', 0, 50)
setting_5.placeWidget(0.1, 0.4, 0.8, 0.5) 

setting_6 = SettingScrollBar(t2box6, 'Temperature', 0, 27)
setting_6.placeWidget(0.1, 0.4, 0.8, 0.5) 




    
left2.pack(side="left", expand=True, fill="both")
right2.pack(side="left", expand=True, fill="both")
bottom2.pack(side = "bottom", expand = True, fill = "both", anchor = S)
t2box1.pack(expand=True, fill="both", padx=10, pady=10)
t2box2.pack(expand=True, fill="both", padx=10, pady=10)
t2box3.pack(expand=True, fill = "both", padx = 10, pady = 10) 
t2box4.pack(expand = True, fill = "both", padx = 10, pady = 10)
t2box5.pack(expand = True, fill = "both", padx = 10, pady = 10) 
t2box6.pack(expand = True, fill = "both", padx = 10, pady = 10)

t2Label1.pack()
t2Label2.pack()
t2Label3.pack()
t2Label4.pack()
t2Label5.pack()
t2Label6.pack()



def callback():
    print ("First Value: ")
    print (setting_1.get())
    print ("Second Value: ")
    print (setting_2.get())
    print ("Third Value: ")
    print (setting_3.get())
    print ("Fourth Value: ")
    print (setting_4.get()) 
    print ("Fifth Value: ") 
    print (setting_5.get()) 
    print ("Sixth Value: ")
    print (setting_6.get()) 

Button1 = Button(bottom2, text = "Submit", command = callback) 
Button1.pack(expand = True, fill = "x", padx = 10, pady = 10, side = BOTTOM)


tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='Screen 3')
class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=tkinter.NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.config(state=tkinter.DISABLED)
        
class CoreGUI(object):
    def __init__(self, parent):
        text_box = tkinter.Text(parent, state=tkinter.DISABLED, yscrollcommand = scrollbar.set)
        sys.stdout = StdRedirector(text_box)
        sys.stderr = StdRedirector(text_box)
        text_box.pack(expand = True, fill = "both")
       
     

    def main(self):
        print ("Std Output")
        raise ValueError("Std Error")       


val1 = StringVar()
val2 = StringVar()
val3 = StringVar()
val4 = StringVar()
val5 = StringVar()
val6 = StringVar()
val7 = StringVar()
val8 = StringVar()

def clock():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    #lab['text'] = time
    val1.set(time)
    val2.set(time)
    val3.set(time)
    val4.set(time)
    val5.set(time)
    val6.set(time)
    val7.set(time)
    val8.set(time)
    
    xList.pop(0)
    xList.append(random.randint(0,100))
    yList.pop(0)
    yList.append(random.randint(0,50))
    newPlot.clear()
    newPlot.plot(xList,yList)
    newCanvas.draw()
    tab3.after(200, clock) # run itself again after 1000 ms
    


left3 = Frame(tab3, borderwidth=2, relief="solid")
right3 = Frame(tab3, borderwidth=2, relief="solid")
scrollbar = Scrollbar(right3)
scrollbar.pack(side = RIGHT, fill = "y")
t3box1 = Frame(left3, borderwidth=2, relief="solid")
t3box2 = Frame(left3, borderwidth=2, relief="solid")
#box3 = Frame(right, borderwidth=2, relief="solid")

t3box4 = Frame(t3box1, borderwidth=2, relief="solid")
t3box5 = Frame(t3box1, borderwidth=2, relief="solid")
t3box6 = Frame(t3box1, borderwidth=2, relief="solid")
t3box7 = Frame(t3box1, borderwidth=2, relief="solid")

t3box8 = Frame(t3box2, borderwidth=2, relief="solid")
t3box9 = Frame(t3box2, borderwidth=2, relief="solid")
t3box10 = Frame(t3box2, borderwidth=2, relief="solid")
t3box11 = Frame(t3box2, borderwidth=2, relief="solid")


t3label4 = Label(t3box4, text=" Value 1")
t3label4.config(font = ("Verdana", 7))
t3label4_1 = Label(t3box4, textvariable = val1)
t3label4_1.config(font = ("Verdana", 7))
t3label5 = Label(t3box5, text="Value 2")
t3label5.config(font = ("Verdana", 7))
t3label5_1 = Label(t3box5, textvariable = val2)
t3label5_1.config(font = ("Verdana", 7))
t3label6 = Label(t3box6, text="Value 3")
t3label6.config(font = ("Verdana", 7))
t3label6_1 = Label(t3box6, textvariable = val3)
t3label6_1.config(font = ("Verdana", 7))
t3label7 = Label(t3box7, text="Value 4")
t3label7.config(font = ("Verdana", 7))
t3label7_1 = Label(t3box7, textvariable = val4)
t3label7_1.config(font = ("Verdana", 7))
t3label8 = Label(t3box8, text="Value 5")
t3label8.config(font = ("Verdana", 7))
t3label8_1 = Label(t3box8, textvariable = val5)
t3label8_1.config(font = ("Verdana", 7))
t3label9 = Label(t3box9, text="Value 6")
t3label9.config(font = ("Verdana", 7))
t3label9_1 = Label(t3box9, textvariable = val6)
t3label9_1.config(font = ("Verdana", 7))
t3label10 = Label(t3box10, text="Value 7")
t3label10.config(font = ("Verdana", 7))
t3label10_1 = Label(t3box10, textvariable = val7)
t3label10_1.config(font = ("Verdana", 7))
t3label11 = Label(t3box11, text="Value 8")
t3label11.config(font = ("Verdana", 7))
t3label11_1 = Label(t3box11, textvariable = val8)
t3label11_1.config(font = ("Verdana", 7))
        
left3.pack(side="left", expand=True, fill="both")
right3.pack(side="right", expand=True, fill="both")
t3box1.pack(expand=True, fill="both", padx=10, pady=10)
t3box2.pack(expand=True, fill="both", padx=10, pady=10)
#box3.pack(expand=True, fill = "both", padx = 5, pady = 10) 

t3box4.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
t3box5.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
t3box6.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
t3box7.pack(side="left", expand=True, fill ="both", padx=5, pady=5)

t3box8.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
t3box9.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
t3box10.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
t3box11.pack(side="left", expand=True, fill ="both", padx=5, pady=5)

t3label4.pack()
t3label5.pack()
t3label6.pack()
t3label7.pack()
t3label8.pack()
t3label9.pack()
t3label10.pack()
t3label11.pack()
t3label4_1.pack()
t3label5_1.pack()
t3label6_1.pack()
t3label7_1.pack()
t3label8_1.pack()
t3label9_1.pack()
t3label10_1.pack()
t3label11_1.pack()


tabControl.pack(expand=1, fill='both')



CoreGUI(right3)
print("Updating Values...")


clock()

window.mainloop()
