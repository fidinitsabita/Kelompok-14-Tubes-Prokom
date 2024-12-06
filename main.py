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

SONG_FILE = r"song_recommendations.json"

# Memuat rekomendasi lagu yang ada
def load_recommendations():
    try:
        with open(SONG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

RECOMMENDATIONS = load_recommendations()

# Muat ulang rekomendasi
def reload_recommendations():
    RECOMMENDATIONS = load_recommendations()
    print("Reloaded data:", RECOMMENDATIONS)  # Debugging

# Simpan rekomendasi yang diperbarui
def save_recommendations():
    try:
        with open(SONG_FILE, "w") as f:
            json.dump(RECOMMENDATIONS, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {e}")    
    
# Aplikasi utama
def main():
    global recommendations
    reload_recommendations()
    root = tk.Tk()
    root.title("NotaRasa")
    root.geometry("1366x768")

    left_frame = tk.Frame(root, width=683, height=768, bg="#fffff0")
    left_frame.pack(side="left", fill="both", expand=False)
    left_frame.pack_propagate(False)
    
    # Menambahkan background untuk frame login
    left_canvas = tk.Canvas(left_frame, width=683, height=768, bg="#ffd5ef", highlightthickness=0)
    left_canvas.place(x=0, y=0)
    left_image = Image.open(r"background\canvani4.png")
    left_photo = ImageTk.PhotoImage(left_image)
    left_canvas.create_image(0, 0, anchor="nw", image=left_photo)
    
    queue_frame = tk.Frame(root, width=683, height=768, bg="#ffd5ef")
    queue_frame.pack(side="right", fill="both", expand=False)
    queue_frame.pack_propagate(False)
    
    # Menambahkan background untuk frame antrian
    queue_canvas = tk.Canvas(queue_frame, width=683, height=768, bg="#ffd5ef", highlightthickness=0)
    queue_canvas.place(x=0, y=0)
    queue_image = Image.open(r"background\daripin.jpg")
    queue_photo = ImageTk.PhotoImage(queue_image)
    queue_canvas.create_image(0, 0, anchor="nw", image=queue_photo)

    tk.Label(queue_frame, text="Daftar Antrian", font=("Elegante Classica", 25), bg="#fffff0").pack(pady=15)
    queue_listbox = tk.Listbox(queue_frame, width=40, height=20, font=("Times New Roman", 15))
    queue_listbox.pack(pady=20)

    queue = load_queue()
    update_queue_display(queue_listbox, queue)

    login_frame = tk.Frame(left_frame, bg="#fffff0")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(login_frame, text="Selamat datang di", font=("Elegante Classica", 15), bg="#fffff0").pack()
    tk.Label(login_frame, text="NotaRasa", font=("Amertha PERSONAL USE ONLY", 60), fg="pink", bg="#fffff0").pack()
    tk.Label(login_frame, text="Masukkan nama kamu:", font=("Elegante Classica", 13), bg="#fffff0").pack(pady=5)
    name_var = tk.StringVar()
    tk.Entry(login_frame, textvariable=name_var, font=("Times New Roman", 18)).pack(pady=5) # entry nama

    def proceed_to_mood_genre():
        reload_recommendations()
        if not name_var.get():
            messagebox.showwarning("Peringatan", "Masukkan nama kamu!")
            return
        greeting_label.config(text=f"Hai, {name_var.get()}! Yuk pilih lagu yang cocok buat kamu hari ini!")
        
        mood_var.set("")
        genre_var.set("")
        listbox.delete(0, tk.END)
        mood_combo['values'] = list(RECOMMENDATIONS.keys())
        login_frame.place_forget()
        mood_genre_frame.pack(fill="both", expand=True)

    submit_button = tk.Button(login_frame, text="Submit", command=proceed_to_mood_genre, font=("Elegante Classica", 12), bg="#cadebd")
    submit_button.pack(pady=10)
    
# Laman Admin
    def admin_passcode_interface():
        admin_window_frame = tk.Toplevel()
        admin_window_frame.title("Laman Admin")
        admin_window_frame.geometry("550x450")
        admin_window_frame.resizable(True, True) 
        
        # Menambahkan background untuk frame admin
        passcode_canvas = tk.Canvas(admin_window_frame, width=550, height=450, bg="#bffdce", highlightthickness=0)
        passcode_canvas.place(x=0, y=0)
        
        admin_window = tk.Frame (admin_window_frame, bg="#bffdce")
        admin_window.place(relx=0.5, rely=0.5, anchor="center") 
           
        # Label untuk memasukkan kata sandi
        tk.Label(admin_window, text="Masukkan kata sandi:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=0, column=0, pady=10, padx=10, sticky='w')
    
        passcode_var = tk.StringVar()
        # Entry kata sandi
        tk.Entry(admin_window, textvariable=passcode_var, font=("Times New Roman", 12), show="*").grid(row=1, column=0, pady=10, padx=10)

        # Button to submit passcode
        def check_passcode():
            if passcode_var.get() == "admin123":
                for widget in admin_window.winfo_children(): # hapus semua widget di admin_window
                    widget.destroy()
                
                admin_interface(admin_window) # panggil admin_interface di jendela yang sama
            else:
                messagebox.showerror("Error", "Kata sandi salah!")

        submit_button = tk.Button(admin_window, text="Submit", command=check_passcode, font=("Elegante Classica", 12))
        submit_button.grid(row=2, columnspan=2, pady=10)
        
        # Antarmuka admin
        def admin_interface(admin_window):
            global RECOMMENDATIONS
            RECOMMENDATIONS = load_recommendations()  # Memastikan sinkronisasi

            tk.Label(admin_window, text="Laman Penambahan Lagu", font=("Elegante Classica", 16), bg="#bffdce").grid(row=0, columnspan=2, pady=10)
            # Pemilihan mood
            tk.Label(admin_window, text="Mood:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=1, column=0, pady=5, padx=10, sticky='w')
            mood_var = tk.StringVar()
            mood_combobox = ttk.Combobox(admin_window, textvariable=mood_var, font=("Times New Roman", 12), values=list(RECOMMENDATIONS.keys()), state="readonly")
            mood_combobox.grid(row=1, column=1, pady=5, padx=10)

            def delete_mood():
                selected_mood = mood_var.get()
                if selected_mood and selected_mood in RECOMMENDATIONS:
                    if messagebox.askyesno("Konfirmasi Penghapusan", f"Apa kamu yakin untuk menghapus mood '{selected_mood}'?"):
                        del RECOMMENDATIONS[selected_mood]
                        save_recommendations()
                        mood_combobox["values"] = list(RECOMMENDATIONS.keys())
                        messagebox.showinfo("Berhasil", "Mood berhasil dihapus!")
                else:
                    messagebox.showwarning("Peringatan", "Mood tidak terpilih atau tidak ada.")

            delete_mood_button  = tk.Button(admin_window, text="Hapus Mood", command=delete_mood, font=("Elegante Classica", 12))
            delete_mood_button.grid(row=1, column=2, padx=10)

            tk.Label(admin_window, text="atau tambah mood baru:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=2, column=0, pady=5, padx=10, sticky='w')
            new_mood_var = tk.StringVar()
            new_mood_entry = tk.Entry(admin_window, textvariable=new_mood_var, font=("Times New Roman", 12))
            new_mood_entry.grid(row=2, column=1, pady=5, padx=10)

            # Pemilihan Genre
            tk.Label(admin_window, text="Genre:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=3, column=0, pady=5, padx=10, sticky='w')
            genre_var = tk.StringVar()
            genre_combobox = ttk.Combobox(admin_window, textvariable=genre_var, font=("Times New Roman", 12), state="readonly")
            genre_combobox.grid(row=3, column=1, pady=5, padx=10)
            genre_combobox["values"] = []

            # Add delete button for genre
            def delete_genre():
                selected_mood = mood_var.get()
                selected_genre = genre_var.get()
                if selected_mood in RECOMMENDATIONS and selected_genre in RECOMMENDATIONS[selected_mood]:
                    if messagebox.askyesno("Konfirmasi Penghapusan", f"Apa kamu yakin untuk menghapus genre '{selected_genre}'?"):
                        del RECOMMENDATIONS[selected_mood][selected_genre]
                        if not RECOMMENDATIONS[selected_mood]:  # Hapus mood jika tidak ada genre yang tersisa
                            del RECOMMENDATIONS[selected_mood]
                        save_recommendations()
                        update_genres()
                        messagebox.showinfo("Berhasil", "Genre berhasil dihapus!")
                else:
                    messagebox.showwarning("Peringatan", "Genre tidak terpilih atau tidak ada.")

            delete_genre_button = tk.Button(admin_window, text="Hapus Genre", command=delete_genre, font=("Elegante Classica", 12))
            delete_genre_button.grid(row=3, column=2, padx=10)

            def update_genres(*args):
                selected_mood = mood_var.get()
                if selected_mood in RECOMMENDATIONS:
                    genre_combobox["values"] = list(RECOMMENDATIONS[selected_mood].keys())
                else:
                    genre_combobox["values"] = []
                genre_var.set("")
            mood_var.trace("w", update_genres)

            tk.Label(admin_window, text="atau tambah genre baru:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=4, column=0, pady=5, padx=10, sticky='w')
            new_genre_var = tk.StringVar()
            new_genre_entry = tk.Entry(admin_window, textvariable=new_genre_var, font=("Times New Roman", 12))
            new_genre_entry.grid(row=4, column=1, pady=5, padx=10)
    
            # Tombol untuk mengosongkan semua
            def clear_all():
                mood_var.set("")
                new_mood_var.set("")
                genre_var.set("")
                new_genre_var.set("")
                song_title_var.set("")
                artist_var.set("")
                url_var.set("")
                genre_combobox["values"] = []

            clearall_button = tk.Button(admin_window, text="Bersihkan", command=clear_all, font=("Elegante Classica", 12))
            clearall_button.grid(row=10, columnspan=2, pady=10)
            
            # Menonaktifkan combobox mood/genre bila entry terisi dan sebaliknya
            def validate_mood_genre(*args):
                if new_mood_var.get():
                    mood_combobox["state"] = "disabled"
                else:
                    mood_combobox["state"] = "readonly"

                if new_genre_var.get():
                    genre_combobox["state"] = "disabled"
                else:
                    genre_combobox["state"] = "readonly"

                if mood_var.get():
                    new_mood_entry["state"] = "disabled"
                else:
                    new_mood_entry["state"] = "normal"

                if genre_var.get():
                    new_genre_entry["state"] = "disabled"
                else:
                    new_genre_entry["state"] = "normal"

            mood_var.trace("w", validate_mood_genre)
            new_mood_var.trace("w", validate_mood_genre)
            genre_var.trace("w", validate_mood_genre)
            new_genre_var.trace("w", validate_mood_genre)

            # Detail Lagu
            tk.Label(admin_window, text="Judul Lagu:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=5, column=0, pady=5, padx=10, sticky='w')
            song_title_var = tk.StringVar()
            tk.Entry(admin_window, textvariable=song_title_var, font=("Times New Roman", 12)).grid(row=5, column=1, pady=5, padx=10)

            tk.Label(admin_window, text="Artis:", font=("Elegante Classica", 12), bg="#bffdce").grid(row=6, column=0, pady=5, padx=10, sticky='w')
            artist_var = tk.StringVar()
            tk.Entry(admin_window, textvariable=artist_var, font=("Times New Roman", 12)).grid(row=6, column=1, pady=5, padx=10)

            tk.Label(admin_window, text="URL YouTube:", font=("Elegante Classica", 12),  bg="#bffdce").grid(row=7, column=0, pady=5, padx=10, sticky='w')
            url_var = tk.StringVar()
            tk.Entry(admin_window, textvariable=url_var, font=("Times New Roman", 12)).grid(row=7, column=1, pady=5, padx=10)

            # Fungsi penambahan lagu
            def add_song():
                mood = new_mood_var.get() or mood_var.get()
                genre = new_genre_var.get() or genre_var.get()
                song_title = song_title_var.get()
                artist = artist_var.get()
                url = url_var.get()

                if not mood or not genre:
                    messagebox.showwarning("Peringatan", "Silakan pilih atau tambahkan mood dan genre terlebih dahulu!")
                    return

                if not song_title or not artist or not url:
                    messagebox.showwarning("Peringatan", "Silakan isi semua kolom!")
                    return

                if mood not in RECOMMENDATIONS:
                    RECOMMENDATIONS[mood] = {}
                if genre not in RECOMMENDATIONS[mood]:
                    RECOMMENDATIONS[mood][genre] = []

                # Menambahkan lagu ke daftar yang tepat
                RECOMMENDATIONS[mood][genre].append({"title": f"{song_title} - {artist}", "url": url})
                save_recommendations()

                # Muat ulang UI
                mood_combobox["values"] = list(RECOMMENDATIONS.keys())
                genre_combobox["values"] = []
                messagebox.showinfo("Berhasil", "Lagu berhasil ditambahkan!")

                # Membersihkan input
                mood_var.set("")
                new_mood_var.set("")
                genre_var.set("")
                new_genre_var.set("")
                song_title_var.set("")
                artist_var.set("")
                url_var.set("")
                
            tk.Button(admin_window, text="Tambah Lagu", command=add_song, font=("Elegante Classica", 12)).grid(row=8, columnspan=2, pady=10)
            # Fungsi lihat daftar lagu
            def view_songs():
                selected_mood = mood_var.get()
                selected_genre = genre_var.get()

                if selected_mood in RECOMMENDATIONS and selected_genre in RECOMMENDATIONS[selected_mood]:
                    songs = RECOMMENDATIONS[selected_mood][selected_genre]
                    song_list = "\n".join([f"{song['title']} - {song['url']}" for song in songs])

                    # Membuat jendela baru untuk menampilkan daftar lagu yang sesuai
                    songs_window = tk.Toplevel()
                    songs_window.title(f"Daftar Lagu")
                    tk.Label(songs_window, text=f"Lagu untuk Mood: {selected_mood} dan Genre: {selected_genre}", font=("Elegante Classica", 14)).grid(row=0, columnspan=2, pady=10)
                    song_listbox = tk.Listbox(songs_window, font=("Times New Roman", 12), width=50, height=10)
                    song_listbox.grid(row=1, column=0, pady=10, padx=10)

                    # Mengisi listbox dengan daftar lagu yang sesuai
                    for idx, song in enumerate(songs):
                        song_listbox.insert(tk.END, f"{song['title']} - {song['url']}")

                    # Fungsi hapus lagu
                    def delete_song():
                        selected_song_index = song_listbox.curselection()
                        if selected_song_index:
                            selected_song = songs[selected_song_index[0]]
                            if messagebox.askyesno("Konfirmasi Penghapusan", f"Apa kamu yakin untuk menghapus lagu '{selected_song['title']}'?"):
                                songs.remove(selected_song)
                                save_recommendations()
                                song_listbox.delete(selected_song_index)
                                messagebox.showinfo("Berhasil", "Lagu berhasil dihapus!")
                                                    
                    delete_button = tk.Button(songs_window, text="Hapus Lagu", command=delete_song, font=("Elegante Classica", 12))
                    delete_button.grid(row=2, columnspan=2, pady=10)

                else:
                    messagebox.showwarning("Peringatan", "Tidak ada lagu yang tersedia untuk mood dan genre yang dipilih.")

            view_button = tk.Button(admin_window, text="Lihat Daftar Lagu", command=view_songs, font=("Elegante Classica", 12))
            view_button.grid(row=9, columnspan=2, pady=10)
   
    underline_font = font.Font(family="Times New Roman", size=12, underline=True)  # Font dengan underline
    tk.Button(login_frame, text="Login sebagai Admin", command=admin_passcode_interface, font=underline_font, fg="blue", bg="#fffff0", relief=tk.FLAT, cursor="hand2").pack(pady=(5, 0))
    tk.Label(login_frame, text="Kelompok 14 Kelas A", font=("Elegante Classica", 12), bg="#fffff0").pack(pady=10)

    mood_genre_frame = tk.Frame(left_frame, bg="#fffff0", width=400)
    greeting_label = tk.Label(mood_genre_frame, text="", font=("Elegante Classica", 16), bg="#fffff0", wraplength=600)
    greeting_label.pack(pady=20)

    def update_genres(event):
        # Ambil mood yang dipilih
        selected_mood = mood_var.get()
    
        # Update genre berdasarkan mood yang dipilih
        if selected_mood in RECOMMENDATIONS:
            genre_combo['values'] = list(RECOMMENDATIONS[selected_mood].keys())
        else:
            genre_combo['values'] = []
            
    reload_recommendations()
    tk.Label(mood_genre_frame, text="Pilih Mood:", font=("Elegante Classica", 14), bg="#fffff0").pack(pady=5)
    mood_var = tk.StringVar()
    mood_combo = ttk.Combobox(mood_genre_frame, textvariable=mood_var, font=("Times New Roman", 12))
    mood_combo['values'] = list(RECOMMENDATIONS.keys())
    mood_combo.pack(pady=5)

    mood_combo.bind("<<ComboboxSelected>>", update_genres)
    
    tk.Label(mood_genre_frame, text="Pilih Genre:", font=("Elegante Classica", 14), bg="#fffff0").pack(pady=5)
    genre_var = tk.StringVar()
    genre_combo = ttk.Combobox(mood_genre_frame, textvariable=genre_var, font=("Times New Roman", 12))
    genre_combo.pack(pady=5)

    tk.Label(mood_genre_frame, text="Rekomendasi Lagu:", font=("Elegante Classica", 14), bg="#fffff0").pack(pady=5)
    listbox = tk.Listbox(mood_genre_frame, width=40, height=10, font=("Times New Roman", 12))
    listbox.pack(pady=10)
    
    play_button = tk.Button(mood_genre_frame, text="Putar Lagu", state=tk.DISABLED, font=("Elegante Classica", 12), command=lambda: [
    add_to_queue(play_button.song_data, queue),
    update_queue_display(queue_listbox, queue),
    ask_to_continue(name_var, mood_var, genre_var, listbox, play_button, root, login_frame, mood_genre_frame)
    ])
    play_button.pack(pady=10)

    search_button = tk.Button(mood_genre_frame, text="Cari", font=("Elegante Classica", 12), command=lambda: show_recommendations(
        mood_var, genre_var, listbox, name_var, RECOMMENDATIONS, queue, queue_listbox, play_button))
    search_button.pack(pady=10)

    thread = threading.Thread(target=player_thread_function, args=(queue, queue_listbox), daemon=True)
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()