from tkinter import *

root = Tk()
root.geometry("640x480")
root.title("ATFL - Metro Vancouver")

left = Frame(root, borderwidth=2, relief="solid")
right = Frame(root, borderwidth=2, relief="solid")
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



root.mainloop()

