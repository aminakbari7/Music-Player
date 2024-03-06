
# Importing the required liabraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
import os
from tkinter import messagebox

# Creating main class called "MusicPlayer" and initializing the root window
class MusicPlayer:

    # Initializing the root window
    def __init__(self, root):
        self.root = root

        # Title and geometry of the root window
        self.root.title("DataFlair - Music Player")

        # Setting the geometry of the root window
        self.root.geometry("750x400")
        self.root.resizable(False, False)

        # Setting the background image
        self.bg_image =  tk.PhotoImage(file="music/bg_con.png")
        self.bg_label = ttk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relx=0, rely=-0, relwidth=1, relheight=1)

        # Setting style for the root window
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('.', background='black', foreground='black')
        s.configure('TFrame', background='white', foreground='white')
        s.configure('TButton', font=('Arial', 12), background='black', foreground='white', 
                                            activebackground='brown', activeforeground='white')
        s.configure('TLabel', font=('Arial', 12), background='black', foreground='white')
        s.configure('TScale', background='white')

        # Initializing Pygame
        pygame.init()

        # Initializing Pygame Mixer
        pygame.mixer.init()

        # Playlist Frame
        self.playlist_frame = tk.Frame(self.root)
        self.playlist_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Playlist Listbox
        self.playlist = tk.Listbox(self.playlist_frame, width=40, height=20)
        self.playlist.pack(fill=tk.BOTH, expand=True)
        self.playlist.bind("<<ListboxSelect>>", self.play_selected)

        # Control Frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10)
        self.control_frame.configure(border=1, relief="groove", borderwidth=2)

        # Background image for the control frame
        self.bg_image3 =  tk.PhotoImage(file ="music/control_bg.png")
        self.bg_label3 = ttk.Label(self.control_frame, image=self.bg_image3)
        self.bg_label3.place(relx=0, rely=-0, relwidth=1, relheight=1)

        # Play/Pause button
        self.play_var = tk.StringVar()
        self.play_var.set("Play")
        self.play_pause_button = ttk.Button(self.control_frame, textvariable=self.play_var, command=self.play_pause)
        self.play_pause_button.grid(row=1, column=0, padx=10, pady=10)

        # Skip Backward button
        self.skip_backward_button = ttk.Button(self.control_frame, text="⏪", command=self.skip_backward)
        self.skip_backward_button.grid(row=2, column=0, padx=10, pady=10)

        # Skip Forward button
        self.skip_forward_button = ttk.Button(self.control_frame, text="⏩", command=self.skip_forward)
        self.skip_forward_button.grid(row=3, column=0, padx=10, pady=10)

        # Status Label and Volume Control label
        self.status_var = tk.StringVar()
        self.status_var.set("Volume Control")
        self.status_label = ttk.Label(self.control_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, padx=10, pady=10)

        # Volume control
        self.volume_var = tk.DoubleVar()
        self.volume_scale = ttk.Scale(self.control_frame, orient="horizontal", from_=0, to=1, 
                                                variable=self.volume_var, command=self.set_volume)
        self.volume_scale.grid(row=5, column=0, padx=10, pady=10)

        # Import Music button
        self.import_button = ttk.Button(self.control_frame, text="Import Music", command=self.import_music)
        self.import_button.grid(row=6, column=0, padx=10, pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.control_frame, orient="horizontal", length=325, mode="determinate")
        self.progress_bar.grid(row=7, column=0, padx=10, pady=10)

        # Elapsed time label to give both visual and numerical feedback to the user 
        self.elapsed_time = ttk.Label(self.control_frame, text="00:00")
        self.elapsed_time.grid(row=8, column=0, padx=10, pady=10)

        # Current song label
        self.current_song = ""

        # Paused variable to check if the song is paused or not
        self.paused = False

    # Function to play the selected song in the playlist
    def play_selected(self, event):
        selected_song = self.playlist.get(self.playlist.curselection())
        self.current_song = selected_song
        pygame.mixer.music.load(self.current_song)
        self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[0:40]+"...")
        self.progress_bar["maximum"] = pygame.mixer.Sound(self.current_song).get_length()
        self.update_progressbar()
        pygame.mixer.music.play()
        self.play_var.set("Pause")

    # Function to play and pause the song currently playing
    # using the play/pause button
    def play_pause(self):
        # play or pause the current song
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_var.set("Pause")
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_var.set("Play")

    # Function to skip to the previous song
    # using the skip backward button
    def skip_backward(self):
        # skip to the previoussong
        selection = self.playlist.curselection()
        if selection:
            prev_song_index = int(selection[0]) - 1
            if prev_song_index >= 0:
                prev_song = self.playlist.get(prev_song_index)
                self.current_song = prev_song
                pygame.mixer.music.load(self.current_song)
                self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[0:40]+"...")
                pygame.mixer.music.play()
                self.play_var.set("Pause")
            else:
                messagebox.showwarning("Warning", "This is the first song.")
        else:
            messagebox.showerror("Error", "No song is selected.")

    # Function to skip to the next song
    # using the skip forward button
    def skip_forward(self):
        # skip to the nextsong
        selection = self.playlist.curselection()
        if selection:
            next_song_index = int(selection[0]) + 1
            if next_song_index < self.playlist.size():
                next_song = self.playlist.get(next_song_index)
                self.current_song = next_song
                pygame.mixer.music.load(self.current_song)
                self.status_var.set("Now Playing: " + os.path.basename(self.current_song)[0:40]+"...")
                pygame.mixer.music.play()
                self.play_var.set("Pause")
            else:
                messagebox.showwarning("Warning", "This is the last song.")

    # Function to set the volume
    # using the volume scale
    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    # Function to import music files
    # using the import button
    def import_music(self):
        # import multiple music files from the local directory
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            #if already in the playlist, don't add it again
            if file_path not in self.playlist.get(0, tk.END):
                self.playlist.insert(tk.END, file_path)

    # Function to update the progress bar
    def update_progressbar(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        self.progress_bar["value"] = current_time
        minutes, seconds = divmod(int(current_time), 60)
        self.elapsed_time.config(text="{:02d}:{:02d}".format(minutes, seconds))
        self.root.after(1000, self.update_progressbar)


# Main program starts here using the class MusicPlayer
# and the root window
root = tk.Tk()
MusicPlayer(root)

# Run the main window loop
root.mainloop()
