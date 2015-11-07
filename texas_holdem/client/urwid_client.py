import urwid
import window
import json

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol

import sys

from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, protocol


class TelnetClient(StatefulTelnetProtocol):

    def rawDataReceived(self,bytes):
        """
	receive raw data
        """
	self.delegateCall("rawDataReceived",bytes)

    def connectionMade(self):
        """
	display connected
        """
	self.delegateCall("connectionMade")

    #def lineReceived(self, line):
	"""
	display recieved line
	"""
	#self.delegateCall("lineReceived",line.rstrip('\r\n').rstrip(" "))

    def dataReceived(self, data):
	"""
	display recieved data
	"""
	self.delegateCall("dataReceived",data)

    def delegateCall(self, method, *args, **kwargs):
        """ Delegate our call to the controller.
        Let the controller be responsible for handling the call, to
        either display it on the view. Or to ignore it and do nothing.
        """
        if hasattr(self.factory.controller, method):
            getattr(self.factory.controller, method)(*args, **kwargs)

class TelnetFactory(protocol.ClientFactory):
    protocol = TelnetClient

    def __init__(self, controller):
        """ Keep a reference to our controller. """
        self.controller = controller

    def buildProtocol(self, addr):
	instance = self.protocol()
        instance.factory = self
        self.controller.connection = instance
        return instance

class Controller(object):
    """ The controller is what glues all components together.
    It displays the data received by the protocol instance on the view, it
    sets up the main loop and handles user input.
    """

    def __init__(self):
        self.view = window.MainWindow(self)
        self.factory = TelnetFactory(self)

    def main(self):
        """ Setup the main loop.
        We use urwid.TwistedEventLoop() to integrate the twisted framework
        into our application.
        """
        self.loop = urwid.MainLoop(self.view.frame, self.view.palette,
            unhandled_input=self.exit_on_q,
            event_loop=urwid.TwistedEventLoop())
	self.connect_to_telnet_server()
	self.loop.run()

    def connect_to_telnet_server(self):
	reactor.connectTCP("localhost", 5051, self.factory)

    def connectionMade(self):
        """
	main window
        """
	self.view.diplay_connection_page()
	self.loop.draw_screen()

    def lineReceived(self, line):
	"""
	display recieved line
	"""
	pass

    def dataReceived(self, data):
	"""
	display recieved data
	"""
	self.handle_message(data)

    def send_data(self,data):
	self.connection.sendLine(data)

    def registration_response(self,json_message):
	if (json_message['status']=='KO'):
	    self.view.display_error_message(json_message['message'])
	else:
	    self.view.display_success_message(json_message['message'])
	self.loop.draw_screen()

    def login_response(self,json_message):
	if (json_message['status']=='KO'):
	    self.view.display_error_message(json_message['message'])
	else:
	    self.view.display_success_message(json_message['message'])
	self.loop.draw_screen()

    def hint_response(self,json_message):
	if (json_message['status']=='KO'):
	    self.view.display_error_message(json_message['message'])
	else:
	    self.view.display_success_message(json_message['message'])
	self.loop.draw_screen()

    def handle_message(self,json_string):
	parsed_json = json.loads(json_string)
	message_type = parsed_json['message_type']
	return {
	    'registration' : lambda json_message: self.registration_response(json_message),
	    'login' : lambda json_message: self.login_response(json_message),
	    'hint' : lambda json_message: self.hint_response(json_message),
	}[message_type](parsed_json)

    def exit_on_q(self,key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

if __name__ == "__main__":
    Controller().main()
