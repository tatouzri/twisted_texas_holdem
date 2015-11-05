"""
Simple telnet server that returns a welcome message to new connected user
"""

from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory
from twisted.application.internet import TCPServer
from twisted.application.service import Application
import time
import json

class TelnetTexasHoldem(TelnetProtocol):
    user_count = 0

    def connectionMade(self):
        TelnetTexasHoldem.user_count += 1
	print "new user connectd, user count:  ", TelnetTexasHoldem.user_count
	#self.transport.write("welcome user %d \n\r" %(TelnetTexasHoldem.user_count,))

    def dataReceived(self, json_string):
	print "data received  ", json_string
	parsed_json = json.loads(json_string)
	#print(parsed_json['username'])

factory = ServerFactory()
factory.protocol = lambda: TelnetTransport(TelnetTexasHoldem)
service = TCPServer(5051, factory)

application = Application("Telnet Texas Holdem Server")
service.setServiceParent(application)

