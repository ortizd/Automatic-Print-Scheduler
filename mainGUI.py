import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import os
from watchdog.observers import Observer
import watchdog.events
from Handler import Handler

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
        self.event_handler = Handler()
        self.executed= False
        
        

    def button_browse(self):
        self.folder_path= filedialog.askdirectory()
        self.lbl1["text"]= self.folder_path


    def run(self):
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


    

if __name__ == "__main__":
    app= MyObserver()
    app.mainloop()