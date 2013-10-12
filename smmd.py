#! /home/thath/dev/small-stuff/bin/python
from docopt import docopt
from smmd.command_def import __doc__ as command_def
from smmd.stat import Stat
from pprint import pprint

def main():
    # Grab args
    args = docopt(command_def)

    stat = Stat(args.get('<directory>'))

    for key,item in stat.music_stat.items():
        print("Artist: "+key)
        print("\tSongs: "+str(item['number_of_songs']))
        print("\tAlbums: "+str(item['number_of_albums']))


if __name__=='__main__':
    main()
