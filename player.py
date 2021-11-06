from tkinter.constants import ACTIVE, BOTH, BOTTOM, END, GROOVE, HORIZONTAL,  LEFT, RAISED,  VERTICAL, X
import tkinter as tk #module to create grapgic interface
from tkinter import ttk, filedialog, PhotoImage
import time
from tinytag import TinyTag
import pygame
from PIL import ImageTk, Image

# graphic 
root = tk.Tk()
root.title("Python Simple Player") # Title of window
root.geometry("500x480") #basic size of window

#root.iconbitmap('icon.ico') dont work for me 
img_icon = PhotoImage(file='icon.png')
root.tk.call('wm', 'iconphoto', root._w, img_icon)

#I want to this project static window that why i block resize
root.resizable(False, False)

global paused #global value for pausing of file 
paused = False 

bg = ImageTk.PhotoImage(Image.open('foto1.png').resize((500, 450), Image.ANTIALIAS))

#init pygame
pygame.mixer.init()

#Create master Frame
masterFrame = tk.Label(root, image=bg)
masterFrame.pack(anchor='center', fill=BOTH, expand=True)

#List of audio files
fileListFrame = tk.Listbox(masterFrame, bg="aqua", fg="green", width=60)
fileListFrame.grid(row=0, column=0, columnspan=2, padx=60, pady=20)

#button for AudioList
fileListButton = tk.Frame(masterFrame)
fileListButton.grid(row=1, column=0, columnspan=2)

#box to print audioFile tag's
audioTagBox = tk.Listbox(masterFrame, fg="green")
audioTagBox.grid(row=2, column=0, pady=20, padx=10)

volumeFrame = tk.LabelFrame(masterFrame, text="Volume")
volumeFrame.grid(row=2, column=1)

#create panel control button
controlFrame = tk.Frame(masterFrame)
controlFrame.grid(row=4, column=0, columnspan=2)

var = tk.StringVar()  #value of label audioTagBox
tagDefvalue = 'Title: ' + '\n' + 'Author: ' + '\n' + 'Album: ' +'\n' + 'Genre:' +'\n' + 'Time: ' 
var.set(tagDefvalue)

#tags print label
label_music_tag = tk.Label(master=audioTagBox, textvariable=var, relief=RAISED, justify=LEFT, width=45, anchor='w', bg='white')
label_music_tag.pack()

def btn_play(): #def play
    global paused
    paused = False
    song = fileListFrame.get(ACTIVE)
    var.set(music_tag(song))    
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0)
    #start option dont work for me, becouse of that i must use value 0 to set position on start
    position_slider.config(value = 0)
    #Print actual value of volume
    currentVolume = pygame.mixer.music.get_volume() * 100
    sliderLabel.config(text = "%.0f" % currentVolume)
    
    song_play_time()

def btn_pause(is_paused): #def pause
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
    position_slider.config(value = 0)
    status_bar.config(text = f"")
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
    position_slider.config(value = 0)   
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
    position_slider.config(value = 0)
    #move active bar in playlist
    fileListFrame.select_clear(0, END)
    fileListFrame.activate(next_file)
    fileListFrame.selection_set(next_file, last=None)

#Audio files tag's
def music_tag(song_file):
    tag = TinyTag.get(song_file)
    return 'Title:      %s.' % tag.title + '\n' + 'Author: %s.' % tag.artist +'\n' + \
        'Album: %s.' % tag.album +'\n' + 'Genre:  %s.' % tag.genre +'\n' + 'Time:    %s.' % time.strftime('%H:%M:%S', time.gmtime(tag.duration))

def song_time(song_file):
    tag = TinyTag.get(song_file)
    return tag.duration

def song_play_time():
    current_position = pygame.mixer.music.get_pos() / 1000
    #convert seconds to format hour:minute:second 
    converted_time = time.strftime('%H:%M:%S', time.gmtime(current_position))
    #grab and get current song file
    song = fileListFrame.get(ACTIVE)
    song_duration = time.strftime('%H:%M:%S', time.gmtime(song_time(song)))
    current_position += 1
    #status bar to stop on end of song
    if int(position_slider.get()) == int(song_time(song)):
        status_bar.config(text = f"Time Elapsed {song_duration} of {song_duration}.")

    elif int(position_slider.get()) == int(current_position):
        time_of_song = song_time(song)
        position_slider.config(to=int(time_of_song), value = int(current_position))
    
    #pause for status bar
    elif paused:
        pass
    
    else:
        time_of_song = song_time(song)
        position_slider.config(to=int(time_of_song), value = int(position_slider.get()))
        converted_time = time.strftime('%H:%M:%S', time.gmtime(int(position_slider.get())))
        #Output time to status bar
        status_bar.config(text = f"Time Elapsed {converted_time} of {song_duration}.")
        next_clock = int(position_slider.get()) + 1
        position_slider.config(value = next_clock)
    #update status bar 
    status_bar.after(1000, song_play_time)

