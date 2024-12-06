import tkinter as tk
from tkinter import ttk, messagebox, font
from player import *
from antrian import *
from utils import *
import threading
import json
import time
import sys
import vlc
import yt_dlp
import logging
from PIL import Image, ImageTk

# Utility functions
def reset_main_window(mood_var, genre_var, listbox, play_button):
    mood_var.set("")
    genre_var.set("")
    listbox.delete(0, tk.END)
    play_button.config(state=tk.DISABLED)

def ask_to_continue(name_var, mood_var, genre_var, listbox, play_button, root, login_frame, mood_genre_frame):
    """Handles whether the user wants to continue selecting songs."""
    response = messagebox.askyesno("Continue?", "Apakah Anda ingin memilih lagu lagi?")
    if response:  # User wants to choose another song
        # Reset mood and genre selection
        mood_var.set("")
        genre_var.set("")
        listbox.delete(0, tk.END)
        reset_main_window(mood_var, genre_var, listbox, play_button)
    else:  # User doesn't want to continue
        # Inform the user and return to the name input
        messagebox.showinfo("Info", "Terima kasih! Anda akan kembali ke pengisian nama.")
        mood_genre_frame.pack_forget()  # Hide the mood/genre frame
        name_var.set("")  # Clear the name field
        login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Show the login frame again
