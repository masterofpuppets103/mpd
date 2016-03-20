import tkinter as tk
from tkinter import *
from tkinter import messagebox ##messageboxes
import musicpd #http://www.musicpd.org/doc/protocol/
import paramiko
from paramiko import * #for ssh

##managing the connection:
class connectobject(object):
	def __init__(self, arg1, arg2, arg3):##initialization. takes URL, port and username for ssh
		self.arg1 = arg1 
		self.arg2 = arg2
		self.arg3 = arg3
	def connect(self):##connects to server
		try:
			client.connect(self.arg1, self.arg2) 
		except musicpd.ConnectionError:
			pass
	def print(self):
		result = "Server: " + self.arg1 + "\n Port: " + str(self.arg2) + "\nUsername: " + str(self.arg3)##save info to string and give it back
		return(result)
	def disconnect(self):#disconnect from server
		try:
			client.close()		  # send the close command
			client.disconnect()
		except musicpd.ConnectionError: #if it is not connected, do nothing. prevents the whole thing from shutting down
			pass
	def change(self, arg1, arg2, arg3):#changes the IP and Port
		self.arg1 = arg1
		self.arg2 = arg2
		self.arg3 = arg3
	def safe(self):####save actual configuration to config-file
		configfile = open("config.txt", 'w') ##open in read-mode then delete the contents and write down Server and IP
		configfile.truncate()
		textstring = connectinfo.arg1
		userstring = connectinfo.arg3
		portconfig = str(connectinfo.arg2)
		configfile.write(portconfig)
		configfile.write("\n")
		configfile.write(textstring)
		configfile.write("\n")
		configfile.write(userstring)
		configfile.close()	
		master.quit()##exits program
	def getip(self): #gives back IP
		result = self.arg1
		return result
	def getport(self): #gives back Port
		result = int(self.arg2)
		return result
	def getuser(self): #gives back User
		result = self.arg3
		return result
	

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


def drawscrollbar():##shows actual playlist  (currently not updating, so you have to re-open it all the time)
	master2 = tk.Tk()
	b1 = Button(master2,text="Play Track",command=playselectedtitle).pack()
	b2 = Button(master2,text="Remove Track",command=deleteselectedtitle).pack()
	connectinfo.connect()
	scrollbar = Scrollbar(master2)
	scrollbar.pack(side=RIGHT, fill=Y)
	global listbox2
	listbox2 = Listbox(master2, yscrollcommand=scrollbar.set)
	text = drawplaylist()
	master2.title(text)
	listbox2.pack(side=LEFT, fill=BOTH, expand=50)
	scrollbar.config(command=listbox2.yview)
	connectinfo.disconnect()
	
def drawplaylist(): #draws playlist to update the view.
	secondstotal = 0
	i=0
	connectinfo.connect()
	for song in client.playlistinfo():
		secondstotal = float(song['time']) + secondstotal
		songtime = secondstominutes(float(song['time']))
		text9 = song['pos'] +  " " +  song['artist'] + " - " + song['title'] +" " + songtime
		listbox2.insert(END, text9) 
		i+=1   
	totaltime = secondstominutes(secondstotal)
	text = "Actual Playlist | Total time: " + totaltime + " | " + str(i) + " Songs"
	connectinfo.disconnect()
	return text

def playselectedtitle():##plays selected sond of the playlist
    tracknumber = min(listbox2.curselection()) 
    connectinfo.connect()
    client.play(tracknumber)
    connectinfo.disconnect()

def deleteselectedtitle():##removes selected track from playlist (not properly working)
    tracknumber = min(listbox2.curselection()) 
    connectinfo.connect()
    #client.deleteid(tracknumber)
    client.delete(tracknumber)
    #print(tracknumber)
    #test() --> should call function drawplaylist, to update the playlist, but not working
    connectinfo.disconnect()

def drawallplaylists():##list all playlists
	connectinfo.connect()
	master3 = tk.Tk()
	master3.title("Playlist overview")
	master3.minsize(width=50, height=300) #makes that the window is not shown too small, but not a very nice solution
	b1 = Button(master3,text="Add playlist",command=addEntry).pack(side = LEFT)
	scrollbar = Scrollbar(master3)
	scrollbar.pack(side=RIGHT, fill=Y)
	global listbox
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
	

def addEntry():##adds selected playlist to the playlist
    playlistnumber = min(listbox.curselection())   ##get selection of listbox
    connectinfo.connect()    
    i = 0
    j = []
    for song in client.listplaylists():
        j.append(song['playlist'])#creating an array so you can access the name of the playlist. Needed because otherwise you get an error
        i+=1
	#add playlist by number:
    client.load(j[playlistnumber])#call this entry in the list and load the playlist
    connectinfo.disconnect()


def displaysong(label):##shows the actual song, time played and so on. updates every second
	def display():
		connectinfo.connect()
		try:
			timeplayed = secondstominutes(float(client.status()['elapsed']))
			timesong = secondstominutes(float(client.currentsong()['time']))
			text = client.currentsong()['artist'] + " - " + client.currentsong()['title'] + " | " + timeplayed + "/" + timesong + "\n" + "Album: " + client.currentsong()['album'] + " | Songnumber: " + client.status()['song'] +  "\n" + client.status()['state'] +    " " + "random: " + client.status()['random'] + " | repeat: " + client.status()['repeat'] + " \n" +"consume: " + client.status()['consume'] + " | single: " + client.status()['single']
		except KeyError: ##if no songs are loaded in the playlist, it will produce a key error. If this occurs, it says no song playing
			text = "no song playing"			
		except musicpd.ConnectionError:
			text = "not connected or wrong IP/Port"
		label.config(text=text, justify=LEFT)
		label.after(1000, display)
		connectinfo.disconnect()
	display()

