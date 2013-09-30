#! /home/thath/dev/fmmd/bin/python
"""
Usage:
 fmmd [options]... <directory>...

option:
    -r, --recurse  Recurse into the directory tree
"""

from docopt import docopt
from pprint import pprint
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.asf import ASF
import os,re

def rename_mp3(file):
    """
    <file> is the absolute path the music file that needs to be renamed
    """

    pat = re.compile(r'(\d+)/\d+')#Some times tracks show up like 1/8, so we have to filter it. 
    dirname = os.path.dirname(file)

    try:
        audio = MP3(file)
        print file,audio["TIT2"],audio["TRCK"]
        result = pat.match(unicode(audio["TRCK"]))
        if result:
            if int(result.group(1)) < 10:
                dest = u"0"+result.group(1)+u" "+unicode(audio["TIT2"]).replace('/','-')+u".mp3"
            else:
                dest = result.group(1)+u" "+unicode(audio["TIT2"]).replace('/','-')+u".mp3"
        else:
            if int(unicode(audio['TRCK'][0])) < 10:
                dest = u"0"+unicode(audio['TRCK'][0])+u" "+unicode(audio["TIT2"]).replace('/','-')+u".mp3"
            else:
                dest = unicode(audio['TRCK'][0])+u" "+unicode(audio["TIT2"]).replace('/','-')+u".mp3"
        os.rename(file, os.path.join(dirname,dest))
    except Exception, e: 
        print "Operation failed for file: ",file," with message: ",e

def rename_m4a(file):
    """
    <file> is the absolute path the music file that needs to be renamed
    """

    dirname = os.path.dirname(file)

    try:
        audio = MP4(file)
        print file,audio['\xa9nam'][0],audio['trkn'][0][0]
        if int(audio['trkn'][0][0]) < 10:
            dest = u"0"+unicode(audio['trkn'][0][0])+u" "+unicode(audio['\xa9nam'][0]).replace('/','-')+u".m4a"
        else:
            dest = unicode(audio['trkn'][0][0])+u" "+unicode(audio['\xa9nam'][0]).replace('/','-')+u".m4a"
        os.rename(file,os.path.join(dirname,dest))
    except Exception, e:
        print "Operation failed for file: ",file," with message: ",e

def rename_wma(file):
    """
    <file> is the absolute path the music file that needs to be renamed
    """

    dirname = os.path.dirname(file)

    try:
        audio = ASF(file)
        print file,audio['Title'][0],audio['WM/TrackNumber'][0]
        if int(unicode(audio['WM/TrackNumber'][0])) < 10:
            dest = u"0"+unicode(audio['WM/TrackNumber'][0])+u" "+unicode(audio['Title'][0]).replace('/','-')+u".wma"
        else:
            dest = unicode(audio['WM/TrackNumber'][0])+u" "+unicode(audio['Title'][0]).replace('/','-')+u".wma"
        os.rename(file,os.path.join(dirname,dest))
    except Exception, e:
        print "Operation failed for file: ",file," with message: ",e


def main():
    # Grab args
    args = docopt(__doc__)

    if args.get('--recurse'):
        for top in args.get('<directory>'):
            for walk in os.walk(top):
                for fname in walk[2]:
                    file_name = os.path.join(walk[0],fname)

                    if fname[-3:].lower() == 'wma':
                        rename_wma( file_name )
                    elif fname[-3:].lower() == 'mp3':
                        rename_mp3( file_name )
                    elif fname[-3:].lower() == 'm4a':
                        rename_m4a( file_name )
    else:
        for top in args.get('<directory>'):
            if os.path.isdir(top):
                for fname in os.listdir(top):
                    file_name = os.path.join(top,fname)

                    if fname[-3:].lower() == 'wma':
                        rename_wma( file_name )
                    elif fname[-3:].lower() == 'mp3':
                        rename_mp3( file_name )
                    elif fname[-3:].lower() == 'm4a':
                        rename_m4a( file_name )
            elif os.path.isfile(top):
                file_name = top

                if file_name[-3:].lower() == 'wma':
                    rename_wma( file_name )
                elif file_name[-3:].lower() == 'mp3':
                    rename_mp3( file_name )
                elif file_name[-3:].lower() == 'm4a':
                    rename_m4a( file_name )
            else:
                print('"'+top + '" is neither a file nor directory')


if __name__=='__main__':
    main()
