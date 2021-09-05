from tkinter.constants import ACTIVE, END, FIRST, LAST, LEFT, RAISED
import tkinter as tk #module to create grapgic interface
from tkinter import filedialog
import time 
from tinytag import TinyTag, TinyTagException 
import pygame

# graphic 
root = tk.Tk()
root.title("Python Simple Player") # Title of window
root.geometry("600x500") #basic size of window

global paused #global value for pausing of file 
paused = False

#init pygame
pygame.mixer.init()

#List of audio files
fileListFrame = tk.Listbox(root, bg="aqua", fg="green", width=60)
fileListFrame.pack(pady=20)

#box to print audioFile tag's
audioTagBox = tk.Listbox(root, fg="green", width=60)
audioTagBox.pack(pady=20)

var = tk.StringVar()  #value of label audioTagBox
tagDefvalue = 'Title: ' + '\n' + 'Author: ' + '\n' + 'Album: ' +'\n' + 'Genre:' +'\n' + 'Time: ' 
var.set(tagDefvalue)

def btn_play(): #def play
    song = fileListFrame.get(ACTIVE)
    var.set(music_tag(song))    
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
def btn_pause(is_paused): #def pauzy
    global paused
    paused = is_paused
    if paused==True:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
    
def btn_stop(): #def stopu
    pygame.mixer.music.stop()
    fileListFrame.selection_clear(ACTIVE)
    var.set(tagDefvalue)

def btn_next():
    next_file = fileListFrame.curselection()
    next_file = next_file[0] + 1

    #if next_file is end index, then after click on next button index is set to first position
    if next_file == fileListFrame.index(END):
        next_file = fileListFrame.index(0)

    # grab file title from playlist
    song = fileListFrame.get(next_file)
    #load file and play
    var.set(music_tag(song))
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #move active bar in playlist
    fileListFrame.select_clear(0, END)
    fileListFrame.activate(next_file)
    fileListFrame.selection_set(next_file, last=None)


def btn_prev():
    next_file = fileListFrame.curselection()
    next_file = next_file[0] - 1

    #if next_file is first index, then after click on prev button, index is set to END position
    if next_file == fileListFrame.index(-1):
        next_file = (fileListFrame.index(END) - 1)

    # grab file title from playlist
    song = fileListFrame.get(next_file)
    #load file and play
    var.set(music_tag(song))
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #move active bar in playlist
    fileListFrame.select_clear(0, END)
    fileListFrame.activate(next_file)
    fileListFrame.selection_set(next_file, last=None)

#Audio files tag's
def music_tag(song_file):
    tag = TinyTag.get(song_file)
    return 'Title:      %s.' % tag.title + '\n' + 'Author: %s.' % tag.artist +'\n' + \
        'Album: %s.' % tag.album +'\n' + 'Genre:  %s.' % tag.genre +'\n' + 'Time:    %s.' % time.strftime('%H:%M:%S', time.gmtime(tag.duration))

def songtime(song_file): #return length of audio file in seconds
    tag = TinyTag.get(song_file)
    return tag.duration

def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose song", filetypes=(("mp3 Files", "*.mp3"), ))
    fileListFrame.insert(END, song)

def add_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose song", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        fileListFrame.insert(END, song)

#tags print label
label_music_tag = tk.Label(master=audioTagBox, textvariable=var, relief=RAISED, justify=LEFT, width=45, anchor='w', bg='white')
label_music_tag.pack()

#create panel control button
controlFrame = tk.Frame(root)
controlFrame.pack(pady= 10)

#button description
button_play = tk.Button(controlFrame, text="Play", command=btn_play)
button_pause = tk.Button(controlFrame, text="Pause", command=lambda: btn_pause(paused))
button_stop = tk.Button(controlFrame, text="Stop", command=btn_stop)
button_prev = tk.Button(controlFrame, text="<<", command=btn_prev) 
button_next = tk.Button(controlFrame, text=">>", command=btn_next) 

#button position
button_prev.grid(row=0, column=0)
button_stop.grid(row=0, column=1)
button_play.grid(row=0, column=2)
button_pause.grid(row=0, column=3)
button_next.grid(row=0, column=4)

my_menu = tk.Menu(root)
root.config(menu=my_menu)

#file menu
file_menu = tk.Menu(my_menu)
my_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Exit")

#add song menu
player_menu = tk.Menu(my_menu)
my_menu.add_cascade(label = "Add song/songs", menu = player_menu)
player_menu.add_command(label = "Add one Song to Playlist", command=add_song)
player_menu.add_command(label = "Add many Songs to Playlist", command=add_songs)
root.mainloop()
