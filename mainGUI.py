import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
import watchdog.events

class MyObserver(tk.Tk):
    
    def __init__(self):
        super().__init__()
        #Var
        self.folder_path="Not selected"

        #Layout
        self.title("Automatic print")
        self.geometry('450x450')
        self.config(bg="skyblue")

        self.lbl1= ttk.Label(self, text=self.folder_path)
        self.lbl1.grid(row=1, column=0, padx=5, pady=5)

        self.button_browse= ttk.Button(self, text="Browse", command=self.button_browse)
        self.button_browse.grid(row=2, column=0, padx=5, pady=5)

        self.button_run= ttk.Button(self, text="Run", command=self.run)
        self.button_run.grid(row=4, column=2, padx=5, pady=5)

        self.button_stop= ttk.Button(self, text="Stop", command=self.button_stop)
        self.button_stop.grid(row=4, column=4, padx=5, pady=5)

        #Obs
        #self.my_observer= Observer()
        self.event_handler = Handler()
        self.executed= False
        
        

    def button_browse(self):
        filename= filedialog.askdirectory()
        self.folder_path=filename
        self.lbl1["text"]= self.folder_path
        print(self.folder_path)

    def run(self):
        #print("run executed")
        if(self.executed):
            messagebox.showinfo(message="Program already running", title="Running")

        elif(os.path.isdir(self.folder_path)):
            self.executed= True
            path= self.folder_path+"/"
            
            global my_observer
            my_observer= Observer()
            my_observer.start()
            my_observer.schedule(self.event_handler, path, recursive = True)
            time.sleep(3)
           
        else:
            messagebox.showinfo(message="Select a folder", title="Empty folder")

    def button_stop(self):
        if(self.executed):
            global my_observer
            my_observer.stop()
            my_observer.join()
            self.executed= False
        else:
            messagebox.showinfo(message="Program is not running", title="Stop")

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf", ".docx"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        watchdog.events.PatternMatchingEventHandler.__init__(self,patterns, ignore_patterns, ignore_directories, case_sensitive)
    
    def on_created(self, event):
        os.startfile(event.src_path, "print")
    

if __name__ == "__main__":
    app= MyObserver()
    app.mainloop()