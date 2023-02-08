import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import os
from watchdog.observers import Observer
import watchdog.events
from Handler import Handler
import json

class MyObserver(tk.Tk):
    
    def __init__(self):
        super().__init__()

        
        try:
            with open("permanent_file.json", "r") as file:
                self.folder_path = json.load(file)
        except:
            self.folder_path="Not selected"
        # Program state variable
        self.state= "Program not running"

        #Obs and Handler
        self.event_handler = Handler()
        self.executed= False

        #Frame
        self.title("Automatic printing")
        self.config(bg="skyblue")

        self.lbl1= ttk.Label(self, text=self.folder_path)
        self.lbl1.grid(row=1, column=0, padx=5, pady=5)

        self.state= ttk.Label(self, text=self.state)
        self.state.grid(row=4, column=2, padx=5, pady=5)

        self.button_browse= ttk.Button(self, text="Browse", command=self.button_browse)
        self.button_browse.grid(row=2, column=0, padx=5, pady=5)

        self.button_run= ttk.Button(self, text="Run", command=self.run)
        self.button_run.grid(row=5, column=2, padx=5, pady=5)

        self.button_stop= ttk.Button(self, text="Stop", command=self.button_stop)
        self.button_stop.grid(row=5, column=3, padx=5, pady=5)

        

        self.files_accepted= ttk.Label(self, text="Files accepted to be printed: "+''.join(self.event_handler.patterns))
        self.files_accepted.grid(row=3, column=0, padx=5, pady=5)
        
        
        

    def button_browse(self):
        self.folder_path= filedialog.askdirectory()
        with open("permanent_file.json", "w") as file:
            json.dump(self.folder_path, file)
        self.lbl1["text"]= self.folder_path


    def run(self):
        if(self.executed):
            messagebox.showinfo(message="Program already running", title="Running")

        elif(os.path.isdir(self.folder_path)):
            self.executed= True
            self.state["text"]= "Program running"
            path= self.folder_path#+"/"
            
            global my_observer
            my_observer= Observer()
            my_observer.start()
            my_observer.schedule(self.event_handler, path, recursive = False)
            #time.sleep(1)

        else:
            messagebox.showinfo(message="Select a folder", title="Empty folder")

    def button_stop(self):
        if(self.executed):
            global my_observer
            my_observer.stop()
            my_observer.join()
            self.executed= False
            self.state["text"]= "Program not running"
        else:
            messagebox.showinfo(message="Program is not running", title="Stop")


    

if __name__ == "__main__":
    app= MyObserver()
    app.mainloop()