from tkinter import *
import datetime
import os
import tkinter
from tkinter import ttk

w, h = 640, 480 #Window Size
window = Tk()
window.title("ATFL - Metro Vancouver") #Include the name of the window
canvas = Canvas(window)
canvas.pack(expand = True, fill ='both')

"""create the tabs, the windows and the names"""


tabControl = ttk.Notebook(canvas)

tab1 = ttk.Frame(tabControl) #making a frame
tabControl.add(tab1, text='Screen 1') #properties of the Frame


left = Frame(tab1, borderwidth=2, relief="solid")
right = Frame(tab1, borderwidth=2, relief="solid")
box1 = Frame(left, borderwidth=2, relief="solid")

def purge1Callback():
    print ("This will be replaced with the required purge 1 actions")
    
def purge2Callback():
    print("This will be replaced with the required purge 2 actions")

def runCallback():
    print("This will be replaced with the required run actions")
    
def stopCallback():
    print("This will be replaced with the required stop actions")
    
box2 = Button(right, text = "Purge 1", command = purge1Callback)
box3 = Button(right, text = "Purge 2", command = purge2Callback)
box4 = Button(right, text = "Run", command = runCallback)
box5 = Button(right, text = "Stop", command = stopCallback)

label1 = Canvas(box1)


left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
box1.pack(expand=True, fill="both", padx=10, pady=10)
label1.pack()
box2.pack(expand = True, fill = "both", padx =10, pady= 10)
box3.pack(expand = True, fill = "both", padx = 10, pady = 10)
box4.pack(expand = True, fill = "both", padx = 10, pady = 10)
box5.pack(expand = True, fill = "both", padx = 10, pady = 10)


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
t2e1 = Entry(t2box1)

t2Label2 = Label(t2box2, text="Second Value")
t2e2 = Entry(t2box2)

t2Label3 = Label(t2box3, text="Third Value")
t2e3 = Entry(t2box3) 

t2Label4 = Label(t2box4, text="Fourth Value")
t2e4 = Entry(t2box4)

t2Label5 = Label(t2box5, text="Fifth Value")
t2e5 = Entry(t2box5)

t2Label6= Label(t2box6, text="Sixth Value")
t2e6 = Entry(t2box6)

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
t2e1.pack()
t2e2.pack()
t2e3.pack()
t2e4.pack()
t2e5.pack()
t2e6.pack()


def callback():
    print ("First Value: ")
    print (t2e1.get())
    print ("Second Value: ")
    print (t2e2.get())
    print ("Third Value: ")
    print (t2e3.get())
    print ("Fourth Value: ")
    print (t2e4.get()) 
    print ("Fifth Value: ") 
    print (t2e5.get()) 
    print ("Sixth Value: ")
    print (t2e6.get()) 

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
    time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    #lab['text'] = time
    val1.set(time)
    val2.set(time)
    val3.set(time)
    val4.set(time)
    val5.set(time)
    val6.set(time)
    val7.set(time)
    val8.set(time)
    print(time)
    
    tab3.after(500, clock) # run itself again after 1000 ms
    


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


t3label4 = Label(t3box4, text="First Value")
t3label4.config(font = ("Verdana", 11))
t3label4_1 = Label(t3box4, textvariable = val1)
t3label4_1.config(font = ("Verdana", 11))
t3label5 = Label(t3box5, text="Second Value")
t3label5.config(font = ("Verdana", 11))
t3label5_1 = Label(t3box5, textvariable = val2)
t3label5_1.config(font = ("Verdana", 11))
t3label6 = Label(t3box6, text="Third Value")
t3label6.config(font = ("Verdana", 11))
t3label6_1 = Label(t3box6, textvariable = val3)
t3label6_1.config(font = ("Verdana", 11))
t3label7 = Label(t3box7, text="Fourth Value")
t3label7.config(font = ("Verdana", 11))
t3label7_1 = Label(t3box7, textvariable = val4)
t3label7_1.config(font = ("Verdana", 11))
t3label8 = Label(t3box8, text="Fifth Value")
t3label8.config(font = ("Verdana", 11))
t3label8_1 = Label(t3box8, textvariable = val5)
t3label8_1.config(font = ("Verdana", 11))
t3label9 = Label(t3box9, text="Sixth Value")
t3label9.config(font = ("Verdana", 11))
t3label9_1 = Label(t3box9, textvariable = val6)
t3label9_1.config(font = ("Verdana", 11))
t3label10 = Label(t3box10, text="Seventh Value")
t3label10.config(font = ("Verdana", 11))
t3label10_1 = Label(t3box10, textvariable = val7)
t3label10_1.config(font = ("Verdana", 11))
t3label11 = Label(t3box11, text="Eigth Value")
t3label11.config(font = ("Verdana", 11))
t3label11_1 = Label(t3box11, textvariable = val8)
t3label11_1.config(font = ("Verdana", 11))
        
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
