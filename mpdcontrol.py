#!/usr/bin/python3
import musicpd #http://www.musicpd.org/doc/protocol/
import time
import pygame  # See http://www.pygame.org/docs
from pygame.locals import *
from sense_hat import SenseHat #http://pythonhosted.org/sense-hat/api/
from evdev import InputDevice, list_devices, ecodes #input for sensehat joystick
import sys


###############
####functions:
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

#############Server
def connect():##connect to server
	try:
		client.connect(IP, PORT) #ip and port (could also be done via config-file)
	except musicpd.ConnectionError:
		print("No Route to Server")
		print("Please check if IP is right and Server is up")
		print("Exiting")
		sys.exit()##exists in a not-very-nice message and not clean :(

	
def disconnect(): ##disconnect from server
	client.close()		  # send the close command
	client.disconnect()		# disconnect from the server
	
def pause(): ##pause playing
	client.pause()

###########output
def drawstrings(stringtext, x, y, outputcolor, font):
	scoreSurf = font.render(stringtext, True, outputcolor)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (x, y)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawplaylist():##show actual playlist
	client.iterate = True
	secondstotal = 0
	i = 0
	try:
		songnumber = client.status()['song']
	except KeyError: ##if no songs are loaded in the playlist, it will produce a key error. If this occurs, it says no song playing
		songnumber = 0
	
	for song in client.playlistinfo():
		secondstotal = float(song['time']) + secondstotal
		if (i<57):##prints only the first x results. Could be done nice, for instance one could check if there is space left on the screen
			songtime = secondstominutes(float(song['time']))
			text9 = song['pos'] +  " " +  song['artist'] + " - " + song['title'] +" " + songtime
			w = 70+ i*15
			#print (song['title'])
			if (songnumber == song['pos']):
				drawstrings(text9, 50, w, DARKBLUE, PLAYLISTFONT)
			else:
				drawstrings(text9, 50, w, DARKGRAY, PLAYLISTFONT)
		else:
			pass
		i = i+1
	totaltime = secondstominutes(secondstotal)
	text = "Total time: " + totaltime + " | " + str(i) + " Songs"
	drawstrings(text, 10, height-80, DARKGREEN, BASICFONT)
	
	
def drawoneplaylist():##show actual playlist
	client.iterate = True
	i = 0
	secondstotal = 0
	text10 = "Playlist: " + playlistname
	drawstrings(text10, 50, 70, DARKBLUE, PLAYLISTFONT)
	for song in client.listplaylistinfo(playlistname):
		secondstotal = float(song['time']) + secondstotal
		if (i<56):
			songtime = secondstominutes(float(song['time']))
			text9 = str(i) +  " " +  song['albumartist'] + " - " + song['title'] +" " + songtime
			w = 85+ i*15
			drawstrings(text9, 50, w, DARKGRAY, PLAYLISTFONT)
		else:
			pass
		i = i+1
	totaltime = secondstominutes(secondstotal)
	text = "Total time: " + totaltime + " | " + str(i) + " Songs"
	drawstrings(text, 10, height-80, DARKGREEN, BASICFONT)

def drawallplaylists():##list all playlists
	client.iterate = True
	i = 0
	for song in client.listplaylists():
		if (i<57):
			text9 = str(i) + " "+  song['playlist']
			w = 70+ i*15
			drawstrings(text9, 50, w, DARKGRAY, PLAYLISTFONT)
		else:
			pass
		i = i+1

def drawsong():#prints current info of the song and so on to the screen
	try:
		timeplayed = secondstominutes(float(client.status()['elapsed']))
		timesong = secondstominutes(float(client.currentsong()['time']))
		text = client.currentsong()['artist'] + " - " + client.currentsong()['title'] + " | " + timeplayed + "/" + timesong
		drawstrings(text, 10,10, DARKRED, BASICFONT)  
		text2 = "Album: " + client.currentsong()['album'] + " | Songnumber: " + client.status()['song']
		drawstrings(text2, 10,30, DARKRED, BASICFONT)
		text3 = client.status()['state']
		drawstrings(text3, 300,height-80, DARKGREEN, BASICFONT)
		text4 = "random: " + client.status()['random'] + " | repeat: " + client.status()['repeat'] 
		drawstrings(text4, 380,height-80, DARKGREEN, BASICFONT)
	except KeyError: ##if no songs are loaded in the playlist, it will produce a key error. If this occurs, it says no song playing
		text1 = "no song playing"
		drawstrings(text1, 10,10, DARKRED, BASICFONT)
	
