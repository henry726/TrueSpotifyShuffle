import tkinter as tk
import requests
import json
import random
from io import BytesIO
from PIL import Image, ImageTk

playlistnames = ["Liked Songs"]

#functions
def keysubmit():
    global key
    global headers
    global playlistnames
    global playlistlist
    global variable
    key = keyentry.get()
    headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + key,
    }
    playlistlist = []
    offset = -50
    while True:
        offset += 50
        params = {
            'limit': '50',
            'offset': str(offset),
        }
        playlistreq = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers, params=params)
        playlistreq = json.loads(playlistreq.text)
        for x in range(0, len(playlistreq["items"])):
            playlistnames.append(playlistreq["items"][x]["name"])
            playlistlist.append(playlistreq["items"][x]["uri"])
        if(len(playlistreq["items"]) != 50):
            break
    variable = tk.StringVar(gui)
    variable.set(playlistnames[0])
    plistdrop = tk.OptionMenu(gui, variable, *playlistnames)
    plistbutton = tk.Button(gui, text="Submit", command=plistchoose)
    plistdrop.grid(row=1, column=0)
    plistbutton.grid(row=1, column=1)
def plistchoose():
    try:
        index = playlistnames.index(variable.get())
        playsuf(index)
    except:
        playsuf(0)
def playsuf(index):
    global uris
    global songnames
    uris = []
    songnames = []
    offset = -50
    while True:
        offset += 50
        params = {
            'limit': '50',
            'offset': str(offset),
        }
        if(index == 0):
            topsongs = requests.get('https://api.spotify.com/v1/me/tracks', headers=headers, params=params)
            topsongs = json.loads(topsongs.text)
            for y in range(0, len(topsongs["items"])):
                uris.append(topsongs["items"][y]["track"]["uri"])
                songnames.append(topsongs["items"][y]["track"]["name"])
            if(len(topsongs["items"]) != 50):
                break
        else:
            topsongs = requests.get('https://api.spotify.com/v1/playlists/' + playlistlist[index-1].replace("spotify:playlist:",""), headers=headers)
            topsongs = json.loads(topsongs.text)
            for y in range(0, len(topsongs["tracks"]["items"])):
                uris.append(topsongs["tracks"]["items"][y]["track"]["uri"])
                songnames.append(topsongs["tracks"]["items"][y]["track"]["name"])
            if(len(topsongs["tracks"]["items"]) != 50):
                break
    temp = list(zip(uris, songnames))
    random.shuffle(temp)
    uris, songnames = zip(*temp)
    uris = list(uris)
    songnames = list(songnames)
    getimage()
def getimage():
    song = requests.get('https://api.spotify.com/v1/tracks/' + uris[0].replace("spotify:track:",""), headers=headers)
    song = json.loads(song.text)
    imageurl = song["album"]["images"][1]["url"]
    imageurl = requests.get(imageurl)
    imageurl = ImageTk.PhotoImage(Image.open(BytesIO(imageurl.content)))
    imagelabel.configure(image=imageurl)
    imagelabel.image = imageurl
    songname.configure(text=songnames[0])
def addsong():
    params = (
        ('uri', uris[0]),
    )
    response = requests.post('https://api.spotify.com/v1/me/player/queue', headers=headers, params=params)
    uris.pop(0)
    songnames.pop(0)
    getimage()
def nextsong():
    uris.pop(0)
    songnames.pop(0)
    getimage()
#gui
gui = tk.Tk()
keyentry = tk.Entry()
keybutton = tk.Button(gui, text="Submit", command=keysubmit)
addbutton = tk.Button(gui, text="Add Song", command=addsong)
nextbutton = tk.Button(gui, text="Next Song", command=nextsong)
imagelabel = tk.Label(gui)
songname = tk.Label(gui)
keyentry.grid(row=0, column=0)
keybutton.grid(row=0, column=1)
addbutton.grid(row=4, column=0)
nextbutton.grid(row=4, column=1)
imagelabel.grid(row=2, column=0)
songname.grid(row=3, column=0)
gui.mainloop()
