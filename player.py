import vlc #obsługa plików muzycznych
import time #potrzebna funkcja sleep
from tinytag import TinyTag, TinyTagException#biblioteka do odczytywania tagów -> autor, czas trwania, itp.
from tkinter import * #moduł do tworzenia interfejsu graficznego

# obsługa grafiki
root = Tk()
root.title("Python Simple Playerf")
root.geometry()
#Creating a Label Wiget
#myLabel = Label(root, text="hello world")
#Showing label on screen
#myLabel.pack()

# obsługa muzyki
file='Alex2.mp3'
file3='fire.wav'
#player puszcza muzykę ale potrzebny jest sleep, długość sleepa oznacza przez jaki czas będzie grany plik, 
#potrzebne wyciągnięcie ile trwa plik !!!
def musicPlayer():
    player = vlc.MediaPlayer(file)
    return player.play()

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


myButton = Button(root, text="Play", command=musicPlayer)
myButton1 = Button(root, text="Pause")
myButton.grid(row=0, column=0)
myButton1.grid(row=0, column=1)
root.mainloop()



music_tag(file)
#player.play()
#time.sleep(songtime(file))

