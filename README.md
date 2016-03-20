# mpdControl
A small tool for connecting to an MPD-Server. Graphical interface using tkinter. Code for python3. code developed and tested at a raspberry pi running raspbian connecting to another raspberry pi running [PiMusicBox](http://www.pimusicbox.com/).

Why?
----

There is no tool at the raspberry pi available that lets you easily control the mpd-server. Using python and tkinter the tool needs lets ressources than a browser and starts a lot faster.

Features:
---------

  * Graphical Interface
  * Add URLs to queue
  * Add playlists to queue
  * next track, last track, pause
  * toggle random/consume/repeat/single
  * lets you shutdown your server
  * play specified song in the playlist
  * add local files to playlist
  * change of ip, port and ssh-login information within the program and via config-file

Usage: 
------

  1. Optional: specify IP-adress of your server in the file "config.txt"
  2. start program via python3 mpdcontrol.py
  3  Set IP-adress of your server via "about/setup/setup server"

Used libraries:
---------------
  * tkinter
  * paramiko
  * musicpd