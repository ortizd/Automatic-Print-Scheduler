""" 
This is the basic design, I need to improve it.
the path is retrieved in the global variable folder_path
The process is in the file Observer.py
"""
#Obs class
import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
#Obs class

from tkinter import *
from tkinter import filedialog

root= Tk()
root.title("Automatic print")
root.geometry('450x450')
root.config(bg="skyblue")

folder_path= StringVar()

#Obs class
if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
#Obs class

def button_browse():
    global folder_path
    filename= filedialog.askdirectory()
    folder_path.set(filename)
    

def button_run():
    if (len(folder_path.get())>0):
        print(folder_path.get())
        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

my_frame= Frame(root, width=200, height=200)
my_frame.grid(row=0, column=0, padx=10, pady=5)
my_frame.config(bg="red")

lbl1= Label(my_frame, textvariable=folder_path)
lbl1.grid(row=1, column=0, padx=5, pady=5)

button_browse= Button(my_frame, text="Browse", command=button_browse)
button_browse.grid(row=2, column=0, padx=5, pady=5)


button_run= Button(my_frame, text="Run", command=button_run)
button_run.grid(row=4, column=2, padx=5, pady=5)


#Obs class
# In this function I should send to print, it is necessary to recover the name of the created file since event.src_path brings the full path 
def on_created(event):
     #print(f"hey, {event.src_path} has been created!")
     os.startfile(event.src_path, "print")


my_event_handler.on_created = on_created

go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path= folder_path.get()+"/", recursive=go_recursively)




#Obs class


root.mainloop()