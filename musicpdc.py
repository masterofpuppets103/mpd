#!/usr/bin/python
import musicpd
import helpers

client = musicpd.MPDClient()       # create client object
client.connect('192.168.1.102', 6600)  # connect to localhost:6600
#print ("Version: ",  client.mpd_version)           # print the mpd version
#print ("Status: ", client.status())
#print ("Stats : ",client.stats())
#print (client.cmd('one', 2))         # print result of the command "cmd one 2"

helpers.printcurrentsong(client)
print ("Playlist:")
print ("Number \t Time \t Artist\t Song")
client.iterate = True
seconds = 0
for song in client.playlistinfo():
    seconds = float(song['time']) + seconds
    songtime = round(float(song['time'])/60, 2)
    print (song['pos'] , "\t" , songtime, "\t",  song['artist'] , " \t" , song['title'] , "\t ")
totalminutes = round(seconds/60)
totalseconds = round(seconds % 60)
print ("Gesamtzeit: ", totalminutes, ":", totalseconds)#shows how long the playlist will last
#print (song)
client.close()                     # send the close command
client.disconnect()                # disconnect from the server


#documentation: http://www.musicpd.org/doc/protocol/
