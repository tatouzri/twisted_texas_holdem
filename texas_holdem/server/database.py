import MySQLdb as mdb
import sys

con = mdb.connect('localhost', 'texasuser', 'texasuser', 'texas_holdem');

def init_db():
    try:
        cur = con.cursor()  
	cur.execute("DROP TABLE IF EXISTS texas_holdem_users")
	cur.execute("CREATE TABLE texas_holdem_users(id INT PRIMARY KEY AUTO_INCREMENT, \
                 user_name VARCHAR(25), password char(32), hint VARCHAR(64))")
    
    except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
    
    finally:    
	if con:    
	    con.close()

init_db()
