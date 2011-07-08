#! /usr/bin/env python
# You need mysqldb library for python.  Please consult your distribution of Linux's mannual for information on to do this

try:
    import MySQLdb,sys
except ImportError, e:
    print e, "You need to have the mysqldb library for this script dummy!"
    import_error = False
import getpass,getopt,sys

class clean_vcp_db:

    #Please put your database information here
    username,password,database,host,prefix = '','','','',''

    def dbConnect(self):
        try:
            conn = MySQLdb.connect(host = self.host, user = self.username, passwd = self.password, db=self.database)
        except MySQLdb.Error, e: 
            print e
            return 1
        return conn

    def showTables(self,cursor,like_statment=False):
        if not like_statment:
            try:
                cursor.execute("SHOW TABLES")
                for row in cursor.fetchall():
                    print row[0]
            except MySQLdb.Error, e:
                print e, "SHOW TABLES failed"
        if like_statment:
            try:
                cursor.execute("SHOW TABLES LIKE '"+i.prefix+"%'")
                for row in cursor.fetchall():
                    print row[0]
            except MySQLdb.Error, e:
                print e, "SHOW TABLES failed"
            
    def handleArgs(self,argv):
        try:
            opts, args = getopt.getopt(argv, 'u:h:d:p', ['user=','host=','database=','passwd','defaults'])
            for opt,arg in opts:
                if opt in ('--defaults'):
                    pass
                if opt in ('-p','--passwd'):
                    self.password = getpass.getpass('Password:')
                if opt in ('-u','--user'):
                    self.username = arg
                if opt in ('-d','--database'):
                    self.database = arg
                if opt in ('-h','--host'):
                    self.host = arg
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)
        return 0

    def getPrefix(self):
        self.prefix = raw_input("Database prefix to remove: ")

    def usage(self):
        print "-h or --host=        hostname of MySQL server\n"
        print "-u or --user=        username for the MySQL server\n"
        print "-d or --database=    name of the MySQL database\n"
        print "-p or --passwd       specify you would like to use a password\n"
        print "--defaults           defaults you put in the script (python coders only!)\n" 

def main():

    if not import_error:
        sys.exit(2)

    #Create instance of our special class
    i = clean_vcp_db()
    
    if not sys.argv[1:] or '--help' in sys.argv:
        i.usage()
        return 0

    i.handleArgs(sys.argv[1:])

    conn = i.dbConnect()
    
    if conn == 1: 
        return 0

    cursor = conn.cursor()

    i.getPrefix()
    cursor.execute('SHOW TABLES LIKE "'+i.prefix+'%"')
    rows = cursor.fetchall()

    print i.prefix
    if not rows:
        print "nothing found"
        return 0

    for row in rows:
        print row[0]

    print "\n"
    answer = raw_input("Are these the tables you want to delete?\nPress 'y' if true press 'n' if not ")

    if answer == 'y':
        for row in rows:
            try:
                cursor.execute("DROP TABLE "+row[0])
            except MySQLdb.Error, e:
                if e[0] == 1051:
                    try:
                        cursor.execute("DROP VIEW "+row[0])
                    except MySQLdb.Error, e:
                        print e, "DROP VIEW gone wrong"
                else:
                    print e, "DROP TABLE gone wrong"

        i.showTables(cursor)
        print "\nThis is your new database buddy hope you like it!!"

        return 0 

    else:
        print "bye-bye"
        return 0

if __name__ == '__main__':
    main()

