""" 
This is the basic development, I need to design the interface.

When I click on the "Run button" the program should be
minimized to the taskbar. The "Stop button" needs to be developed.

"""
#Obs class
import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
#Obs class

from tkinter import *
from tkinter import filedialog

root= Tk()
root.title("Automatic print")
root.geometry('450x450')
root.config(bg="skyblue")
folder_path= StringVar()




class OnMyWatch():
    global folder_path
    def __init__(self):
        patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf", ".docx"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self.observer= Observer()
    
    def run(self):
        print("run executed")
        event_handler = Handler()
        self.observer.schedule(event_handler, self.folder_path.get()+"/", recursive = True)
        self.observer.start()
        print(folder_path)
        if (len(folder_path.get())>0):
            try:
                while True:
                    time.sleep(5)
            except:
                self.observer.stop()
                print("Observer Stopped")
    
            self.observer.join()


    def button_browse():
        global folder_path
        filename= filedialog.askdirectory()
        folder_path.set(filename)

    
    def button_stop():
        self.observer.stop()
        self.observer.join()

    # Layout
   

    my_frame= Frame(root, width=200, height=200)
    my_frame.grid(row=0, column=0, padx=10, pady=5)
    my_frame.config(bg="red")

    lbl1= Label(my_frame, textvariable=folder_path)
    lbl1.grid(row=1, column=0, padx=5, pady=5)

    button_browse= Button(my_frame, text="Browse", command=button_browse)
    button_browse.grid(row=2, column=0, padx=5, pady=5)


    button_run= Button(my_frame, text="Run", command=run)
    button_run.grid(row=4, column=2, padx=5, pady=5)


    button_stop= Button(my_frame, text="Stop", command=button_stop)
    button_stop.grid(row=4, column=4, padx=5, pady=5)
    # Layout

        
    """
    def button_run():
        if (len(folder_path.get())>0):
            
            my_observer.start()
            try:
                while True:
                    time.sleep(3)
            except KeyboardInterrupt:
                my_observer.stop()
            my_observer.join()
    """
        
class Handler(FileSystemEventHandler):
    #Obs class
    def on_created(event):
        os.startfile(event.src_path, "print")
    #Obs class




#Obs class
"""
if __name__ == "__main__":
    #myWatch= OnMyWatch()
    

    patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf", ".docx"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    #myWatch= OnMyWatch()
    #myWatch.run()
"""
   
    
        
#Obs class




root.mainloop()