"""
Simple telnet server that returns a welcome message to new connected user
"""

from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory
from twisted.application.internet import TCPServer
from twisted.application.service import Application
import time
import json
import database
import response

class TelnetTexasHoldem(TelnetProtocol):
    user_count = 0

    def __init__(self):
	self.db_connection = dbConnection
	self.respone = None

    def connectionMade(self):
        TelnetTexasHoldem.user_count += 1
	print "new user connectd, user count:  ", TelnetTexasHoldem.user_count

    def dataReceived(self, data):
	result = self.handle_message(data)
	json_result = result.to_JSON()
	self.transport.write(json_result)

    def create_user(self,json_message):
	username = json_message['username']
	pwd = json_message['password']
	hint = json_message['hint']
	db_result = self.db_connection.create_user(username,pwd,hint)
	if db_result == None:
	    result = response.Response('user exists','registration','KO')
	    print 'creating new user failed: ',username
	else:
	    result = response.Response('congratulations user created','registration','OK')
	    print 'new user created: ',username
	return result

    def login_user(self,json_message):
	username = json_message['username']
	pwd = json_message['password']
	db_result = self.db_connection.check_user(username,pwd)
	if db_result == None:
	    result = response.Response('error login please verify your credentials','login','KO')
	    print 'try login failed: ',username
	else:
	    result = response.Response('congratulations login success','login','OK')
	    print 'user logged in: ',username
	return result

    def get_user_hint(self,json_message):
	username = json_message['username']
	db_result = self.db_connection.get_user_hint(username)
	if db_result == None:
	    result = response.Response('error can\'t find hint please verify your username','hint','KO')
	    print 'try get hint failed: ',username
	else:
	    result = response.Response('Hint: ' + db_result,'hint','OK')
	    print 'user asked for hint in: ',username
	return result

    def handle_message(self,json_string):
	parsed_json = json.loads(json_string)
	message_type = parsed_json['message_type']
	return {
	    'registration' : lambda json_message: self.create_user(json_message),
	    'login' : lambda json_message: self.login_user(json_message),
	    'hint' : lambda json_message: self.get_user_hint(json_message),
	}[message_type](parsed_json)

dbConnection = database.DatabaseConnection()
dbConnection.create_db()
factory = ServerFactory()
factory.protocol = lambda: TelnetTransport(TelnetTexasHoldem)
service = TCPServer(5051, factory)

application = Application("Telnet Texas Holdem Server")
service.setServiceParent(application)