def drawkeys():	
	text8 = "1: show actual playlist | 2: show all playlists | 3: show help | 4: show songs of a playlist"
	drawstrings(text8, 10,height-40, DARKGRAY, BASICFONT)
	pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, 60), (800, 60), 10)
	pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, height-50), (800, height-50), 10)

def drawhelp():	
	indent = 50
	help1 = "ENTER: add URL to playlist | SPACE: pause | r: toggle random | w: toggle repeat "
	drawstrings(help1, indent,70, DARKGRAY, PLAYLISTFONT)
	help2 = "Joystick and keyboard: left: last | right: next | up: show on LED | down: pause "
	drawstrings(help2, indent,85, DARKGRAY, PLAYLISTFONT)
	help3 = "p: select Playlist to add | n: play track | c: clear"
	drawstrings(help3, indent,100, DARKGRAY, PLAYLISTFONT)
	help4 = "1: show actual playlist | 2: show all playlists | 3: show this page | 4: show songs of a playlist"
	drawstrings(help4, indent,115, DARKGRAY, PLAYLISTFONT)

def setscreenone():
	global SCREEN 
	SCREEN = 1
def setscreentwo():
	global SCREEN 
	SCREEN = 2
def setscreenthree():
	global SCREEN 
	SCREEN = 3	
def setscreenfour():
	global SCREEN 
	SCREEN = 4

def setplaylistname():
	global playlistname
	i = 0
	j = []
	for song in client.listplaylists():
		#print (i ,song['playlist'])
		j.append(song['playlist'])#creating an array so you can access the name of the playlist. Needed because otherwise you get an error
		i+=1
	#show playlist by number
	playlistnumber = int(input("Please enter the number of the playlist you want to see: ") )
	playlistname = j[playlistnumber]
	
	
#########manipulate playback
def add():
	print("Please insert URL")
	url = input("--> ")
	try:
		client.add(url)
	except musicpd.CommandError:
		print ("Please enter a playable URL")
	#local tracks: 'local:track:USB/Musik/Ko%3Fn/Untouchables/02%20Make%20Believe.mp3'
	#spotify: 'spotify:track:5m88DsBQPIfXps1FomdwqA'

def playnext(): ##play next track
	client.next()
	#helpers.printcurrentsong(client)

def random():#toggle random
	if (client.status()['random'] == "1"):
		client.random(0)
	else:
		client.random(1)
		
def repeat():#toggle repeat
	if (client.status()['repeat'] == "1"):
		client.repeat(0)
	else:
		client.repeat(1)	
	
def playlast():##start current track again or play song before if actual song runs less than 10 seconds
	tracknumber = float(client.status()['song'])
	tracknumber = int(tracknumber)	
	if (float(client.status()['elapsed'])<10):
		tracknumber = tracknumber -1
	else:
		pass	
	client.play(tracknumber)

def playtitle():##play given number on the playlist
	playtitleloop = True
	while playtitleloop:
		print("Enter the number of the song you want to play")
		try:
			number = int(input())
			if (number < 0):# | (number >10):
				print("Please insert a positive number")
			else:
				client.play(number)
				playtitleloop = False
		except ValueError:
			print ("Please enter a number")

def clearplaylist(): #clear the playlist
	client.clear()

def addplaylist(): ##the not-so-nice way: shows text in shell. Could be moved to a graphical view
	i = 0
	j = []
	for song in client.listplaylists():
		#print (i ,song['playlist'])
		j.append(song['playlist'])#creating an array so you can access the name of the playlist. Needed because otherwise you get an error
		i+=1
	#add playlist by number:
	playlistnumber = int(input("Please enter the number of playlist to add: ") )
	client.load(j[playlistnumber])#call this entry in the list and load the playlist
	print("Playlist " + j[playlistnumber]+ " added")
	

