#! /usr/bin/env python
from docopt import docopt
from getart.command_def import __doc__ as command_def
from getart.utilities import MusicInfo
from getart.utilities import get_album_art
from discogs_client import DiscogsAPIError
from pprint import pprint

def main():
    # Grab args
    args = docopt(command_def)

    # Scan root directory for all music files (wma, m4a and mp3)
    music_info = MusicInfo(args.get('<directory>'))

    # Enter main loop
    for artist,artist_info in music_info.data.items():
        for album,album_info in artist_info['albums'].items():
            try:
                uri = get_album_art(artist, album_info['title'])
                print(uri)
            except(Exception, DiscogsAPIError) as err:
                # Future: Make debug information available via -v/--verbose
                pass

if __name__=='__main__':
    main()
