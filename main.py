import json
import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
from utils import load_recommendations, reload_recommendations, save_recommendations, ask_to_continue
from antrian import update_queue_display, load_queue, add_to_queue
from recommendations import show_recommendations
from player import player_thread_function
from PIL import Image, ImageTk

# Main application
SONG_FILE = r"C:\Users\julia\nastu mencoba\song_recommendations.json"
RECOMMENDATIONS = load_recommendations()

def main():
    global recommendations
    reload_recommendations()
    root = tk.Tk()
    root.title("Music Cafe")
    root.geometry("1366x768")

    left_frame = tk.Frame(root, width=683, height=768, bg="#ffd5ef")
    left_frame.pack(side="left", fill="both", expand=False)
    left_frame.pack_propagate(False)
    
    queue_frame = tk.Frame(root, width=683, height=768, bg="#ffd5ef")
    queue_frame.pack(side="right", fill="both", expand=False)
    queue_frame.pack_propagate(False)

    canvas2 = tk.Canvas(queue_frame, width=683, height=768, bg="#ffd5ef", highlightthickness=0)
    canvas2.place(x=0, y=0)
    image2 = Image.open(r"C:\Users\julia\nastu mencoba\desain pink2.png")
    photo2 = ImageTk.PhotoImage(image2)
    canvas2.create_image(0, 0, anchor="nw", image=photo2)
    
    tk.Label(queue_frame, text="Queue List", font=("Today Show", 25, "bold"), bg="#ffd5ef").pack(pady=30)
    queue_listbox = tk.Listbox(queue_frame, width=50, height=25, font=("Arial", 10))
    queue_listbox.pack(pady=20)

    queue = load_queue()
    update_queue_display(queue_listbox, queue)

    login_frame = tk.Frame(left_frame, bg="#ffd5ef")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(login_frame, text="Welcome to", font=('Today Show', 20), fg="black", bg="#ffd5ef").pack()
    tk.Label(login_frame, text="NotaRasa", font=('Workspace', 40, 'bold'), fg="black", bg="#ffd5ef").pack()
    tk.Label(login_frame, text="Enter your name:", font=("Arial", 12), bg="#ffd5ef").pack(pady=5)
    name_var = tk.StringVar()
    tk.Entry(login_frame, textvariable=name_var, font=("Arial", 12)).pack(pady=5)

    def proceed_to_mood_genre():
        reload_recommendations()
        if not name_var.get():
            messagebox.showwarning("Warning", "Please enter your name!")
            return
        greeting_label.config(text=f"Hai, {name_var.get()}! Yuk pilih lagu yang cocok buat kamu hari ini!")
        
        mood_var.set("")
        genre_var.set("")
        listbox.delete(0, tk.END)
        mood_combo['values'] = list(RECOMMENDATIONS.keys())
        login_frame.place_forget()
        mood_genre_frame.pack(fill="both", expand=True)

    tk.Button(login_frame, text="Submit", command=proceed_to_mood_genre, bg="#fff6a9", font=("Arial", 12)).pack(pady=10)
    
    def admin_passcode_interface(): # Admin Interface
        admin_window_frame = tk.Toplevel()
        admin_window_frame.title("Admin Login")
        admin_window_frame.geometry("500x450")
        admin_window_frame.resizable(True, True)
        admin_window = tk.Frame (admin_window_frame, bg="lightyellow")
        admin_window.place(relx=0.5, rely=0.5, anchor="center")     
        
        # Label for Enter passcode
        tk.Label(admin_window, text="Enter passcode:", font=("Arial", 12), bg="lightyellow").grid(row=0, column=0, pady=10, padx=10, sticky='w')
    
        passcode_var = tk.StringVar()
        # Entry field for passcode
        tk.Entry(admin_window, textvariable=passcode_var, font=("Arial", 12), show="*").grid(row=1, column=0, pady=10, padx=10)

        # Button to submit passcode
        def check_passcode():
            if passcode_var.get() == "admin123":
                for widget in admin_window.winfo_children(): # hapus semua widget di admin_window
                    widget.destroy()
                
                admin_interface(admin_window) # panggil admin_interface di jendela yang sama
            else:
                messagebox.showerror("Error", "Incorrect passcode!")

        tk.Button(admin_window, text="Submit", command=check_passcode, font=("Arial", 12)).grid(row=2, columnspan=2, pady=10)
        
        # Admin interface
        def admin_interface(admin_window):
            global RECOMMENDATIONS
            RECOMMENDATIONS = load_recommendations()  # Reload to ensure sync

            tk.Label(admin_window, text="Add New Song", font=("Dancing Script", 16)).grid(row=0, columnspan=2, pady=10)
            # Mood Selection
            tk.Label(admin_window, text="Mood:", font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=10, sticky='w')
            mood_var = tk.StringVar()
            mood_combobox = ttk.Combobox(admin_window, textvariable=mood_var, font=("Arial", 12), values=list(RECOMMENDATIONS.keys()), state="readonly")
            mood_combobox.grid(row=1, column=1, pady=5, padx=10)

            # Add delete button for mood
            def delete_mood():
                selected_mood = mood_var.get()
                if selected_mood and selected_mood in RECOMMENDATIONS:
                    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the mood '{selected_mood}'?"):
                        del RECOMMENDATIONS[selected_mood]
                        save_recommendations()
                        mood_combobox["values"] = list(RECOMMENDATIONS.keys())
                        messagebox.showinfo("Success", "Mood deleted successfully!")
                else:
                    messagebox.showwarning("Warning", "No mood selected or mood does not exist.")

            tk.Button(admin_window, text="Delete Mood", command=delete_mood, font=("Arial", 12)).grid(row=1, column=2, padx=10)

            tk.Label(admin_window, text="or add new mood:", font=("Arial", 12)).grid(row=2, column=0, pady=5, padx=10, sticky='w')
            new_mood_var = tk.StringVar()
            new_mood_entry = tk.Entry(admin_window, textvariable=new_mood_var, font=("Arial", 12))
            new_mood_entry.grid(row=2, column=1, pady=5, padx=10)

            # Genre Selection
            tk.Label(admin_window, text="Genre:", font=("Arial", 12)).grid(row=3, column=0, pady=5, padx=10, sticky='w')
            genre_var = tk.StringVar()
            genre_combobox = ttk.Combobox(admin_window, textvariable=genre_var, font=("Arial", 12), state="readonly")
            genre_combobox.grid(row=3, column=1, pady=5, padx=10)
            genre_combobox["values"] = []

            # Add delete button for genre
            def delete_genre():
                selected_mood = mood_var.get()
                selected_genre = genre_var.get()
                if selected_mood in RECOMMENDATIONS and selected_genre in RECOMMENDATIONS[selected_mood]:
                    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the genre '{selected_genre}'?"):
                        del RECOMMENDATIONS[selected_mood][selected_genre]
                        if not RECOMMENDATIONS[selected_mood]:  # Remove mood if no genres left
                            del RECOMMENDATIONS[selected_mood]
                        save_recommendations()
                        update_genres()
                        messagebox.showinfo("Success", "Genre deleted successfully!")
                else:
                    messagebox.showwarning("Warning", "No genre selected or genre does not exist.")

            tk.Button(admin_window, text="Delete Genre", command=delete_genre, font=("Arial", 12)).grid(row=3, column=2, padx=10)

            def update_genres(*args):
                selected_mood = mood_var.get()
                if selected_mood in RECOMMENDATIONS:
                    genre_combobox["values"] = list(RECOMMENDATIONS[selected_mood].keys())
                else:
                    genre_combobox["values"] = []
                genre_var.set("")
            mood_var.trace("w", update_genres)

            tk.Label(admin_window, text="or add new genre:", font=("Arial", 12)).grid(row=4, column=0, pady=5, padx=10, sticky='w')
            new_genre_var = tk.StringVar()
            new_genre_entry = tk.Entry(admin_window, textvariable=new_genre_var, font=("Arial", 12))
            new_genre_entry.grid(row=4, column=1, pady=5, padx=10)
    
            # Clear All Functionality
            def clear_all():
                mood_var.set("")
                new_mood_var.set("")
                genre_var.set("")
                new_genre_var.set("")
                song_title_var.set("")
                artist_var.set("")
                url_var.set("")
                genre_combobox["values"] = []

            tk.Button(admin_window, text="Clear All", command=clear_all, font=("Arial", 12)).grid(row=10, columnspan=2, pady=10)
            # Disable combobox or entry if the other is filled
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

            # Song Details
            tk.Label(admin_window, text="Song Title:", font=("Arial", 12)).grid(row=5, column=0, pady=5, padx=10, sticky='w')
            song_title_var = tk.StringVar()
            tk.Entry(admin_window, textvariable=song_title_var, font=("Arial", 12)).grid(row=5, column=1, pady=5, padx=10)

            tk.Label(admin_window, text="Artist:", font=("Arial", 12)).grid(row=6, column=0, pady=5, padx=10, sticky='w')
            artist_var = tk.StringVar()
            tk.Entry(admin_window, textvariable=artist_var, font=("Arial", 12)).grid(row=6, column=1, pady=5, padx=10)

            tk.Label(admin_window, text="YouTube URL:", font=("Arial", 12)).grid(row=7, column=0, pady=5, padx=10, sticky='w')
            url_var = tk.StringVar()
            tk.Entry(admin_window, textvariable=url_var, font=("Arial", 12)).grid(row=7, column=1, pady=5, padx=10)

            # Add Song Functionality
            def add_song():
                mood = new_mood_var.get() or mood_var.get()
                genre = new_genre_var.get() or genre_var.get()
                song_title = song_title_var.get()
                artist = artist_var.get()
                url = url_var.get()

                if not mood or not genre:
                    messagebox.showwarning("Warning", "Please select or add a mood and genre!")
                    return

                if not song_title or not artist or not url:
                    messagebox.showwarning("Warning", "Please fill in all fields!")
                    return

                if mood not in RECOMMENDATIONS:
                    RECOMMENDATIONS[mood] = {}
                if genre not in RECOMMENDATIONS[mood]:
                    RECOMMENDATIONS[mood][genre] = []

                # Add the song to the correct list
                RECOMMENDATIONS[mood][genre].append({"title": f"{song_title} - {artist}", "url": url})
                save_recommendations()

                # Refresh UI
                mood_combobox["values"] = list(RECOMMENDATIONS.keys())
                genre_combobox["values"] = []
                messagebox.showinfo("Success", "Song added successfully!")

                # Clear inputs
                mood_var.set("")
                new_mood_var.set("")
                genre_var.set("")
                new_genre_var.set("")
                song_title_var.set("")
                artist_var.set("")
                url_var.set("")
                
            tk.Button(admin_window, text="Add Song", command=add_song, font=("Arial", 12)).grid(row=8, columnspan=2, pady=10)
            # View Songs Functionality
            def view_songs():
                selected_mood = mood_var.get()
                selected_genre = genre_var.get()

                if selected_mood in RECOMMENDATIONS and selected_genre in RECOMMENDATIONS[selected_mood]:
                    songs = RECOMMENDATIONS[selected_mood][selected_genre]
                    song_list = "\n".join([f"{song['title']} - {song['url']}" for song in songs])

                    # Create a new window to display the list of songs
                    songs_window = tk.Toplevel()
                    songs_window.title(f"Songs for Mood: {selected_mood} and Genre: {selected_genre}")

                    # Label for the title
                    tk.Label(songs_window, text=f"Songs for Mood: {selected_mood} and Genre: {selected_genre}", font=("Arial", 14)).grid(row=0, columnspan=2, pady=10)

                    # Listbox to display the songs
                    song_listbox = tk.Listbox(songs_window, font=("Arial", 12), width=50, height=10)
                    song_listbox.grid(row=1, column=0, pady=10, padx=10)

                    # Populate the Listbox with the songs
                    for idx, song in enumerate(songs):
                        song_listbox.insert(tk.END, f"{song['title']} - {song['url']}")

                    # Function to delete a song
                    def delete_song():
                        selected_song_index = song_listbox.curselection()
                        if selected_song_index:
                            selected_song = songs[selected_song_index[0]]
                            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_song['title']}'?"):
                                songs.remove(selected_song)
                                save_recommendations()
                                song_listbox.delete(selected_song_index)
                                messagebox.showinfo("Success", "Song deleted successfully!")

                    # Button to delete a song
                    tk.Button(songs_window, text="Delete Song", command=delete_song, font=("Arial", 12)).grid(row=2, columnspan=2, pady=10)

                else:
                    messagebox.showwarning("Warning", "No songs available for the selected mood and genre.")

            # Button to view songs
            tk.Button(admin_window, text="View Songs", command=view_songs, font=("Arial", 12)).grid(row=9, columnspan=2, pady=10)
   
    underline_font = font.Font(family="Arial", size=10, underline=True)  # Font dengan underline
    tk.Button(login_frame, text="Login as Admin", command=admin_passcode_interface, font=underline_font, fg="blue", bg="#ffd5ef", relief=tk.FLAT, cursor="hand2").pack(pady=(5, 0))

    mood_genre_frame = tk.Frame(left_frame, bg="#ffd5ef")
    
    def update_genres(event):
        # Ambil mood yang dipilih
        selected_mood = mood_var.get()
    
        # Update genre berdasarkan mood yang dipilih
        if selected_mood in RECOMMENDATIONS:
            genre_combo['values'] = list(RECOMMENDATIONS[selected_mood].keys())
        else:
            genre_combo['values'] = []
            
    reload_recommendations()
    greeting_label = tk.Label(mood_genre_frame, text="Hai, {name_var.get()}! Yuk pilih lagu yang cocok buat kamu hari ini!", font=("Arial", 16), bg="#ffd5ef")
    greeting_label.pack(pady=5)
    tk.Label(mood_genre_frame, text="Select Mood:", font=("Arial", 12), bg="#ffd5ef").pack(pady=5)
    mood_var = tk.StringVar()
    mood_combo = ttk.Combobox(mood_genre_frame, textvariable=mood_var, font=("Arial", 12))
    mood_combo['values'] = list(RECOMMENDATIONS.keys())
    mood_combo.pack(pady=5)

    mood_combo.bind("<<ComboboxSelected>>", update_genres)
    
    tk.Label(mood_genre_frame, text="Select Genre:", font=("Arial", 12), bg="#ffd5ef").pack(pady=5)
    genre_var = tk.StringVar()
    genre_combo = ttk.Combobox(mood_genre_frame, textvariable=genre_var, font=("Arial", 12))
    genre_combo.pack(pady=5)

    tk.Label(mood_genre_frame, text="Song Recommendations:", font=("Arial", 12), bg="#ffd5ef").pack(pady=5)
    listbox = tk.Listbox(mood_genre_frame, width=40, height=10, font=("Arial", 10))
    listbox.pack(pady=10)
    
    play_button = tk.Button(mood_genre_frame, text="Play Song", state=tk.DISABLED, font=("Arial", 12), command=lambda: [
    add_to_queue(play_button.song_data, queue),
    update_queue_display(queue_listbox, queue),
    ask_to_continue(name_var, mood_var, genre_var, listbox, play_button, root, login_frame, mood_genre_frame)
    ])

    play_button.pack(pady=10)

    tk.Button(mood_genre_frame, text="Search", font=("Arial", 12), command=lambda: show_recommendations(
        mood_var, genre_var, listbox, name_var, RECOMMENDATIONS, queue, queue_listbox, play_button)).pack(pady=10)

    thread = threading.Thread(target=player_thread_function, args=(queue, queue_listbox), daemon=True)
    thread.start()

    root.mainloop()
    
if __name__ == "__main__":
    main()