def about(): ##draw window 'about'
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

class playattributes():##bundles all functions for playing like random, single, consume, repeat and clearplaylist
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
	
	def clearplaylist(): #clear the playlist
	    connectinfo.connect()
	    client.clear()
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



####window 'add'
def addurl():##adds an URL (currently only mp3/ogg-streams, no youtube). Youtube-code: "yt:https://www.youtube.com/watch?v=N9nUIFYc5II" but also on server not working :(
    connectinfo.connect()
    url = e3.get()
    try:
        client.add(url)
    except musicpd.CommandError:
        messagebox.showwarning("Error", "Please enter a playable URL")
    connectinfo.disconnect()
    e3.delete(0,END)


def addstuff():##main window for adding URLs, Playlist and play a tracknumber (not very nice grouped)
	master4 = tk.Tk()
	master4.title("Adding")
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

####class for setting up the server
class serversetup():
	def serversetupwindow():#window for serversetup
		serversetupwin = tk.Tk()
		serversetupwin.title("Set up IP and Port")
		label = tk.Label(serversetupwin, text="IP:",justify = LEFT)
		label.grid(row = 0, column= 0)
		label = tk.Label(serversetupwin, text="Port:",justify = LEFT)
		label.grid(row = 1, column= 0)
		label = tk.Label(serversetupwin, text="Username:",justify = LEFT)
		label.grid(row = 2, column= 0)
		global e7
		e7= Entry(serversetupwin)
		e7.grid(row = 0, column= 1)
		global e8
		e8= Entry(serversetupwin)
		e8.grid(row = 1, column= 1)
		global e20
		e20= Entry(serversetupwin)
		e20.grid(row = 2, column= 1)		
		Button(serversetupwin, text='Update IP and Port', command=serversetup.serversetupbutton).grid(row = 3, column= 1)

	def serversetupbutton():#changes connection info based on input at serversetup
		ip = e7.get()
		port = int(e8.get())
		user = e20.get()
		connectinfo.change(ip, port,user)
		e7.delete(0,END)
		e8.delete(0,END)
		e20.delete(0,END)
	
##class that connects to the server via ssh and can shut down the server
class shutdown():
	def sshshutdown():
		sshclient = SSHClient() ##init sshclient
		sshclient.load_system_host_keys()
		password = sshpasswordinput.get()
		try:
			sshclient.connect(connectinfo.getip(), username = connectinfo.getuser(), password = password) 
			time = sshtimeinput.get()
			command = 'sudo shutdown -hP ' + time #shutdown with given time
			sshclient.exec_command(command)
			sshclient.close()
		except paramiko.ssh_exception.AuthenticationException:
			messagebox.showwarning("Error", "Wrong username or password")
		sshpasswordinput.delete(0,END) #delete field with password
		sshtimeinput.delete(0,END) #delete field with time

	def mainwindow(): #main window, you have to provide the time and the passoword for the server
		shutdownwindow = tk.Tk()
		shutdownwindow.title("MPC Shutdown")#title
		shutdownwindow.minsize(width=150, height=100)##minimum size
		label = tk.Label(shutdownwindow, justify = LEFT, text="Enter Passwort")
		label.grid(column=0, row= 0)
		label2 = tk.Label(shutdownwindow, justify = LEFT, text="Enter Time ")
		label2.grid(column=0, row= 1)
		global sshpasswordinput
		sshpasswordinput= Entry(shutdownwindow, show="*")##make password invisible, input field for password
		sshpasswordinput.grid(row = 0, column= 1)
		global sshtimeinput
		sshtimeinput= Entry(shutdownwindow)#entry-field for time
		sshtimeinput.grid(row = 1, column= 1)
		button1 = tk.Button(shutdownwindow, text='Shutdown', width=10, command=shutdown.sshshutdown)
		button1.grid(column=1, row= 2)	
	
	
####setting up connection
try:
	with open('config.txt') as f:#open file
		lines = f.readlines()
	IP = lines[1]#IP is line number 2
	IP = IP[:-1]#get rid of linbreak after ip
	USER = lines[2]#USER is line number 3
	PORT = int(lines[0]) #Port is line number 1
	f.close()
except FileNotFoundError:#if it cannot find the file, set IP and Port to a random value so program starts and user can change it
	IP = '192.168.1.2'
	PORT = 6600
	USER = 'root'
except ValueError:#if file is corrupted, set IP and Port to a random value so program starts and user can change it
	IP = '192.168.1.2'
	PORT = 6600
	USER = 'root'
except IndexError:#if file is corrupted, set IP and Port to a random value so program starts and user can change it
	IP = '192.168.1.2'
	PORT = 6600
	USER = 'root'

client = musicpd.MPDClient()#set up basic object for MPD-Client
connectinfo = connectobject(IP, PORT, USER)#set object with connection settings


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
menu.add_cascade(label="Playback modes", menu=newmenu)
newmenu.add_command(label="Clear Playlist", command=playattributes.clearplaylist)
newmenu.add_command(label="Toggle Random", command=playattributes.random)
newmenu.add_command(label="Toggle Repeat", command=playattributes.repeat)
newmenu.add_command(label="Toggle consume", command=playattributes.consume)
newmenu.add_command(label="Toggle single", command=playattributes.single)

menu3 = Menu(master)
master.config(menu=menu)
newmenu = Menu(menu3)
menu.add_cascade(label="About/setup", menu=newmenu)
newmenu.add_command(label="Set up Server", command=serversetup.serversetupwindow)
newmenu.add_command(label="About", command=about)
newmenu.add_command(label="Shutdown", command=shutdown.mainwindow)

##############
master.protocol("WM_DELETE_WINDOW", connectinfo.safe)
mainloop()
