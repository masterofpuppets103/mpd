import tkinter as tk
from tkinter import *
import musicpd #http://www.musicpd.org/doc/protocol/

##managing the connection:
class connectobject(object):
	def __init__(self, arg1, arg2):
		self.arg1 = arg1 
		self.arg2 = arg2
	def connect(self):
		try:
			client.connect(self.arg1, self.arg2) #ip and port (could also be done via config-file)
		except musicpd.ConnectionError:
			pass
			#print("No Route to Server")
			#print("Please check if IP is right and Server is up")
			#print("Exiting")
			#sys.exit()
	def print(self):
		result = "Server: " + self.arg1 + "\n Port: " + str(self.arg2) ##save info to string and give it back
		return(result)
	def disconnect(self):
		try:
			client.close()		  # send the close command
			client.disconnect()
		except musicpd.ConnectionError:
			pass
	def change(self, arg1, arg2):
		self.arg1 = arg1
		self.arg2 = arg2
	def safe(self):####not done yet :(
		configfile = open("config.txt", 'w') ##open in read-mode then delete the contents and write down Server and IP
		configfile.truncate()
		textstring = connectinfo.arg1
		portconfig = str(connectinfo.arg2)
		configfile.write(textstring)
		configfile.write("\n")
		configfile.write(portconfig)
		configfile.close()	
		master.quit()##exits program
	

####draw some windows
def secondstominutes(secondsinput):##converts seconds to minutes
	if (secondsinput > 3600): ##write playlist in hours, if it is longer than one hour
		hours = int(secondsinput/3600)
		minutes = round(int(secondsinput % 3600)/60)
		seconds = round(minutes % 60)
		returnstring = str(hours)  + ":" + str(minutes) + ":" + str(seconds)
	else:#write playlist in minutes, if it is shorter than an hour
		seconds = round(secondsinput % 60)
		minutes = int(secondsinput /60)
		returnstring = str(minutes) + ":" + str(seconds)
	return(returnstring)


def drawscrollbar():
	master2 = tk.Tk()
	connectinfo.connect()
	scrollbar = Scrollbar(master2)
	scrollbar.pack(side=RIGHT, fill=Y)
	listbox = Listbox(master2, yscrollcommand=scrollbar.set)
	secondstotal = 0
	i=0
	for song in client.playlistinfo():
		secondstotal = float(song['time']) + secondstotal
		songtime = secondstominutes(float(song['time']))
		text9 = song['pos'] +  " " +  song['artist'] + " - " + song['title'] +" " + songtime
		listbox.insert(END, text9) 
		i+=1   
	totaltime = secondstominutes(secondstotal)
	text = "Actual Playlist | Total time: " + totaltime + " | " + str(i) + " Songs"
	master2.title(text)
	listbox.pack(side=LEFT, fill=BOTH, expand=50)
	scrollbar.config(command=listbox.yview)
	connectinfo.disconnect()

def drawallplaylists():##list all playlists
	connectinfo.connect()
	master3 = tk.Tk()
	master3.title("Playlist overview")
	master3.minsize(width=50, height=300) #makes that the window is not shown too small, but not a very nice solution
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
	connectinfo.disconnect()

def displaysong(label):
	def display():
		connectinfo.connect()
		try:
			timeplayed = secondstominutes(float(client.status()['elapsed']))
			timesong = secondstominutes(float(client.currentsong()['time']))
			text = client.currentsong()['artist'] + " - " + client.currentsong()['title'] + " | " + timeplayed + "/" + timesong + "\n" + "Album: " + client.currentsong()['album'] + " | Songnumber: " + client.status()['song'] +  "\n" + client.status()['state'] +    " " + "random: " + client.status()['random'] + " | repeat: " + client.status()['repeat'] + " \n consume: " + client.status()['consume'] + " | single: " + client.status()['single']
		except KeyError: ##if no songs are loaded in the playlist, it will produce a key error. If this occurs, it says no song playing
			text = "no song playing"			
		except musicpd.ConnectionError:
			text = "not connected or wrong IP/Port"
		label.config(text=text, justify=LEFT)
		label.after(1000, display)
		connectinfo.disconnect()
	display()