########output to senseHat
def actualled():##show the name and artist of current song on the LED-Display on the senseHat
	text = client.currentsong()['artist'] + " - " + client.currentsong()['title']
	#print(text) debug
	sense.show_message(text, text_colour=RED)

##################handle input
def handle_event(event):##configure what happens when a button is pressed
    if event.key == pygame.K_SPACE:
        pause()
    elif event.key == pygame.K_RIGHT:
        playnext()
    elif event.key == pygame.K_LEFT:
        playlast()
    elif event.key == pygame.K_RETURN:
        add()
    elif event.key == pygame.K_UP:
		##next block checks if SenseHat is connected
        found = False;
        devices = [InputDevice(fn) for fn in list_devices()]
        for dev in devices:
            if dev.name == 'Raspberry Pi Sense HAT Joystick':
                found = True
                break
        if not(found):
            print('Raspberry Pi Sense HAT not connected.')
        else:
            actualled()
    elif event.key == pygame.K_DOWN:
        pause()
    elif event.key == pygame.K_r:
        random()
    elif event.key == pygame.K_w:
        repeat()
    elif event.key == pygame.K_n:
        playtitle()
    elif event.key == pygame.K_c:
        clearplaylist()
    elif event.key == pygame.K_p:
        addplaylist()
    elif event.key == pygame.K_1:
        setscreenone()
    elif event.key == pygame.K_2:
        setscreentwo()
    elif event.key == pygame.K_3:
        setscreenthree()
    elif event.key == pygame.K_4:
        setscreenfour()
        setplaylistname()



###################
###run the program:
def main():
	running = True #sets variable to True, so the loop goes on
	while running:##loop goes on until ESCAPE is pressed
		connect()##connect to server
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				handle_event(event)
		#time.sleep(10)
		screen.fill(BLACK)
		drawkeys()#draw instructions to the screen
		drawsong()#draw information of the current song
		if (SCREEN == 1):
			drawplaylist()#draw information of the playlist
		elif (SCREEN == 2):
			drawallplaylists()#draw list of all playlists
		elif (SCREEN == 3):
			drawhelp()#draw list of all playlists
		elif (SCREEN == 4):
			drawoneplaylist()#draw info of one playlist
		pygame.display.update()
		disconnect()#disconnect from server this is not very cool, but I did not find a better solution yet. If you leave it out, it runs into the same connection error as with the wrong IP
		time.sleep(0.5) ###give the server some time to relax (can be lower, so you do not have any delay when pressing a key)


###############
###init:
##sensehat:
##next block checks if SenseHat is connected
found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
	if dev.name == 'Raspberry Pi Sense HAT Joystick':#if you find the joystick, the variable is set to True and SenseHat can be initialized
		found = True
		break
if not(found):
	print('Raspberry Pi Sense HAT not connected.')
else:
	sense = SenseHat()
	sense.clear()

##reading configuration from file
try:
	with open('config.txt') as f:
		lines = f.readlines()
except FileNotFoundError:#if it cannot find the file, exit
	print("File not found")
	print("Exiting")
	sys.exit()
IP = lines[1]#IP is line number 2
PORT = int(lines[2]) #Port is line number 3
width = int(lines[3])
height = int(lines[4])
#pygame:

pygame.init()
screen = pygame.display.set_mode((width, height)) #set screen size
DISPLAYSURF = pygame.display.set_mode((width, height))
BASICFONT = pygame.font.Font('freesansbold.ttf', 18) #set basic font
PLAYLISTFONT = pygame.font.Font('freesansbold.ttf', 14) #sets font for playlist (I made this one a little bit smaller, so more items can be displayed)
pygame.display.set_caption('MPD Control') # set caption of window



#musicpdc
client = musicpd.MPDClient() # create client object

#####colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKRED   = (155,   0,   0)
DARKGRAY  = ( 60,  60,  60)
DARKBLUE  = (  0,   0, 100)

global SCREEN ##assigns the number of the screen as global variable. Not the nicest way :(
SCREEN = 1
main() #start the program
