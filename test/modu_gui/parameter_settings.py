from tkinter import *

def parameter_settings(tab):
    left = Frame(tab, borderwidth=2, relief="solid")
    right = Frame(tab, borderwidth=2, relief="solid")
    box1 = Frame(left, borderwidth=2, relief="solid")
    box2 = Frame(left, borderwidth=2, relief="solid")
    box3 = Frame(left, borderwidth=2, relief = "solid")
    box4 = Frame(right, borderwidth=2, relief = "solid")
    box5 = Frame(right, borderwidth=2, relief = "solid")
    box6 = Frame(right, borderwidth=2, relief = "solid")


    Label1 = Label(box1, text="First Value")
    e1 = Entry(box1)

    Label2 = Label(box2, text="Second Value")
    e2 = Entry(box2)

    Label3 = Label(box3, text="Third Value")
    e3 = Entry(box3)

    Label4 = Label(box4, text="Fourth Value")
    e4 = Entry(box4)

    Label5 = Label(box5, text="Fifth Value")
    e5 = Entry(box5)

    Label6= Label(box6, text="Sixth Value")
    e6 = Entry(box6)


    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    box1.pack(expand=True, fill="both", padx=10, pady=10)
    box2.pack(expand=True, fill="both", padx=10, pady=10)
    box3.pack(expand=True, fill = "both", padx = 10, pady = 10)
    box4.pack(expand = True, fill = "both", padx = 10, pady = 10)
    box5.pack(expand = True, fill = "both", padx = 10, pady = 10)
    box6.pack(expand = True, fill = "both", padx = 10, pady = 10)

    Label1.pack()
    Label2.pack()
    Label3.pack()
    Label4.pack()
    Label5.pack()
    Label6.pack()
    e1.pack()
    e2.pack()
    e3.pack()
    e4.pack()
    e5.pack()
    e6.pack()


    def callback():
        print ("First Value: ",e1.get())
        print ("Second Value: ",e2.get())
        print ("Third Value: ",e3.get())
        print ("Fourth Value: ",e4.get())
        print ("Fifth Value: ",e5.get())
        print ("Sixth Value: ",e6.get())


    Button1 = Button(tab, text = "Submit", command = callback)
    Button1.pack(expand = True, fill = "both", padx = 10, pady = 10, side = BOTTOM)
