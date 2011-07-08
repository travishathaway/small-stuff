#! /bin/sh

# This script makes files and directories group readable and writeable 
# Yes I know there is an exec option in find, but to me, the while 
# syntax is more readable

find $1 -type f | while read item; do chmod 664 $item; done
if [ $? -eq 0 ]; then 
	echo "files are good!"
fi
find $1 -type d | while read item; do chmod 775 $item; done 
if [ $? -eq 0 ]; then 
	echo "dirs are good too!"
fi
exit 0 
