from tkinter import *

def display_graph(tab):
    left = Frame(tab, borderwidth=2, relief="solid")
    right = Frame(tab, borderwidth=2, relief="solid")
    box1 = Frame(right, borderwidth=2, relief="solid")
    box2 = Frame(right, borderwidth=2, relief="solid")
    box3 = Frame(left, borderwidth=2, relief = "solid")
    box4 = Frame(left, borderwidth=2, relief = "solid")

    label1 = Canvas(box3)
    label2 = Canvas(box4)
    label4 = Canvas(box1)
    label5 = Canvas(box2)

    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    box1.pack(expand=True, fill="both", padx=10, pady=10)
    box2.pack(expand=True, fill="both", padx=10, pady=10)
    box3.pack(expand=True, fill = "both", padx = 10, pady = 10)
    box4.pack(expand = True, fill = "both", padx = 10, pady = 10)

    label1.pack()
    label2.pack()
    label4.pack()
    label5.pack()
