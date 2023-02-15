import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time, os, json
from watchdog.observers import Observer
import watchdog.events
from Handler import Handler
from EditExtension import EditExtension
from JSONReader import JsonReader



class MyObserver(tk.Tk):
    
    def __init__(self):
        super().__init__()

        # Program state variable
        self.state= "Program not started"
        self.var_check= tk.IntVar() # Used in check_subFolders checkbox
        self.my_json_reader= JsonReader() # JsonReader instance to read or write
        self.executed= False # Check if the program is running or not

        # Read the JsonFile and set the variables
        try:
            self.data= self.my_json_reader.read_json()
            self.folder_path = self.data["path"]
            self.var_check.set(int(self.data["subFolder"]))
            self.extension_accepted= [extension["extension"] for extension in self.data["extensions"] if extension["allowed"]==1]
        # Set variables by default and create the JsonFile in case it does not exist       
        except:
            self.folder_path="Not selected"
            self.sub_folder=False
            self.extensions= [
        {
            "extension": "*.doc",
            "allowed": 1
        },
        {
            "extension": "*.docx",
            "allowed": 1
        },
        {
            "extension": "*.pdf",
            "allowed": 1
        },
        {
            "extension": "*.txt",
            "allowed": 1
        },
        {
            "extension": "*.rtf",
            "allowed": 0
        },
        {
            "extension": "*.odt",
            "allowed": 0
        },
	    {
            "extension": "*.jpeg",
            "allowed": 1
        },
        {
            "extension": "*.jpg",
            "allowed": 1
        },
        {
            "extension": "*.png",
            "allowed": 1
        },
	    {
            "extension": "*.gif",
            "allowed": 0
        },
	    {
            "extension": "*.bmp",
            "allowed": 1
        },
        {
            "extension": "*.tiff",
            "allowed": 0
        },
        {
            "extension": "*.ppt",
            "allowed": 1
        },
        {
            "extension": "*.pptx",
            "allowed": 1
        }   
    ]
            # Get the extensions allowed to update the label "files_accepted" and create the JSON File by default    
            self.extension_accepted = [extension["extension"] for extension in self.extensions if extension["allowed"] == 1]
            with open("permanent_file.json", "w") as file:
                json.dump({"path":self.folder_path, "subFolder":0, "extensions":self.extensions}, file, indent=4)
        
        
        
        # Define a color palette
        BLUE = "#1E3A8A"
        DARK_BLUE = "#13244F"
        LIGHT_BLUE = "#86BBD8"
        WHITE = "#FFFFFF"
        GRAY = "#9B9B9B"
        GREEN = "#78BE20"
        RED = "#D42D2D"
        DARK_RED = '#A8321F'
        LIGHT_RED = '#F6BBAF'
        DARK_GREEN = '#387A07'
        LIGHT_GREEN = '#B2D8A7'
        
        # Define a custom style for buttons
        style = ttk.Style()
        style.configure("Blue.TButton", foreground=GRAY, bordercolor=BLUE, lightcolor=BLUE, darkcolor=DARK_BLUE, padding=5, relief="flat")
        style.configure("Red.TButton", foreground=GRAY, bordercolor=RED, lightcolor=RED, darkcolor=DARK_RED, padding=5, relief="flat")
        style.configure("Green.TButton", foreground=GRAY, bordercolor=GREEN, lightcolor=GREEN, darkcolor=DARK_GREEN, padding=5, relief="flat")
        style.configure("Blue.TCheckbutton", foreground=GRAY, background=DARK_BLUE, focuscolor=LIGHT_BLUE, bordercolor=BLUE, indicatorcolor=BLUE)


        # Create the main window and set its properties
        self.title("Automatic printing")
        self.config(bg=BLUE, bd=5, relief="groove")
        self.resizable(False, False)
        self.iconbitmap("printer.ico")
        # Automatic printing title
        self.label_title = ttk.Label(self, text="Printer Scheduler", font=("Helvetica", 16))
        self.label_title.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")
        # Progressbar
        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.grid(row=6, column=1, padx=5, pady=5)
        # Shows the path where the process will run
        self.label_path= ttk.Label(self, text=self.folder_path, foreground=WHITE, background=DARK_BLUE)
        self.label_path.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        # Shows if the program is running
        self.state= ttk.Label(self, text=self.state, foreground=WHITE, background= DARK_BLUE, padding=5)
        self.state.grid(row=6, column=2, padx=5, pady=5, sticky="e")
        # Browse Button
        self.button_browse= ttk.Button(self, text="Browse", command=self.browse, style="Blue.TButton")
        self.button_browse.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        # Run Button
        self.button_run= ttk.Button(self, text="Start", style="Green.TButton",command=self.run)
        self.button_run.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        # Stop Button
        self.button_stop= ttk.Button(self, text="Stop", style="Red.TButton",command=self.button_stop)
        self.button_stop.grid(row=5, column=2, padx=5, pady=5, sticky="e")
        # Files allowed to be printed
        self.files_accepted= ttk.Label(self, text="Files accepted to be printed: "+' '.join(self.extension_accepted), foreground=WHITE, background=DARK_BLUE)
        self.files_accepted.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        # Checks if include or not subfolders to be observed                
        self.check_subFolders= ttk.Checkbutton(self, text="Include subfolders" ,variable=self.var_check, onvalue=1, offvalue=0, command=self.subFolders, style="Blue.TCheckbutton")
        self.check_subFolders.grid(row=5, column=0, padx=1, pady=1, sticky="w")
        # Edit Button binded with the open_edit_extension function, necessary to retrieve the information that returns
        self.button_edit= ttk.Button(self, text="Edit", state="normal", style="Blue.TButton")
        self.button_edit.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.button_edit.bind("<Button>", self.open_edit_extension)

    # Open edit widget and retrieves how the widget was closed. Necessary to reread the JSON File and update the information in case it was updated
    # (Did not find another way to get the information updated in EditExtension.py)
    def open_edit_extension(self, event):
        edit_window = EditExtension(self.master)
        edit_window.protocol("WM_DELETE_WINDOW", lambda: self.on_edit_extension_close(edit_window, "CLOSE"))
        edit_window.on_save_and_exit = lambda: self.on_edit_extension_close(edit_window, "SAVE_AND_EXIT")


    def on_edit_extension_close(self, edit_window, close_type):
        # Check if the information was edited and update files_accepted label
        if close_type=="SAVE_AND_EXIT":
            data= self.my_json_reader.read_json()
            self.extension_accepted= [extension["extension"] for extension in data["extensions"] if extension["allowed"] == 1]
            self.files_accepted["text"]= "Files accepted to be printed: "+' '.join(self.extension_accepted)
            edit_window.destroy()
        if close_type=="CLOSE":
            edit_window.destroy()


    def subFolders(self):
        data= self.my_json_reader.read_json()
        # Check if the program is running
        if(self.executed):
            messagebox.showinfo(message="Stop the program first", title="Running")
            # I need this reading to keep the variable as it was
            self.var_check.set(int(data["subFolder"]))
        else:
            if (self.var_check.get()==1):
                data["subFolder"]=1
                self.my_json_reader.write_json(data)
            else:
                data["subFolder"]=0
                self.my_json_reader.write_json(data)

  

    def browse(self):
        if (self.executed):
            messagebox.showinfo(message="stop the program first", title="Running")
        else:
            # Browse Directory
            self.folder_path= filedialog.askdirectory()
            # Read and Update JSON File
            data=self.my_json_reader.read_json()
            data["path"]= self.folder_path
            self.my_json_reader.write_json(data)
            # Update Label
            self.label_path["text"]= self.folder_path


    def run(self):
        if(self.executed):
            messagebox.showinfo(message="Program already started", title="Running")
        # Make sure it is a directory
        elif(os.path.isdir(self.folder_path)):
            self.executed= True
            self.state["text"]= "Program started"
            # Get path
            data= self.my_json_reader.read_json()
            path= data["path"]
            # Initialize Handler and the Observer
            self.event_handler = Handler()
            global my_observer
            my_observer= Observer()
            my_observer.start()
            # Check if it includes subFolder
            if self.var_check.get()==1:
                self.sub_folder=True
            else:
                self.sub_folder=False
            # Set Observer    
            my_observer.schedule(self.event_handler, path, recursive = self.sub_folder)
            # Button disabled and Unbound from any events
            self.button_edit.configure(state="disabled")
            self.button_edit.unbind("<Button>")
            self.progressbar.start()
        else:
            messagebox.showinfo(message="Select a folder", title="Empty folder")

    def button_stop(self):
        if(self.executed):
            global my_observer
            my_observer.stop()
            my_observer.join()
            # Button Again Enabled and Bound
            self.button_edit.configure(state="normal")
            self.button_edit.bind("<Button>", self.open_edit_extension)
            self.progressbar.stop()
            self.executed= False
            self.state["text"]= "Program not started"
        else:
            msg_box= messagebox.askquestion("Program not started", "Program not started, do you want to start it?")
            if msg_box== "yes":
                self.run()
    

if __name__ == "__main__":
    app= MyObserver()
    app.mainloop()