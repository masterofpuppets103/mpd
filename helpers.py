#!/usr/bin/python
import musicpd
import helpers

def printcurrentsong(client):
    timeplayed = float(client.status()['elapsed'])
    sekunden = round(timeplayed % 60)
    minuten = round(timeplayed /60)
    print ("Song: " , client.currentsong()['title'], "| Artist: ", client.currentsong()['artist'],
       " | Album: ", client.currentsong()['album'], "| Songnumber: ", client.status()['song'],
       "| Time played: ", minuten, ":", sekunden)
