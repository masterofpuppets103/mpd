import tkinter as tk
from tkinter import *
import musicpd #http://www.musicpd.org/doc/protocol/
#from messagebox import *
client = musicpd.MPDClient()


def connect():##connect to server
	try:
		client.connect('192.168.1.102', 6600) #ip and port (could also be done via config-file)
	except musicpd.ConnectionError:
		print("No Route to Server")
		print("Please check if IP is right and Server is up")
		print("Exiting")
		sys.exit()##exists in a not-very-nice message and not clean :(

	
def disconnect(): ##disconnect from server
	client.close()		  # send the close command
	client.disconnect()	

def secondstominutes(secondsinput):##converts seconds to minutes
	if (secondsinput > 3600): ##write playlist in hours, if it is longer than one hour
		hours = int(secondsinput/3600)
		minutes = round(int(secondsinput % 3600)/60)
		seconds = round(minutes % 60)
		returnstring = str(hours)  + ":" + str(minutes) + ":" + str(seconds)
	else:
		seconds = round(secondsinput % 60)
		minutes = int(secondsinput /60)
		returnstring = str(minutes) + ":" + str(seconds)
	return(returnstring)


def drawscrollbar():
	master2 = tk.Tk()
	master2.Title = ("MPC Control")
	connect()
	scrollbar = Scrollbar(master2)
	scrollbar.pack(side=RIGHT, fill=Y)
	listbox = Listbox(master2, yscrollcommand=scrollbar.set)
	for song in client.playlistinfo():
		text9 = song['pos'] +  " " +  song['artist'] + " - " + song['title'] #+" " + songtime
		listbox.insert(END, text9)    
	listbox.pack(side=LEFT, fill=BOTH, expand=50)
	scrollbar.config(command=listbox.yview)
	disconnect()

def drawallplaylists():##list all playlists
	connect()
	master3 = tk.Tk()
	master3.Title = ("MPC Control")
	scrollbar = Scrollbar(master3)
	scrollbar.pack(side=RIGHT, fill=Y)
	listbox = Listbox(master3, yscrollcommand=scrollbar.set)	
	client.iterate = True
	i = 0
	for song in client.listplaylists():
		text9 = str(i) + " "+  song['playlist']
		i = i+1
		listbox.insert(END, text9)    
	listbox.pack(side=LEFT, fill=BOTH, expand=50)
	scrollbar.config(command=listbox.yview)
	disconnect()
		

def setpause():
    connect()
    client.pause()
    disconnect()

def playnext(): ##play next track
    connect()
    client.next()
    disconnect()


def random():#toggle random
    connect()
    if (client.status()['random'] == "1"):
        client.random(0)
    else:
        client.random(1)
    disconnect()
		
def repeat():#toggle repeat
    connect()
    if (client.status()['repeat'] == "1"):
        client.repeat(0)
    else:
        client.repeat(1)
    disconnect()
	
def playlast():##start current track again or play song before if actual song runs less than 10 seconds
    connect()    
    tracknumber = float(client.status()['song'])
    tracknumber = int(tracknumber)	
    if (float(client.status()['elapsed'])<10):
        tracknumber = tracknumber -1
    else:
        pass	
    client.play(tracknumber)
    disconnect()

def displaysong(label):
	def display():
		connect()
		try:
			timeplayed = secondstominutes(float(client.status()['elapsed']))
			timesong = secondstominutes(float(client.currentsong()['time']))
			text = client.currentsong()['artist'] + " - " + client.currentsong()['title'] + " | " + timeplayed + "/" + timesong + "\n" + "Album: " + client.currentsong()['album'] + " | Songnumber: " + client.status()['song'] +  "\n" + client.status()['state'] +    " " + "random: " + client.status()['random'] + " | repeat: " + client.status()['repeat']
			label.config(text=text)
		except KeyError: ##if no songs are loaded in the playlist, it will produce a key error. If this occurs, it says no song playing
			text1 = "no song playing"
			label.config(text=text1)
		#drawstrings(text1, 10,10, DARKRED, BASICFONT
		label.after(1000, display)
		disconnect()
	display()

def addplaylist(): ##the not-so-nice way: shows text in shell. Could be moved to a graphical view
    playlistnumber = int(float(e1.get()))    
    connect()    
    i = 0
    j = []
    for song in client.listplaylists():
        j.append(song['playlist'])#creating an array so you can access the name of the playlist. Needed because otherwise you get an error
        i+=1
	#add playlist by number:
    #playlistnumber = int(input("Please enter the number of playlist to add: ") )
    client.load(j[playlistnumber])#call this entry in the list and load the playlist
    #print("Playlist " + j[playlistnumber]+ " added")
    disconnect()
    e1.delete(0,END) #deletes input of the field

def addurl():
    connect()
	#print("Please insert URL")
    url = e3.get()
    try:
        client.add(url)
    except musicpd.CommandError:
        print ("Please enter a playable URL")
    disconnect()
    e3.delete(0,END)
 #local tracks: 'local:track:USB/Musik/Ko%3Fn/Untouchables/02%20Make%20Believe.mp3'
	#spotify: 'spotify:track:5m88DsBQPIfXps1FomdwqA'

def playtitle():##play given number on the playlist
    connect()
    playtitleloop = True
    while playtitleloop:
        try:
            number = int(float(e2.get())) 
            if (number < 0):# | (number >10):
                print("Please insert a positive number")
            else:
                client.play(number)
                playtitleloop = False
        except ValueError:
            print ("Please enter a number")
    disconnect()
    e2.delete(0,END)
	
master = tk.Tk()
master.Title = ("MPC Control")

label = tk.Label(master, fg="dark green")
label.pack()
displaysong(label)



button = tk.Button(master, text='<<', width=5, command=playlast)
button.pack(padx=5, pady=10, side=LEFT)
button = tk.Button(master, text='||', width=5, command=setpause)
button.pack(padx=5, pady=20, side=LEFT)
button = tk.Button(master, text='>>', width=5, command=playnext)
button.pack(padx=5, pady=30, side=LEFT)

e1 = Entry(master)
e1.pack()
Button(master, text='Add Playlist', command=addplaylist).pack()

e2 = Entry(master)
e2.pack()
Button(master, text='Play track', command=playtitle).pack()

e3 = Entry(master)
e3.pack()
Button(master, text='Add URL', command=addurl).pack()

#Button(text='Quit', command=callback).pack(fill=X)
#w = Label(master, text="Actual Playlist:")
#w.pack(padx=10, pady=25, side=LEFT)
#drawscrollbar()

####Menu
menu = Menu(master)
master.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Playlist", command=drawscrollbar)
filemenu.add_command(label="All playlists", command=drawallplaylists)
#filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)

mainloop()
