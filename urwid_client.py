"""
This is an example of how to integrate urwid with Twisted by using
urwid.TwistedEventLoop. It is nothing fancy, and error checking is severly
lacking but it gets the job done to demonstrate how it works.
Author: Alexander Borgerth (sobber)
alex.borgert@gmail.com
PS: Requires urwid 0.9.9.1 from wardi's github repository, with commit
'84dba9430ac0f5d842897d0d7fbe36df2c06a5a7' which fixes urwid.TwistedEventLoop()
to use reactor.stop() instead of reactor.crash() to stop the reactor.
git clone git://github.com/wardi/urwid.git
"""

import urwid

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol

import sys

from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, protocol


class TelnetClient(StatefulTelnetProtocol):

    def rawDataReceived(self,bytes):
        """
	receive arw data
        """
	self.delegateCall("rawDataReceived",bytes)

    def connectionMade(self):
        """
	display connected
        """
	self.delegateCall("connectionMade")

    def lineReceived(self, line):
	"""
	display recieved data
	"""
	self.delegateCall("lineReceived",line)

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

class View(object):

    palette = [
        ('banner', 'yellow', 'dark red'),
        ('bg', 'black', 'dark blue'),
    ]

    def __init__(self):
        """
	init screen
        """
        self.text = urwid.Text(('banner', u" Connecting ... "), align='center')
	fill = urwid.Filler(self.text)
	self.frame = urwid.AttrMap(fill, 'bg')

    def lineWrite(self, text):
        """ change message if connected. """
        self.text.set_text(text)

class Controller(object):
    """ The controller is what glues all components together.
    It displays the data received by the protocol instance on the view, it
    sets up the main loop and handles user input.
    """

    def __init__(self):
        self.view = View()
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
	display connected
        """

    def lineReceived(self, line):
	"""
	display recieved data
	"""
	self.view.lineWrite(line)
	self.loop.draw_screen()

    def exit_on_q(self,key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

if __name__ == "__main__":
    Controller().main()
