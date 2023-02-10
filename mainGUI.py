import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time, os, json
from watchdog.observers import Observer
import watchdog.events
from Handler import Handler

class MyObserver(tk.Tk):
    def __init__(self):
        super().__init__()

        # Program state variable
        self.state= "Program not running"
        self.var_check= tk.IntVar()
        
        try:
            with open("permanent_file.json", "r") as file:
                self.json_dict= json.load(file)
                self.folder_path = self.json_dict["path"]
                self.var_check.set(int(self.json_dict["subFolder"]))
               
        except:
            self.folder_path="Not selected"
            self.sub_folder=False
            with open("permanent_file.json", "w") as file:
                json.dump({"path":self.folder_path, "subFolder":0}, file)
        

        #Obs and Handler
        self.event_handler = Handler()
        self.executed= False
        
            
        
        #Frame
        self.title("Automatic printing")
        self.config(bg="skyblue", bd=5, relief="groove")

        self.lbl1= ttk.Label(self, text=self.folder_path)
        self.lbl1.grid(row=1, column=0, padx=5, pady=5)

        self.state= ttk.Label(self, text=self.state)
        self.state.grid(row=4, column=2, padx=5, pady=5)

        self.button_browse= ttk.Button(self, text="Browse", command=self.browse)
        self.button_browse.grid(row=2, column=0, padx=0, pady=5)

        self.button_run= ttk.Button(self, text="Run", command=self.run)
        self.button_run.grid(row=5, column=2, padx=5, pady=5)

        self.button_stop= ttk.Button(self, text="Stop", command=self.button_stop)
        self.button_stop.grid(row=5, column=3, padx=5, pady=5)

        

        self.files_accepted= ttk.Label(self, text="Files accepted to be printed: "+''.join(self.event_handler.patterns))
        self.files_accepted.grid(row=3, column=0, padx=5, pady=5)

                
        self.check_subFolders= ttk.Checkbutton(self, text="Include subfolders" ,variable=self.var_check, onvalue=1, offvalue=0, command=self.subFolders)
        self.check_subFolders.grid(row=5, column=1, padx=1, pady=1)
        # self.check_subFolders.bind("<Button-1>", self.checkButton_click)
        

    # def subFolders(self):
    #     if self.var_check.get()==1:
    #         with open("permanent_file.json", "w") as file:
    #             json.dump({"path":self.folder_path, "subFolder":1}, file)
    #     else:
    #         with open("permanent_file.json", "w") as file:
    #             json.dump({"path":self.folder_path, "subFolder":0}, file)

    def subFolders(self):
        if(self.executed):
            messagebox.showinfo(message="Stop the program first", title="Running")
            with open("permanent_file.json", "r") as file:
                self.json_dict= json.load(file)
                self.var_check.set(int(self.json_dict["subFolder"]))
        else:
        
            if (self.var_check.get()==1):
                with open("permanent_file.json", "r") as file:
                    data= json.load(file)
                data["subFolder"]=1
                with open("permanent_file.json", "w") as file:
                    json.dump(data, file, indent=4)
            else:
                with open("permanent_file.json", "r") as file:
                    data= json.load(file)
                data["subFolder"]=0
                with open("permanent_file.json", "w") as file:
                    json.dump(data, file, indent=4)

    # def checkButton_click(self, event):
    #         if(self.executed):
    #             messagebox.showinfo(message="Stop the program first", title="Running")
    #         else:
                
    #             self.subFolders()




    def browse(self):
        if (self.executed):
            messagebox.showinfo(message="stop the program first", title="Running")
        else:
            self.folder_path= filedialog.askdirectory()
            with open("permanent_file.json", "r") as file:
                data= json.load(file)
                data["path"]= self.folder_path
            with open("permanent_file.json", "w") as file:
                json.dump(data, file, indent=4)
            self.lbl1["text"]= self.folder_path


    def run(self):
        if(self.executed):
            messagebox.showinfo(message="Program already running", title="Running")

        elif(os.path.isdir(self.folder_path)):
            self.executed= True
            self.state["text"]= "Program running"
            path= self.folder_path
            global my_observer
            my_observer= Observer()
            my_observer.start()
            if self.var_check.get()==1:
                self.sub_folder=True
            else:
                self.sub_folder=False
            my_observer.schedule(self.event_handler, path, recursive = self.sub_folder)

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
            msg_box= messagebox.askquestion("Program not running", "Program not running, do you want to start it?")
            if msg_box== "yes":
                self.run()
    

if __name__ == "__main__":
    app= MyObserver()
    app.mainloop()