import tkinter as tk
from tkinter import ttk, messagebox, font
from player import *
from antrian import *
from utils import *

def reset_main_window(mood_var, genre_var, listbox, play_button):
    mood_var.set("")
    genre_var.set("")
    listbox.delete(0, tk.END)
    play_button.config(state=tk.DISABLED)

def ask_to_continue(name_var, mood_var, genre_var, listbox, play_button, root, login_frame, mood_genre_frame):
    """Handles whether the user wants to continue selecting songs."""
    response = messagebox.askyesno("Lanjutkan?", "Apakah kamu ingin memilih lagu lagi?")
    if response:  # Pelanggan ingin memilih lagu lagi
        # Mereset pemilihan mood dan genre
        mood_var.set("")
        genre_var.set("")
        listbox.delete(0, tk.END)
        reset_main_window(mood_var, genre_var, listbox, play_button)
    else:  # Pelanggan sudah selesai
        messagebox.showinfo("Info", "Terima kasih! Kamu akan kembali ke pengisian nama.")
        mood_genre_frame.pack_forget() 
        name_var.set("")  # Membersihkan entry nama
        login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Memunculkan kembali frame pengisian nama