def about():
	master5 = tk.Tk()
	master5.title('About')
	label = tk.Label(master5)
	text =  "This program was written by Julian Hocker, licenced under the GPL"
	text = text + "\n" + connectinfo.print()
	label.config(text =text)
	label.grid()
#############manipulate playback
def setpause():
    connectinfo.connect()
    client.pause()
    connectinfo.disconnect()

def playnext(): ##play next track
    connectinfo.connect()
    client.next()
    connectinfo.disconnect()

class playattributes():
	def random():#toggle random
		connectinfo.connect()
		if (client.status()['random'] == "1"):
			client.random(0)
		else:
			client.random(1)
		connectinfo.disconnect()
	
	def single():#toggle single (only current song is played until the end)
		connectinfo.connect()
		if (client.status()['single'] == "1"):
			client.single(0)
		else:
			client.single(1)
		connectinfo.disconnect()
		
	def consume():#toggle consume (each played song is removed from playlist)
		connectinfo.connect()
		if (client.status()['consume'] == "1"):
			client.consume(0)
		else:
			client.consume(1)
		connectinfo.disconnect()
		
	def repeat():#toggle repeat
		connectinfo.connect()
		if (client.status()['repeat'] == "1"):
			client.repeat(0)
		else:
			client.repeat(1)
		connectinfo.disconnect()
	
def playlast():##start current track again or play song before if actual song runs less than 10 seconds
    connectinfo.connect()    
    tracknumber = float(client.status()['song'])
    tracknumber = int(tracknumber)	
    if (float(client.status()['elapsed'])<10):
        tracknumber = tracknumber -1
    else:
        pass	
    client.play(tracknumber)
    connectinfo.disconnect()

def clearplaylist(): #clear the playlist
	connectinfo.connect()
	client.clear()
	connectinfo.disconnect()

####window 'add'
def addplaylist(): ##the not-so-nice way: shows text in shell. Could be moved to a graphical view
    playlistnumber = int(float(e1.get()))    
    connectinfo.connect()    
    i = 0
    j = []
    for song in client.listplaylists():
        j.append(song['playlist'])#creating an array so you can access the name of the playlist. Needed because otherwise you get an error
        i+=1
	#add playlist by number:
    client.load(j[playlistnumber])#call this entry in the list and load the playlist
    connectinfo.disconnect()
    e1.delete(0,END) #deletes input of the field

def addurl():##adds an URL (currently only mp3/ogg-streams, no youtube)
    connectinfo.connect()
    url = e3.get()
    try:
        client.add(url)
    except musicpd.CommandError:
        print ("Please enter a playable URL")
    connectinfo.disconnect()
    e3.delete(0,END)

def playtitle():##play given number on the playlist
    connectinfo.connect()
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
    connectinfo.disconnect()
    e2.delete(0,END)

def addstuff():##main window for adding URLs, Playlist and play a tracknumber (not very nice grouped)
	master4 = tk.Tk()
	master4.title("Adding")
	##Adding a Playlist
	global e1 
	e1= Entry(master4)
	e1.grid(row=0, column=0)
	Button(master4, text='Add Playlist', command=addplaylist).grid(row=0, column=1)
	##Play track number
	global e2 
	e2 = Entry(master4)
	e2.grid(row=1, column=0)
	Button(master4, text='Play track', command=playtitle).grid(row=1, column=1)
	##Add an URL
	global e3 
	e3= Entry(master4)
	e3.grid(row=2, column=0)
	Button(master4, text='Add URL', command=addurl).grid(row=2, column=1)
	
def addlocal():##main window for adding an album on the local hard disc
	master5 = tk.Tk()
	master5.title("Adding")
	label = tk.Label(master5, text="Artist:",justify = LEFT)
	label.grid(row = 0, column= 0)
	global e5
	e5= Entry(master5)
	e5.grid(row = 0, column= 1)
	global e6
	e6= Entry(master5)
	e6.grid(row = 1, column= 1)
	label = tk.Label(master5, text="Album:",justify = LEFT)
	label.grid(row = 1, column= 0)
	Button(master5, text='Add Album', command=addlocalfiles).grid(row = 2, column= 0)
	Button(master5, text='Show Albums of Artist', command=showalbums).grid(row = 2, column= 1)
	global labellocalartists
	labellocalartists = tk.Label(master5, justify = LEFT)
	labellocalartists.grid(row = 0, column= 3, rowspan = 3)


