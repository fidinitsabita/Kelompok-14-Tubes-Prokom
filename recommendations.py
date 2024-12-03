import json
import tkinter as tk
from tkinter import messagebox, Listbox
from utils import load_recommendations

SONG_FILE = r"C:\Users\julia\nastu mencoba\song_recommendations.json"
RECOMMENDATIONS = load_recommendations()

def load_song_recommendations(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} not found!")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON file format!")
        return {}

def show_recommendations(mood_var, genre_var, listbox, name_var, RECOMMENDATIONS, queue, queue_listbox, play_button):
    mood = mood_var.get()
    genre = genre_var.get()
    if not mood or not genre:
        messagebox.showwarning("Warning", "Please select mood and genre!")
        return

    songs = RECOMMENDATIONS.get(mood, {}).get(genre, [])
    if not songs:
        messagebox.showinfo("Info", "No songs available for this combination.")
        return

    def on_song_select(event):
        selected_index = listbox.curselection()
        if selected_index:
            selected_song = songs[selected_index[0]]
            song_data = {
                "name": name_var.get(),
                "song": {
                    "title": selected_song.get("title", "Unknown Title"),
                    "url": selected_song.get("url", "")
                }
            }
            play_button.config(state=tk.NORMAL)
            play_button.song_data = song_data

    listbox.delete(0, tk.END)
    for song in songs:
        listbox.insert(tk.END, song.get("title", "Unknown Title"))
    listbox.bind("<<ListboxSelect>>", on_song_select)