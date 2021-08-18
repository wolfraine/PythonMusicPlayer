from tkinter.constants import ACTIVE, END, RAISED
import tkinter as tk #module to create grapgic interface
from tkinter import filedialog
import vlc 
import time 
from tinytag import TinyTag, TinyTagException 


# graphic 
root = tk.Tk()
root.title("Python Simple Player")
root.geometry("600x500") #podstawowy rozmiar okna

#List of audio files
fileListFrame = tk.Listbox(root, bg="aqua", fg="green", width=60)
fileListFrame.pack(pady=20)

#box to print audioFile tag's
audioTagBox = tk.Listbox(root, bg="white", fg="green", width=60)
audioTagBox.pack(pady=20)

# zmienna która przechowuje adres i nazwę pliku muzycznego
file='Alex2.mp3'

#class to use to chandle player
class music_Player():
    def __init__(self, audio_file):
    # creating a vlc instance
        vlc_instance = vlc.Instance()
    # creating a media player
        self.player = vlc_instance.media_player_new()
    # creating a media
        media = vlc_instance.media_new(audio_file)
    # setting media to the player
        self.player.set_media(media)
    
    def btn_play(self): #def play
        song = fileListFrame.get(ACTIVE)
        audio =music_Player(song)
        self.player.play()
    
    def btn_pause(self): #def pauzy
        self.player.pause()
    
    def btn_stop(self): #def stopu
        self.player.stop()

    def btn_next(self):
        pass

    def btn_prev(self):
        pass

audio =music_Player(file)

#Audio files tag's
def music_tag(song_file):
    tag = TinyTag.get(song_file)
    return 'Title: %s.' % tag.title + '\n' + 'Author: %s.' % tag.artist +'\n' + \
        'Album author: %s.' % tag.albumartist +'\n' + 'Genre: %s.' % tag.genre +'\n' + 'Time: %s.' % time.strftime('%H:%M:%S', time.gmtime(tag.duration))

def songtime(song_file): #return length of audio file in seconds
    tag = TinyTag.get(file)
    return tag.duration

def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose song", filetypes=(("mp3 Files", "*.mp3"), ))
    fileListFrame.insert(END, song)

#print tags -> add command to print info on click on file ?
var = tk.StringVar()
label_music_tag = tk.Label(master=audioTagBox, textvariable=var, relief=RAISED)
var.set(music_tag(file))
label_music_tag.pack()


#create panel control button
controlFrame = tk.Frame(root)
controlFrame.pack(pady= 10)

#button description
button_play = tk.Button(controlFrame, text="Play", command=audio.btn_play)
button_pause = tk.Button(controlFrame, text="Pause", command=audio.btn_pause)
button_stop = tk.Button(controlFrame, text="Stop", command=audio.btn_stop)
button_prev = tk.Button(controlFrame, text="<<", command=audio.btn_prev) 
button_next = tk.Button(controlFrame, text=">>", command=audio.btn_next) 

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
my_menu.add_cascade(label = "Add songs", menu = player_menu)
player_menu.add_command(label = "Add one Song to Playlist",command=add_song)

root.mainloop()