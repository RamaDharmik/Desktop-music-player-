import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames, askdirectory
from pathlib import Path
import pygame
import os

# Function to toggle the liked status of a song
def toggle_like(index):
    song_list[index]["liked"] = not song_list[index]["liked"]
    update_like_button(index)

# Function to update the appearance of the LIKE button based on the liked status
def update_like_button(index):
    liked_text = "❤" if song_list[index]["liked"] else "LIKE"
    like_button.config(text=liked_text)

# Creating the main application window
music_player = tk.Tk()
music_player.title("My Music Player")
music_player.geometry("500x400")

# Prompt the user to select music files
file_paths = askopenfilenames(title="Select Music File", filetypes=[("Audio Files", "*.mp3;*.wav")])
if not file_paths:
    messagebox.showinfo("Information", "No files selected. Please select the appropriate file name. Exiting.")

    # If the user wants to come back and select the files again, provide a comeback button
    comeback_button = tk.Button(music_player, text="Comeback", command=music_player.destroy)
    comeback_button.pack()
    music_player.mainloop()
    exit()

# Get the directory of the first selected file
directory = Path(file_paths[0]).parent

# Save the current working directory
original_directory = os.getcwd()

# Change the current working directory to the directory containing the first selected file
os.chdir(directory)

# Create a list of dictionaries with song information
song_list = [
    {"title": Path(file_path).name,
     "path": file_path,
     "liked": False}  # Added a "liked" field to track whether the song is liked
    for file_path in file_paths
]

# Add widgets to the window
play_list = tk.Listbox(music_player, font="Helvetica 12 bold", bg='brown', selectmode=tk.MULTIPLE)
for item in song_list:
    pos = 0
    play_list.insert(pos, item["title"])
    pos += 1

pygame.init()
pygame.mixer.init()

# Functioning for buttons
def play():
    selected_indices = play_list.curselection()
    if not selected_indices:
        messagebox.showinfo("Information", "No song selected. Please select a song to play.")
        return

    # Clear the playlist and play selected songs in a loop
    play_list.selection_clear(0, tk.END)
    for index in selected_indices:
        play_list.selection_set(index)

    play_selected_songs(selected_indices)

def play_selected_songs(selected_indices):
    for index in selected_indices:
        song_info = song_list[index]
        pygame.mixer.music.load(song_info["path"])
        var.set(song_info["title"])
        singer_label.config(text="Singer: " + song_info["singer"])  # Display singer's name
        pygame.mixer.music.play()
        pygame.mixer.music.queue(song_info["path"])  # Queue the song for looping

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

def play_next():
    current_index = play_list.curselection()
    if not current_index:
        messagebox.showinfo("Information", "No song selected. Please select a song to play.")
        return

    next_index = (current_index[0] + 1) % len(song_list)
    song_info = song_list[next_index]
    pygame.mixer.music.load(song_info["path"])
    var.set(song_info["title"])
    singer_label.config(text="Singer: " + song_info["singer"])  # Display singer's name
    pygame.mixer.music.play()

    # If the last song is played, loop back to the first song
    if next_index == 0:
        play_list.selection_clear(0, tk.END)
        play_list.selection_set(next_index)

def play_previous():
    current_index = play_list.curselection()
    if not current_index:
        messagebox.showinfo("Information", "No song selected. Please select a song to play.")
        return

    previous_index = (current_index[0] - 1) % len(song_list)
    song_info = song_list[previous_index]
    pygame.mixer.music.load(song_info["path"])
    var.set(song_info["title"])
    singer_label.config(text="Singer: " + song_info["singer"])  # Display singer's name
    pygame.mixer.music.play()

    # If the first song is played, loop to the last song
    if previous_index == len(song_list) - 1:
        play_list.selection_clear(0, tk.END)
        play_list.selection_set(previous_index)

# Add a heart symbol on LIKE button
like_button = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="LIKE", bg="pink",
                    fg="white", command=lambda: toggle_like(play_list.curselection()[0]))
like_button.pack(fill="x")

Button1 = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PLAY", command=play, bg="green",
                    fg="white")
Button2 = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="STOP", command=stop, bg="red",
                    fg="white")
Button3 = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PAUSE", command=pause,
                    bg="yellow", fg="white")
Button4 = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="UNPAUSE", command=unpause,
                    bg="orange", fg="white")
Button5 = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="NEXT", command=play_next, bg="blue",
                    fg="white")
Button6 = tk.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PREVIOUS", command=play_previous,
                    bg="purple", fg="white")

var = tk.StringVar()
song_title = tk.Label(music_player, font="Helvetica 12 bold", textvariable=var)

# Add a label to display singer's name
singer_label = tk.Label(music_player, font="Helvetica 12 bold", text="Singer: ")

song_title.pack()
singer_label.pack()
Button1.pack(fill="x")
Button2.pack(fill="x")
Button3.pack(fill="x")
Button4.pack(fill="x")
Button5.pack(fill="x")
Button6.pack(fill="x")
play_list.pack(fill="both", expand="yes")

# Restore the original working directory when the application is closed
music_player.protocol("WM_DELETE_WINDOW", lambda: [os.chdir(original_directory), music_player.destroy()])

music_player.mainloop()

