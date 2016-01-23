#!/usr/bin/python
#This file is used for all functions we need in more than one file, so we can reuse code
import musicpd
import helpers

def printcurrentsong(client):#gives some information to the song currently played
    timeplayed = float(client.status()['elapsed'])
    sekunden = round(timeplayed % 60)
    minuten = round(timeplayed /60)
    print ("Song: " , client.currentsong()['title'], "| Artist: ", client.currentsong()['artist'],
       " | Album: ", client.currentsong()['album'], "| Songnumber: ", client.status()['song'],
       "| Time played: ", minuten, ":", sekunden)
