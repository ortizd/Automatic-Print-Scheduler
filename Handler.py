from watchdog.observers import Observer
import watchdog.events
import os
from tkinter import messagebox
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.pdf", "*.docx"]
        ignore_patterns = None
        ignore_directories = True
        case_sensitive = True
        watchdog.events.PatternMatchingEventHandler.__init__(self,patterns, ignore_patterns, ignore_directories, case_sensitive)
    
    def on_created(self, event):
        try:
            os.startfile(event.src_path, "print")
        except:
            messagebox.showinfo(message="There is no application associated with the file", title="No printer")