def addlocalfiles():#adds album according to artist and album name
	artist = e5.get()
	album = e6.get()	
	input = "Local media/Artists/" + artist + "/" + album
	connectinfo.connect()
	for song in client.lsinfo(input):
		text10 = song['file']
		client.add(text10)
	connectinfo.disconnect()
	e5.delete(0,END)
	e6.delete(0,END)

def showalbums():
	input = "Local media/Artists/" + e5.get()
	stringlength = len(input) +1
	text9 = ""
	connectinfo.connect()
	for song in client.lsinfo(input):
		text9 = text9  + song['directory'][stringlength:] + "\n"
	labellocalartists.config(text=text9)
	connectinfo.disconnect()
	
	
def serversetup():
	master6 = tk.Tk()
	master6.title("Adding")
	label = tk.Label(master6, text="IP:",justify = LEFT)
	label.grid(row = 0, column= 0)
	global e7
	e7= Entry(master6)
	e7.grid(row = 0, column= 1)
	global e8
	e8= Entry(master6)
	e8.grid(row = 1, column= 1)
	label = tk.Label(master6, text="Port:",justify = LEFT)
	label.grid(row = 1, column= 0)
	Button(master6, text='Update IP and Port', command=serversetupbutton).grid(row = 2, column= 1)

def serversetupbutton():#adds album according to artist and album name
	ip = e7.get()
	port = int(e8.get())
	connectinfo.change(ip, port)
	e7.delete(0,END)
	e8.delete(0,END)
	
####setting up connection
try:
	with open('config.txt') as f:
		lines = f.readlines()
	IP = lines[0]#IP is line number 2
	PORT = int(lines[1]) #Port is line number 3
	f.close()
except FileNotFoundError:#if it cannot find the file, set IP and Port to a random value so program starts and user can change it
	IP = '192.168.1.2'
	PORT = 6600
except ValueError:#if file is corrupted, set IP and Port to a random value so program starts and user can change it
	IP = '192.168.1.2'
	PORT = 6600
except IndexError:#if file is corrupted, set IP and Port to a random value so program starts and user can change it
	IP = '192.168.1.2'
	PORT = 6600

client = musicpd.MPDClient()
connectinfo = connectobject(IP, PORT)

#####################
##########main window
master = tk.Tk()
master.title("MPC Control")#title
master.minsize(width=150, height=100)##minimum size

label = tk.Label(master, justify = LEFT)
label.grid(column=0, row= 0, columnspan = 3)
displaysong(label)##label for actual song

#buttons for controlling the playback
button1 = tk.Button(master, text='<<', width=10, command=playlast)
button1.grid(column=0, row= 1)
button2 = tk.Button(master, text='||', width=10, command=setpause)
button2.grid(column=1, row= 1)
button3 = tk.Button(master, text='>>', width=10, command=playnext)
button3.grid(column=2, row= 1)

####Menu
menu = Menu(master)
master.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Playlist", command=drawscrollbar)
filemenu.add_command(label="All playlists", command=drawallplaylists)
filemenu.add_command(label="Add", command=addstuff)
filemenu.add_command(label="Add Local files", command=addlocal)
filemenu.add_command(label="Exit", command=connectinfo.safe) ###should save the actual server configuration to file and read it when it starts

menu2 = Menu(master)
master.config(menu=menu)
newmenu = Menu(menu2)
menu.add_cascade(label="About", menu=newmenu)
newmenu.add_command(label="Clear Playlist", command=clearplaylist)
newmenu.add_command(label="Toggle Random", command=playattributes.random)
newmenu.add_command(label="Toggle Repeat", command=playattributes.repeat)
newmenu.add_command(label="Toggle consume", command=playattributes.consume)
newmenu.add_command(label="Toggle single", command=playattributes.single)
newmenu.add_command(label="Set up Server", command=serversetup)
newmenu.add_command(label="About", command=about)

##############
mainloop()
