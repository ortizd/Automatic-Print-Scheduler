from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import json
from JSONReader import JsonReader
 
class EditExtension(Toplevel):

    def __init__(self, master = None):   

        super().__init__(master = master)

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
        style.configure("Blue.TButton", foreground=GRAY, bordercolor=BLUE, lightcolor=BLUE, darkcolor=DARK_BLUE, padding=3, relief="flat")
        style.configure("Blue.TCheckbutton", foreground=DARK_BLUE, background=LIGHT_BLUE, focuscolor=LIGHT_BLUE, bordercolor=BLUE, indicatorcolor=BLUE)

        self.title("Extensions")
        self.resizable(False, False)
        self.config(bg=LIGHT_BLUE, bd=5, relief="groove")
        self.iconbitmap("printer.ico")
        self.grab_set()

        # Main Label
        #label = Label(self, text ="Extensions to be printed").grid(row=0, column=0, columnspan=2 ,sticky=W+E)
        self.label_title = ttk.Label(self, text="Extensions allowed", font=("Helvetica", 12))
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")
        # Exit & Save Button
        exit_b= Button(self, text="Save & Exit", command=self.on_save_and_exit, style="Blue.TButton")
        exit_b.grid(row=10, column=0,padx=5, pady=5 ,sticky=W+S)

        # Cancel Button
        cancel_b= Button(self, text="Cancel", command= self.on_close , style="Blue.TButton")
        cancel_b.grid(row=10, column=1,padx=5, pady=5 ,sticky=W+S)
        
        # This is useful to later retrieve the info from the MainGUI class
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.on_save_and_exit= None

        # Read Json File, Initialize self.extensions, row and column to put the checkboxes in place in the widget
        self.my_json_reader= JsonReader()
        data= self.my_json_reader.read_json()
        self.extensions= data["extensions"]
        row=1
        column=0
        
        # Create the widget with checkboxes
        for extension in self.extensions:
            var = tk.IntVar()
            var.set(extension["allowed"])
            checkbox = Checkbutton(self, text=extension["extension"], variable=var, onvalue=1, offvalue=0,command=lambda value=var, ext=extension["extension"]: self.on_checkbox_click(ext, value, self.extensions),  style="Blue.TCheckbutton" )
            checkbox.grid(row=row, column=column, padx=3, pady=3, sticky=W)
            row+= 1
            if row== int(len(self.extensions)/2) + 1:
                column=1
                row=1
    # Work with the list and save the allowed changes
    def on_checkbox_click(self,extension, value, extensions):
        for ext in self.extensions:
            if ext["extension"] == extension:
                ext["allowed"] = value.get()
                break
    # Close the window
    def on_close(self):
        self.destroy()
    
    # Save and Close
    def on_save_and_exit(self):

        # It checks if there is at least one checkbox allowed
        if not any(ext["allowed"] for ext in self.extensions):
            messagebox.showerror("Error", "At least one extension must be allowed.")
            return
        #Read & Write Json File
        data= self.my_json_reader.read_json()
        data["extensions"] = self.extensions
        
        self.my_json_reader.write_json(data)
        # the if statement is a safeguard that ensures that a function is actually assigned to self.on_save_and_exit before attempting to call it.
        if self.on_save_and_exit:
            self.on_save_and_exit()
        self.destroy()

        
