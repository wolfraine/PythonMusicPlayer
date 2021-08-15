import vlc #vlc is used to play audio files
import time 
from tinytag import TinyTag, TinyTagException #use to tag reading 
from tkinter import * #module to create grapgic interface

# obsługa grafiki
root = Tk()
root.title("Python Simple Player")
root.geometry("600x500") #podstawowy rozmiar okna

#List of audio files
fileListFrame = Listbox(root,bg="aqua", fg="green", width=60)
fileListFrame.pack()
#box to print audioFile tag's
audioTagBox = Listbox(root,bg="white", fg="green", width=60)
audioTagBox.pack(pady=20)

# zmienna która przechowuje adres i nazwę pliku muzycznego
file='Alex2.mp3'
file3='fire.wav'

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
        self.player.play()
    
    def btn_pause(self): #def pauzy
        self.player.pause()
    
    def btn_stop(self): #def stopu
        self.player.stop()

#Audio files tag's
def music_tag(song_file):
    tag = TinyTag.get(file)
    print('Title: %s.' % tag.title)
    print('Author: %s.' % tag.artist)
    print('Album author: %s.' % tag.albumartist)
    print('Genre: %s.' % tag.genre)
    print('Time: %s.' % time.strftime('%H:%M:%S', time.gmtime(tag.duration)))

def songtime(song_file): #zwraca czas trwania utworu w sekundach
    tag = TinyTag.get(file)
    return tag.duration

audio =music_Player(file)

#create panel control button
controlFrame = Frame(root)
controlFrame.pack(pady= 10)

#button description
button_play = Button(controlFrame, text="Play", command=audio.btn_play)
button_pause = Button(controlFrame, text="Pause", command=audio.btn_pause)
button_stop = Button(controlFrame, text="Stop", command=audio.btn_stop)
button_prev = Button(controlFrame, text="<<")
button_next = Button(controlFrame, text=">>")

#button position
button_prev.grid(row=0, column=0)
button_stop.grid(row=0, column=1)
button_play.grid(row=0, column=2)
button_pause.grid(row=0, column=3)
button_next.grid(row=0, column=4)


root.mainloop()



music_tag(file)
