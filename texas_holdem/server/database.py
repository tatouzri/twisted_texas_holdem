import MySQLdb as mdb
import sys
import bcrypt

class DatabaseConnection():

    host = 'localhost'
    user = 'texasuser'
    password = 'texasuser'
    db = 'texas_holdem'

    def __init__(self):
	self.connection = mdb.connect(self.host, self.user, self.password, self.db)
	self.cursor = self.connection.cursor()

    def create_user(self,username,plain_pwd,hint):
	hashed_pwd = bcrypt.hashpw(plain_pwd.encode('utf-8'), bcrypt.gensalt())
	insertstmt=("insert into texas_holdem_users (user_name, password, hint) values ('%s', '%s', '%s')" % (username,hashed_pwd, hint))
	try:
	    self.cursor.execute(insertstmt)
	    self.connection.commit()
	    return username
	except:
            self.connection.rollback()

    def check_user(self,username,plain_pwd):
	try:
	    self.cursor.execute("SELECT user_name, password FROM texas_holdem_users WHERE user_name = '%s' " % (username))
	    self.connection.commit()
	    data = self.cursor.fetchone()
    	    if data == None :
                return None
	    hashed_pwd = data[1]
	    if bcrypt.hashpw(plain_pwd.encode('utf-8'), hashed_pwd) == hashed_pwd:
		return username
	    else:
		return None
	except:
            self.connection.rollback()
	    return None
    
    def get_user_hint(self,username):
	try:
	    self.cursor.execute("SELECT user_name, hint FROM texas_holdem_users WHERE user_name = '%s' " % (username))
	    self.connection.commit()
	    data = self.cursor.fetchone()
    	    if data == None :
                return None
	    else:
	        return data[1]
	except:
	    print "Error %d: %s" % (e.args[0],e.args[1])
            self.connection.rollback()
	    return None
    
    def create_db(self):
	try:
	    self.cursor.execute("DROP TABLE IF EXISTS texas_holdem_users")
	    self.cursor.execute("CREATE TABLE texas_holdem_users(id INT PRIMARY KEY AUTO_INCREMENT, \
		 user_name VARCHAR(25), password char(60), hint VARCHAR(64),UNIQUE(user_name))")
	    self.connection.commit()

	except mdb.Error, e:
	    print "Error %d: %s" % (e.args[0],e.args[1])
	    sys.exit(1)

if __name__ == '__main__':
    con = DatabaseConnection()
    con.create_db()
    con.create_user("taha","taha","this is a hint")
    hint = con.get_user_hint('taha')
    print 'hint : ',hint
    user = con.check_user("taha","taha")
    if user == None:
        print 'error user credentials ', user
    else:
        print 'congrats ', user 
