#!/usr/bin/python
#pauses/plays actual song
import musicpd
import helpers

client = musicpd.MPDClient()       # create client object
client.connect('192.168.1.102', 6600)  # connect to localhost:6600
print ("Version: ",  client.mpd_version)           # print the mpd version
client.pause()
helpers.printcurrentsong(client)
print (client.status()['state'])

client.close()                     # send the close command
client.disconnect()                # disconnect from the server

