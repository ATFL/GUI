import tkinter
import sys


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
        text_box = tkinter.Text(parent, state=tkinter.DISABLED)
        sys.stdout = StdRedirector(text_box)
        sys.stderr = StdRedirector(text_box)
        text_box.pack()

        output_button = tkinter.Button(parent, text="Output", command=self.main)
        output_button.pack()

    def main(self):
        print ("Std Output")
        raise ValueError("Std Error")

root = tkinter.Tk()
CoreGUI(root)
root.mainloop()
