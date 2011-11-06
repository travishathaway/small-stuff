#! /usr/bin/env python
# Requires mutagen python library 
# see: http://code.google.com/p/mutagen/

# Author: Travis Hathaway
# Notes: Meta data really sucks.  This script is an attempt to retrieve meta data from 
#        song files and rename the songs so the files themselves have cleaner names.

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.asf import ASF
import os,sys,re,getopt

long_flags  = ['type=',
               'dir=',
               'file=',]
short_flags = 't:d:f:'

def help_text():
    print '''The is a command line utility for renaming music file names based on metadata.

    example usage: fix_songs.py --type=mp3 --dir=/home/thath/Music/Album

    please specify --type and (--dir or --file)
    
    You can only specify a single file or a single dir'''

def parse_args(args,long_flags,short_flags):
    try:
        opts, args = getopt.getopt(args[1:],short_flags,long_flags)
    except:
        print "Option not recognized"
        help_text()
        sys.exit(2)

    return opts,args

#if not sys.argv[1:]:
#    print "Please supply argument (e.g. mp3 directory)"
#     sys.exit(0)

def rename_mp3(music_file=None,music_dir=None):
    if music_dir:
        song_list = os.listdir(music_dir)
    elif music_file:
        song_list = [music_file]
    else:
        return 1

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
            print "Operation failed",song

def rename_m4a(music_file=None,music_dir=None):
    if music_dir:
        song_list = os.listdir(sys.argv[2])
    elif music_file:
        song_list = [music_file]
    else:
        return 1

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
            print "Operation failed for",song

def rename_wma(music_file=None,music_dir=None):
    if music_file:
        song_list = [music_file]
    elif music_dir:
        song_list = os.listdir(sys.argv[2])
    else:
        return 1

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
            print "Operation failed for",song

def main():
    music_file = None
    music_dir = None
    file_type = None
    opts, args = parse_args(sys.argv,long_flags,short_flags)

    for o,v in opts:
        if o == '-f' or o == '--file':
            music_file = v
        if o == '-d' or o == '--dir':
            music_dir = v
        if o == '-t' or o == '--type':
            file_type = v

    if music_file and music_dir:
        print "Cannot use both file and dir options"
        sys.exit(2)

    if music_file:
        if file_type == None:
            print "Please specify file type (wma,m4a,mp3)"
            sys.exit(2)
        if file_type == 'mp3':
            rename_mp3(music_file=music_file)
        elif file_type == 'm4a':
            rename_m4a(music_file=music_file)
        elif file_type == 'wma':
            rename_wma(music_file=music_file)
        else:
            print 'File type not supported'
            sys.exit(2)

    if music_dir:
        if file_type == None:
            print "Please specify file type (wma,m4a,mp3)"
            sys.exit(2)
        if file_type == 'mp3':
            rename_mp3(music_dir=music_dir)
        elif file_type == 'm4a':
            rename_m4a(music_dir=music_dir)
        elif file_type == 'wma':
            rename_wma(music_dir=music_dir)
        else:
            print 'File type not supported'

if __name__ == '__main__':
    main()
