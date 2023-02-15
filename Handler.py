from watchdog.observers import Observer
import watchdog.events
import os, json
from tkinter import messagebox
from JSONReader import JsonReader


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        my_json_reader= JsonReader()    
        data= my_json_reader.read_json()
        
        # Extensions allowed to be printed
        patterns= [extension["extension"] for extension in data["extensions"] if extension["allowed"] == 1]
        ignore_patterns = None
        ignore_directories = True
        case_sensitive = True
        watchdog.events.PatternMatchingEventHandler.__init__(self,patterns, ignore_patterns, ignore_directories, case_sensitive)
    
    def on_created(self, event):
        try:
            os.startfile(event.src_path, "print")
        except:
            messagebox.showinfo(message="There is no application associated with the file", title="No printer")

   