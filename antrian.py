import tkinter as tk
from tkinter import  messagebox
import json

# Queue-related functions
QUEUE_FILE = r"queue.json"

def load_queue():
    try:
        with open(QUEUE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_queue(queue):
    try:
        with open(QUEUE_FILE, "w") as file:
            json.dump(queue, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save queue: {e}")

def update_queue_display(queue_listbox, queue):
    queue_listbox.delete(0, tk.END)
    for index, song in enumerate(queue, start=1):
        queue_listbox.insert(tk.END, f"{index}. {song['song']['title']} - {song['name']}")

def add_to_queue(song_data, queue):
    queue.append(song_data)
    save_queue(queue)
    print(f"Added to queue: {song_data['song']['title']} by {song_data['name']}")
    print("Current Queue:")
    for song in queue:
        print(f"- {song['song']['title']} by {song['name']}")
