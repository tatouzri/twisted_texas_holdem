"""
Simple telnet server that returns a welcome message to new connected user
"""

from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory
from twisted.application.internet import TCPServer
from twisted.application.service import Application

class TelnetTexasHoldem(TelnetProtocol):
    user_count = 0

    def connectionMade(self):
        TelnetTexasHoldem.user_count += 1
        self.transport.write("welcome user %d \n\r" %(TelnetTexasHoldem.user_count,))

    def dataReceived(self, data):
	print "data received  ", data
        self.transport.write("your data back: %s \n\r" % (data,))

factory = ServerFactory()
factory.protocol = lambda: TelnetTransport(TelnetTexasHoldem)
service = TCPServer(5051, factory)

application = Application("Telnet Texas Holdem Server")
service.setServiceParent(application)

