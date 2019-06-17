from tkinter import *

root = Tk()
root.geometry("640x480")
root.title("ATFL - Metro Vancouver")

left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
bottom = Frame(root, borderwidth=2, relief = "solid")
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
right.pack(side="left", expand=True, fill="both")
bottom.pack(side = "bottom", expand = True, fill = "both", anchor = S)
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
    print ("First Value: ")
    print (e1.get())
    print ("Second Value: ")
    print (e2.get())
    print ("Third Value: ")
    print (e3.get())
    print ("Fourth Value: ")
    print (e4.get()) 
    print ("Fifth Value: ") 
    print (e5.get()) 
    print ("Sixth Value: ")
    print (e6.get()) 

Button1 = Button(bottom, text = "Submit", command = callback) 
Button1.pack(expand = True, fill = "x", padx = 10, pady = 10, side = BOTTOM)




mainloop( )