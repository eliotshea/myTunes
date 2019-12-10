from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from pygame import mixer
import time
import threading
import mutagen
import pickle

root = Tk()
root.title("myTunes")
root.iconbitmap(r'icon.ico')

menuBar = Menu(root)
root.config(menu=menuBar)

songList = list(set(line.strip() for line in open('songs.txt')))
songNameList = list()
for item in songList:
    songNameList.append(item.split('/')[-1])


songNameDict = dict.fromkeys(songList, songNameList)

def browseFile():
    global filename, x
    filename = filedialog.askopenfilename()
    listBoxLabel.insert(x, filename.split('/')[-1])
    x += 1
    songList.append(filename)

def exitProgram():
    with open('songs.txt', 'w') as file:
        for item in set(songList):
            if item == '':
                continue
            else:
                file.write("%s\n" % item)
    mixer.music.stop()
    root.destroy()

subMenuFile = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=subMenuFile)
subMenuFile.add_command(label="Open file", command=browseFile)
subMenuFile.add_command(label="Exit", command=exitProgram)

def About():
    tkinter.messagebox.showinfo('About MyTunes', 'This MP3 Player was created by Eliot Shea for CIS4930 Python!\nThe youtube channel buildwithpython has a tutorial that was incredibly helpful!')

subMenuHelp = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=subMenuHelp)
subMenuHelp.add_command(label="About", command=About)

mixer.init()

fileLabel = Label(root, text='')
fileLabel.pack(pady=10)
lengthLabel = Label(root, text='Total Length- 00:00')
lengthLabel.pack(pady=10)
currentLabel = Label(root, text='Current Time- 00:00')
currentLabel.pack(pady=10)


paused = FALSE
playing = FALSE
def play_music():
    global paused
    global playing
    global filename
    if playing:
        if paused:
                mixer.music.unpause()
                paused = FALSE
                playButton['image'] = playPhoto
                statusBar['text'] = filename.split('/')[-1]
        else:
            mixer.music.pause()
            paused = TRUE
            playButton['image'] = pausePhoto
            statusBar['text'] = "PAUSED: " + filename.split('/')[-1]
    else:
        if listBoxLabel.curselection():
                filename = songList[int(listBoxLabel.curselection()[0])]
                mixer.music.load(filename)
                fileLabel['text'] = filename.split('/')[-1]
        mixer.music.play()
        playing = TRUE
        statusBar['text'] = filename.split('/')[-1]
        total_length = get_time()
        t1 = threading.Thread(target=start_count, args=(total_length,))
        t1.start()
        
def rewind_music():
    mixer.music.rewind()
    currentLabel['text'] = 'Current Length- 00:00'

def stop_music(): 
    global playing
    global filename
    mixer.music.stop()
    playing = FALSE
    statusBar['text'] = "Welcome to MyTunes"
    currentLabel['text'] = 'Current Length- 00:00'
    shortName = filename.split('/')[-1]
    fileLabel['text'] = "Stopped: " + shortName
    


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar['text'] = "PAUSED: " + filename.split('/')[-1]

def set_vol(val):
    volume = int(val)/ 100
    mixer.music.set_volume(volume)

muted = FALSE
def mute_music():
    global muted
    if muted:
        set_vol(70)
        muteButton['image'] = unmutePhoto
        volume.set(70)
        muted = FALSE
    else:
        set_vol(0)
        muteButton['image'] = mutePhoto
        volume.set(0)
        muted = TRUE

def get_time():
    audio = mutagen.File(filename)
    total_length = int(audio.info.length)
    return total_length

def show_details():
    shortName = filename.split('/')[-1]
    fileLabel['text'] = "Playing: " + shortName
    total_length = get_time()

    mins, secs = divmod(total_length, 60)
    time_format = '{:02d}:{:02d}'.format(round(mins), round(secs))
    lengthLabel['text'] = "Total Length- " + time_format
    
def start_count(t_time):
    t_count = int(t_time)
    while t_count and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod((t_time - t_count), 60)
            time_format = '{:02d}:{:02d}'.format(round(mins), round(secs))
            currentLabel['text'] = "Current Time- " + time_format
            time.sleep(1)
            t_count -= 1
        



playbackControls = Frame(root)
playbackControls.pack(side=TOP, padx= 40, pady = 10, fill=X, anchor=N) 

rewindPhoto = PhotoImage(file='rewind.png')
rewindButton = Button(playbackControls, image=rewindPhoto, command= rewind_music, relief=FLAT)
rewindButton.pack(side = LEFT)

playPhoto = PhotoImage(file='playButton.png')
pausePhoto = PhotoImage(file='pauseButton.png')
playButton = Button(playbackControls, image=playPhoto, command = play_music,relief=FLAT)
playButton.pack(side = LEFT)

stopPhoto = PhotoImage(file='stopButton.png')
stopButton = Button(playbackControls, image=stopPhoto, command = stop_music, relief=FLAT)
stopButton.pack(side = LEFT, padx= 10)

volume = Scale(playbackControls, from_=0, to = 100, orient=HORIZONTAL, command = set_vol)
volume.set(70)
mixer.music.set_volume(0.7)
volume.pack(side = LEFT)

mutePhoto = PhotoImage(file='mute.png')
unmutePhoto = PhotoImage(file='volume.png')
muteButton = Button(playbackControls, image=unmutePhoto, command=mute_music, relief=FLAT)
muteButton.pack(side=LEFT)

listBoxLabel = Listbox(root, width=40)
x = 0
for item in songNameList:
    listBoxLabel.insert(x, item)
    x += 1
listBoxLabel.pack()

statusBar = Label(root, text="Welcome to MyTunes", relief=SUNKEN, anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

root.protocol("WM_DELETE_WINDOW", exitProgram)
root.mainloop()