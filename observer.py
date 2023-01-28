""" 
This works, it is necessary to insert it into main.py which is where the layout will be
"""

import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

# In this function I should send to print, it is necessary to recover the name of the created file since event.src_path brings the full path 
def on_created(event):
     #print(f"hey, {event.src_path} has been created!")
     os.startfile(event.src_path, "print")

my_event_handler.on_created = on_created

path = "C:/Users/dario/OneDrive/Escritorio/PrintPython/"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)


my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()