def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose song", filetypes=(("mp3 Files", "*.mp3"), ))
    fileListFrame.insert(END, song)

def add_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose song", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        fileListFrame.insert(END, song)

def remove_song():
    fileListFrame.delete(ACTIVE)

def clear_fileList():
    fileListFrame.delete(0, END)

def volume(x):
    pygame.mixer.music.set_volume(volumeSlider.get())
    currentVolume = pygame.mixer.music.get_volume() * 100
    sliderLabel.config(text = "%.0f" % currentVolume)

def slide(x):
    song = fileListFrame.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0, start = int(position_slider.get()))
    
def save_tracklist():
    file = open("audio/tracklist.spp", "w")
    track_lenght = int(fileListFrame.index(END))

    for i in range(0, track_lenght, 1):
        file.write(fileListFrame.get(i) + '\n')
    file.close()

def save_tracklist_as():
    pass

def open_tracklist():
    #trackL contain file name, to read from file you need to open file
    trackL = filedialog.askopenfilename(initialdir='audio/', title="Choose tracklist", filetypes=(("tracklist", "*.spp"), ))
    with open(trackL) as file:
        for line in file:
            fileListFrame.insert(END, line.rstrip("\n")) # on end of line is enter, to play song you must remove him


#button description
button_play = tk.Button(controlFrame, text="Play", command=btn_play)
button_pause = tk.Button(controlFrame, text="Pause", command=lambda: btn_pause(paused))
button_stop = tk.Button(controlFrame, text="Stop", command=btn_stop)
button_prev = tk.Button(controlFrame, text="<<", command=btn_prev) 
button_next = tk.Button(controlFrame, text=">>", command=btn_next) 

button_add = tk.Button(fileListButton, text="+", command=add_songs)
button_remove = tk.Button(fileListButton, text="-", command=remove_song)
#button position
button_prev.grid(row=0, column=0)
button_stop.grid(row=0, column=1)
button_play.grid(row=0, column=2)
button_pause.grid(row=0, column=3)
button_next.grid(row=0, column=4)

#button position in fileListButton
button_add.grid(row=0, column=0)
button_remove.grid(row=0, column=1)

#create volume slider
volumeSlider = ttk.Scale(volumeFrame, from_=1, to=0, orient=VERTICAL, command=volume, length=45, value=1)
volumeSlider.pack()

#music position slider
position_slider = ttk.Scale(masterFrame,from_=0, to=100, orient=HORIZONTAL, value=0, command= slide, length=380)
position_slider.grid(row=3, column=0, columnspan=2)

#create volume value slider
sliderLabel = tk.Label(volumeFrame, text="100", anchor='center')
sliderLabel.pack(fill=X, side=BOTTOM, ipady=2)

status_bar = tk.Label(root, text='',border=1, relief=GROOVE)
status_bar.pack(anchor=tk.E)

#=================================================================================================================
#                  MENU PART
my_menu = tk.Menu(root)
root.config(menu=my_menu)

#file menu
file_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Open tracklist", command=open_tracklist)
file_menu.add_command(label = "Save tracklist", command = save_tracklist)
file_menu.add_command(label = "Save tracklist as", command = save_tracklist_as)
file_menu.add_command(label = "Exit", command=root.quit)

#add song menu
player_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label = "Add song", menu = player_menu)
player_menu.add_command(label = "Add one Song to Playlist", command = add_song)
player_menu.add_command(label = "Add many Songs to Playlist", command = add_songs)

#remove song menu
remove_menu = tk.Menu(my_menu, tearoff = 0)
my_menu.add_cascade(label = "Remove", menu = remove_menu)
remove_menu.add_command(label = "Remove Song", command = remove_song)
remove_menu.add_command(label = "Clear list of songs", command = clear_fileList)

root.mainloop()