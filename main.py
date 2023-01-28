""" 
This is the basic design, I need to improve it.
the path is retrieved in the global variable folder_path
The process is in the file Observer.py
"""

from tkinter import *
from tkinter import filedialog



root= Tk()
root.title("Automatic print")
root.geometry('450x450')
root.config(bg="skyblue")


def browse_button():
    global folder_path
    filename= filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

my_frame= Frame(root, width=200, height=200)
my_frame.grid(row=0, column=0, padx=10, pady=5)
my_frame.config(bg="red")

folder_path= StringVar()

lbl1= Label(my_frame, textvariable=folder_path)
lbl1.grid(row=1, column=0, padx=5, pady=5)

button2= Button(my_frame, text="Browse", command=browse_button)
button2.grid(row=2, column=0, padx=5, pady=5)

root.mainloop()