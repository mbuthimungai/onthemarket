from miningFunctionalities.miningFunctionalities import process_queue

import tkinter as tk
from tkinter import messagebox
import asyncio
from queue import Queue
from threading import Thread, Event


queue = Queue()
processing_thread = None
processing_event = Event()

def start_search():
    url = url_entry.get()
    custom_message = message_entry.get("1.0", 'end-1c') or """
I'm really interested in your property and was wondering if we could arrange a viewing. It would be great to meet in person and discuss the possibility of renting this property on a company let. We currently manage a few other properties with similar characteristics to yours, and we've built a strong track record with other landlords. We always strive to tailor our business model to meet their needs. 
We have plenty of references from landlords and investors we've worked with in the past as well as very good finances.
We'd be happy to provide more information and are looking forward to hearing from you. 
Alber
"""
    if len(custom_message) > 650:
        messagebox.showerror("Error", "The custom message is too long. It should be less than 650 characters.")
        return

    delay = int(delay_entry.get() or 100)  # Default delay to 100 ms

    queue.put((url, custom_message, delay))
    messagebox.showinfo("Success", "Task added to queue.")

def process_queue_wrapper():
    asyncio.run(process_queue(queue))

def start_queue_processing():
    global processing_thread
    if processing_thread is None or not processing_thread.is_alive():
        processing_thread = Thread(target=process_queue_wrapper)
        processing_thread.daemon = True  # This allows the thread to exit when the main program exits
        processing_thread.start()
        messagebox.showinfo("Info", "Started processing the queue.")
    else:
        messagebox.showinfo("Info", "Queue processing is already running.")

# Tkinter GUI
root = tk.Tk()
root.title("Property Search")

tk.Label(root, text="Search Properties URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Label(root, text="Custom Message:").pack()
message_entry = tk.Text(root, height=10, width=50)
message_entry.pack()

tk.Label(root, text="Typing Delay (ms):").pack()
delay_entry = tk.Entry(root, width=10)
delay_entry.pack()

search_button = tk.Button(root, text="Add to Queue", command=start_search)
search_button.pack()

process_button = tk.Button(root, text="Process Queue", command=start_queue_processing)
process_button.pack()

root.mainloop()