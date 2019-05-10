from tkinter import *
import datetime
import os
import tkinter
from tkinter import ttk


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

root = Tk()

root.geometry("640x480")
root.title("ATFL - Metro Vancouver") 
 

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
    
    root.after(500, clock) # run itself again after 1000 ms
    

# run first time



left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
scrollbar = Scrollbar(right)
scrollbar.pack(side = RIGHT, fill = "y")
box1 = Frame(left, borderwidth=2, relief="solid")
box2 = Frame(left, borderwidth=2, relief="solid")
#box3 = Frame(right, borderwidth=2, relief="solid")

box4 = Frame(box1, borderwidth=2, relief="solid")
box5 = Frame(box1, borderwidth=2, relief="solid")
box6 = Frame(box1, borderwidth=2, relief="solid")
box7 = Frame(box1, borderwidth=2, relief="solid")

box8 = Frame(box2, borderwidth=2, relief="solid")
box9 = Frame(box2, borderwidth=2, relief="solid")
box10 = Frame(box2, borderwidth=2, relief="solid")
box11 = Frame(box2, borderwidth=2, relief="solid")


label4 = Label(box4, text="First Value")
label4.config(font = ("Verdana", 11))
label4_1 = Label(box4, textvariable = val1)
label4_1.config(font = ("Verdana", 11))
label5 = Label(box5, text="Second Value")
label5.config(font = ("Verdana", 11))
label5_1 = Label(box5, textvariable = val2)
label5_1.config(font = ("Verdana", 11))
label6 = Label(box6, text="Third Value")
label6.config(font = ("Verdana", 11))
label6_1 = Label(box6, textvariable = val3)
label6_1.config(font = ("Verdana", 11))
label7 = Label(box7, text="Fourth Value")
label7.config(font = ("Verdana", 11))
label7_1 = Label(box7, textvariable = val4)
label7_1.config(font = ("Verdana", 11))
label8 = Label(box8, text="Fifth Value")
label8.config(font = ("Verdana", 11))
label8_1 = Label(box8, textvariable = val5)
label8_1.config(font = ("Verdana", 11))
label9 = Label(box9, text="Sixth Value")
label9.config(font = ("Verdana", 11))
label9_1 = Label(box9, textvariable = val6)
label9_1.config(font = ("Verdana", 11))
label10 = Label(box10, text="Seventh Value")
label10.config(font = ("Verdana", 11))
label10_1 = Label(box10, textvariable = val7)
label10_1.config(font = ("Verdana", 11))
label11 = Label(box11, text="Eigth Value")
label11.config(font = ("Verdana", 11))
label11_1 = Label(box11, textvariable = val8)
label11_1.config(font = ("Verdana", 11))
        
left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
box1.pack(expand=True, fill="both", padx=10, pady=10)
box2.pack(expand=True, fill="both", padx=10, pady=10)
#box3.pack(expand=True, fill = "both", padx = 5, pady = 10) 

box4.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
box5.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
box6.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
box7.pack(side="left", expand=True, fill ="both", padx=5, pady=5)

box8.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
box9.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
box10.pack(side="left", expand=True, fill ="both", padx=5, pady=5)
box11.pack(side="left", expand=True, fill ="both", padx=5, pady=5)

label4.pack()
label5.pack()
label6.pack()
label7.pack()
label8.pack()
label9.pack()
label10.pack()
label11.pack()
label4_1.pack()
label5_1.pack()
label6_1.pack()
label7_1.pack()
label8_1.pack()
label9_1.pack()
label10_1.pack()
label11_1.pack()

CoreGUI(right)
print("Updating Values...")

clock()


root.mainloop()