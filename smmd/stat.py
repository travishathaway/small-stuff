from mutagen.mp3 import MP3
from pprint import pprint 
from mutagen.mp4 import MP4
from mutagen.asf import ASF
import os

class Stat(object):

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

    def get_num_artists(self):
        self.__scan()
        self.__collect_stats() 
        return self.music_stat

    def get_artist(self):
        return []

    def get_per_artist(self):
        return []

    def summary(self):
        return []

    def __scan(self):
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
        self.__collect_stats_mp3()   
        self.__collect_stats_m4a()   
        self.__collect_stats_wma()   

    def __collect_stats_mp3(self):
        for file in self.music_files['mp3']:
            mp3 = MP3(file)

            artist = str(mp3.get('TPE1', ['Unknown Artist'])[0])
            song   = str(mp3.get('TIT2', ['Unknown Title'])[0])
            album  = str(mp3.get('TALB', ['Unknown Album'])[0])

            self.__add_stats(artist, album, song)

    def __collect_stats_m4a(self):
        for file in self.music_files['m4a']:
            mp4 = MP4(file)

            artist = str(mp4.get('\xa9ART',['Unknown Artist'])[0])
            song   = str(mp4.get('\xa9nam',['Unknown Title'])[0])
            album  = str(mp4.get('\xa9alb',['Unknown Album'])[0])

            self.__add_stats(artist, album, song)

    def __collect_stats_wma(self):
        for file in self.music_files['wma']:
            asf = ASF(file)

            pprint(asf)
            artist = str(asf.get('WM/AlbumArtist', ['Unknown Artist'])[0])
            song   = str(asf.get('Title', ['Unknown Title'])[0])
            album  = str(asf.get('WM/AlbumTitle', ['Unknown Album'])[0])

            self.__add_stats(artist, album, song)

    def __add_stats(self, artist, album, song):
        if not self.music_stat.get(artist):
            self.music_stat[artist] = { 'albums' : {} }

        self.__add_album(artist, album)
        self.__add_song(artist, album, song)

    def __add_song(self, artist, album, song):
        if song not in self.music_stat[artist]['albums'][album]:
            self.music_stat[artist]['albums'][album]['songs'].append(song)

    def __add_album(self, artist, album):
        if self.music_stat[artist]['albums'].get(album) == None:
            self.music_stat[artist]['albums'][album] = {}
            self.music_stat[artist]['albums'][album]['title'] = album
            self.music_stat[artist]['albums'][album]['songs'] = []
        

def main():
    directory = ''
    stat = Stat(directory)

    stat.get_num_artists()
    #returns integer
    stat.get_artist()
    # returns list
    stat.get_per_artist()
    """
        returns
            {
                'name_1' : {
                    'songs' : 15,
                    'albums': 2,
                },
                ...
            }
    """
    stat.summary()
    # { 'albums' : 40, 'songs' : 400 }
