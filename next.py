#!/usr/bin/python
#connects to the server and plays next track
import musicpd
import helpers

client = musicpd.MPDClient()       # create client object
client.connect('192.168.1.102', 6600)  # connect to server:6600
print ("Version: ",  client.mpd_version)           # print the mpd version
client.next()   #play next song
print ("Playing next song:")
helpers.printcurrentsong(client)
client.close()                     # send the close command
client.disconnect()                # disconnect from the server

