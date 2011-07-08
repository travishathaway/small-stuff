#! /usr/bin/env python
# Requires mutagen python library 
# see: http://code.google.com/p/mutagen/

# Author: Travis Hathaway
# Notes: Meta data really sucks.  This script is an attempt to retrieve meta data from 
#        song files and rename the songs so the files themselves have cleaner names.

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.asf import ASF
import os,sys,re

if not sys.argv[1:]:
    print "Please supply argument (e.g. mp3 directory)"
    sys.exit(0)

if sys.argv[1] == "mp3":
    song_list = os.listdir(sys.argv[2])
    pat = re.compile(r'(\d+)/\d+')#Some times tracks show up like 1/8, so we have to filter it. 

    for song in song_list:
        try:
            audio = MP3(song)
            print song,audio["TIT2"],audio["TRCK"]
            result = pat.match(str(audio["TRCK"]))
            if result:
                if int(result.group(1)) < 10:
                    dest = "0"+result.group(1)+" "+str(audio["TIT2"]).replace('/','-')+".mp3"
                else:
                    dest = result.group(1)+" "+str(audio["TIT2"]).replace('/','-')+".mp3"
            else:
                if int(str(audio['TRCK'][0])) < 10:
                    dest = "0"+str(audio['TRCK'][0])+" "+str(audio["TIT2"]).replace('/','-')+".mp3"
                else:
                    dest = str(audio['TRCK'][0])+" "+str(audio["TIT2"]).replace('/','-')+".mp3"
            os.rename(song,dest)
        except: 
            pass

if sys.argv[1] == "m4a":
    song_list = os.listdir(sys.argv[2])

    for song in song_list:
        try:
            audio = MP4(song)
            print song,audio['\xa9nam'][0],audio['trkn'][0][0]
            if int(audio['trkn'][0][0]) < 10:
                dest = "0"+str(audio['trkn'][0][0])+" "+str(audio['\xa9nam'][0]).replace('/','-')+".m4a"
            else:
                dest = str(audio['trkn'][0][0])+" "+str(audio['\xa9nam'][0]).replace('/','-')+".m4a"
            os.rename(song,dest)
        except:
            pass

if sys.argv[1] == "wma":
    song_list = os.listdir(sys.argv[2])

    for song in song_list:
        try:
            audio = ASF(song)
            print song,audio['Title'][0],audio['WM/TrackNumber'][0]
            if int(str(audio['WM/TrackNumber'][0])) < 10:
                dest = "0"+str(audio['WM/TrackNumber'][0])+" "+str(audio['Title'][0]).replace('/','-')+".wma"
            else:
                dest = str(audio['WM/TrackNumber'][0])+" "+str(audio['Title'][0]).replace('/','-')+".wma"
            os.rename(song,dest)
        except:
            pass
