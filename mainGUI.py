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
        self.my_observer= Observer()
        self.event_handler = Handler()
        
        

    def button_browse(self):
        filename= filedialog.askdirectory()
        self.folder_path=filename
        self.lbl1["text"]= self.folder_path
        print(self.folder_path)

    def run(self):
        
        print("run executed")
        
        #print(path)
        if (os.path.isdir(self.folder_path)):
            path= self.folder_path+"/"
            self.my_observer.start()
            self.my_observer.schedule(self.event_handler, path, recursive = True)
            try:
                while True:
                    print("Observer Running")
                    time.sleep(3)
            except:
                self.my_observer.stop()
                print("Observer Stopped")
    
            self.my_observer.join()
        else:
            messagebox.showinfo(message="Select a folder", title="folder empty")

    def button_stop(self):
        if(self.my_observer.is_alive()):
            self.my_observer.stop()
            self.my_observer.join()
        else:
            messagebox.showinfo(message="program nor running", title="stop")

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf", ".docx"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        watchdog.events.PatternMatchingEventHandler.__init__(self,patterns, ignore_patterns, ignore_directories, case_sensitive)
    #Obs class
    def on_created(self, event):
        os.startfile(event.src_path, "print")
    #Obs class

if __name__ == "__main__":
    app= MyObserver()
    app.mainloop()