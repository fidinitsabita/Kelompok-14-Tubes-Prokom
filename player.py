import tkinter as tk
from tkinter import messagebox
from player import *
from antrian import *
from utils import *
import json
import time
import yt_dlp
import logging


# Fungsi yang berhubungan dengan rekomendasi
def load_song_recommendations(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} tidak ditemukan!")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", "File JSON tidak valid!")
        return {}

def show_recommendations(mood_var, genre_var, listbox, name_var, RECOMMENDATIONS, queue, queue_listbox, play_button):
    mood = mood_var.get()
    genre = genre_var.get()
    if not mood or not genre:
        messagebox.showwarning("Peringatan", "Silakan pilih mood dan genre!")
        return

    songs = RECOMMENDATIONS.get(mood, {}).get(genre, [])
    if not songs:
        messagebox.showinfo("Info", "Tidak ada lagu yang tersedia untuk kombinasi ini.")
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

# Fungsi yang berhubungan dengan pemutar lagu
logging.basicConfig(filename="music_cafe_errors.log", level=logging.ERROR)
instance = vlc.Instance()
media_player = instance.media_player_new()

def get_youtube_stream_url(youtube_url):
    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return info_dict['url']
    except Exception as e:
        error_message = f"Failed to fetch stream URL: {e}"
        logging.error(error_message)
        print(error_message)
        return None

def player_thread_function(queue, queue_listbox):
    while True:
        if not media_player.is_playing() and queue:
            next_song = queue.pop(0)
            save_queue(queue)
            try:
                stream_url = get_youtube_stream_url(next_song['song']['url'])
                if not stream_url:
                    raise ValueError("Stream URL is None")
                media = instance.media_new(stream_url)
                media_player.set_media(media)
                media_player.play()
                print(f"Playing: {next_song['song']['title']}")
            except Exception as e:
                error_message = f"Error playing song: {e}"
                logging.error(error_message)
                print(error_message)
            update_queue_display(queue_listbox, queue)
        time.sleep(1)