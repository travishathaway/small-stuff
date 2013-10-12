from mutagen.mp3 import MP3
from pprint import pprint 
from mutagen.mp4 import MP4
from mutagen.asf import ASF
import os

class Stat(object):
    """
    Passing `dir` as an agrument, scan this directory recursively
    in order to gather meta-data about the supported music file
    types that lie underneath it. Support file types:
    - M4A (AAC-iTunes)
    - WMA (Windows Media Player)
    - MP3
    """

    def __init__(self, dir):
        # Base working directory
        self.dir = dir

        # categories of our files
        self.music_files = {
            'mp3' : [],
            'm4a' : [],
            'wma' : [],
        }

        self.music_stat = {}

        self.__scan()
        self.__collect_stats()

    def get_num_artists(self):
        return self.music_stat

    def get_per_artist(self):
        return []

    def summary(self):
        return []

    def __scan(self):
        """
        Scan `self.dir` for support file types:
        - M4A (AAC-iTunes)
        - WMA (Windows Media Player)
        - MP3
        """
        for dir in self.dir:
            for dir_level in os.walk(dir):
                for file in dir_level[2]:
                    if file[-3:].lower() == 'mp3':
                        self.music_files['mp3'].append(os.path.join(dir_level[0],file))
                    elif file[-3:].lower() == 'm4a':
                        self.music_files['m4a'].append(os.path.join(dir_level[0],file))
                    elif file[-3:].lower() == 'wma':
                        self.music_files['wma'].append(os.path.join(dir_level[0],file))
                        
    def __collect_stats(self):
        """
        This method collects stats from support file types:
        - M4A (AAC-iTunes)
        - WMA (Windows Media Player)
        - MP3
        """
        self.__collect_stats_mp3()   
        self.__collect_stats_m4a()   
        self.__collect_stats_wma()   

    def __collect_stats_mp3(self):
        """
        Process a MP3 file to grab meta-data from it
        """
        for file in self.music_files['mp3']:
            try: 
                mp3 = MP3(file)

                artist = unicode(mp3.get('TPE1', ['Unknown Artist'])[0])
                song   = unicode(mp3.get('TIT2', ['Unknown Title'])[0])
                album  = unicode(mp3.get('TALB', ['Unknown Album'])[0])

                self.__add_stats(artist, album, song)
            except Exception as e:
                print("Error: "+str(e))
                print("File: "+file)

    def __collect_stats_m4a(self):
        """
        Process a M4A (AAC-iTUnes) file to grab meta-data from it
        """
        for file in self.music_files['m4a']:
            try:
                mp4 = MP4(file)

                artist = unicode(mp4.get('\xa9ART',['Unknown Artist'])[0])
                song   = unicode(mp4.get('\xa9nam',['Unknown Title'])[0])
                album  = unicode(mp4.get('\xa9alb',['Unknown Album'])[0])

                self.__add_stats(artist, album, song)
            except Exception as e:
                print("Error: "+str(e))
                print("File: "+file)

    def __collect_stats_wma(self):
        """
        Process a WMA file to grab meta-data from it
        """
        for file in self.music_files['wma']:
            try:
                asf = ASF(file)

                artist = unicode(asf.get('WM/AlbumArtist', ['Unknown Artist'])[0])
                song   = unicode(asf.get('Title', ['Unknown Title'])[0])
                album  = unicode(asf.get('WM/AlbumTitle', ['Unknown Album'])[0])

                self.__add_stats(artist, album, song)
            except Exception as e:
                print("Error: "+str(e))
                print("File: "+file)

    def __add_stats(self, artist, album, song):
        """
        Called for each file that is processed. It adds the values
        to our data dict `self.music_stat`
        """
        if not self.music_stat.get(artist):
            self.music_stat[artist] = { 
                'albums' : {},
                'number_of_albums' : 0,
                'number_of_songs' : 0,
            }

        self.__add_album(artist, album)
        self.__add_song(artist, album, song)

    def __add_song(self, artist, album, song):
        """
        Add a single song to our music stat data dict `self.music_stat`
        """
        if song not in self.music_stat[artist]['albums'][album]:
            self.music_stat[artist]['albums'][album]['songs'].append(song)
            # Increment counters
            self.music_stat[artist]['albums'][album]['number_of_songs'] += 1
            self.music_stat[artist]['number_of_songs'] += 1

    def __add_album(self, artist, album):
        """
        Add a single album to our data dict `self.music_stat`
        """
        if self.music_stat[artist]['albums'].get(album) == None:
            # Add the album to our dict
            self.music_stat[artist]['albums'][album] = {}
            self.music_stat[artist]['albums'][album]['title'] = album
            
            # Initialize list for songs
            self.music_stat[artist]['albums'][album]['songs'] = []
            
            # Increment album counter
            self.music_stat[artist]['number_of_albums'] += 1

            # Per album song counter
            self.music_stat[artist]['albums'][album]['number_of_songs'] = 0
