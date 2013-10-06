#! /home/thath/dev/fmmd/bin/python
from docopt import docopt
from smmd.command_def import __doc__ as command_def
from smmd.stat import Stat
from pprint import pprint

def main():
    # Grab args
    args = docopt(command_def)

    stat = Stat(args.get('<directory>'))

    pprint(stat.get_num_artists())

if __name__=='__main__':
    main()
