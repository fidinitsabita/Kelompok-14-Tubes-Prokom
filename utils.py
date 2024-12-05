import json
import tkinter as tk
from tkinter import messagebox

# Menyambungkan kefile song_recommendations.json
SONG_FILE = r"C:\nastu\mas dani mencoba\song_recommendations.json"

# Memuat rekomendasi lagu yang ada
def load_recommendations():
    try:
        with open(SONG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

RECOMMENDATIONS = load_recommendations()

#  memuat ulang data rekomendasi lagu dari file JSON
def reload_recommendations():
    global RRECOMMENDATIONS
    RECOMMENDATIONS = load_recommendations()
    print("Reloaded data:", RECOMMENDATIONS)  # Debugging

# menyimpan data rekomendasi lagu ke dalam file JSON
def save_recommendations():
    try:
        with open(SONG_FILE, "w") as f:
            json.dump(RECOMMENDATIONS, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

# mengatur ulang antarmuka utama aplikasi ke keadaan awal atau kosong.
def reset_main_window(mood_var, genre_var, listbox, play_button):
    mood_var.set("")
    genre_var.set("")
    listbox.delete(0, tk.END)
    play_button.config(state=tk.DISABLED)
    
# Fungsi jika pengguna masih ingin menambah lagu atau tidak    
def ask_to_continue(name_var, mood_var, genre_var, listbox, play_button, root, login_frame, mood_genre_frame):
    """Handles whether the user wants to continue selecting songs."""
    response = messagebox.askyesno("Continue?", "Apakah Anda ingin memilih lagu lagi?")
    if response:  
        # Reset pemilihan mood dan genre 
        mood_var.set("")
        genre_var.set("")
        listbox.delete(0, tk.END)
        reset_main_window(mood_var, genre_var, listbox, play_button)
    else:  
        # memberi informasi ke pelanggan dan kembali ke input nama
        messagebox.showinfo("Info", "Terima kasih! Anda akan kembali ke pengisian nama.")
        mood_genre_frame.pack_forget()  # menghilangkankan frame mood dan genre
        name_var.set("")  # menghapus bagian nama
        login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Menampilkan login frame kembali