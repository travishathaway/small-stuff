#! /home/thath/dev/small-stuff/bin/python
from docopt import docopt
from fmmd.command_def import __doc__ as command_def
from fmmd.rename import *

def main():
    # Grab args
    args = docopt(command_def)

    for top in args.get('<directory>'):
        if os.path.isdir(top):
            if args.get('--recurse'):
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
                for fname in os.listdir(top):
                    file_name = os.path.join(top, fname)

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
