import urwid
from .. import message
from . import window

choices = (u'validate', u'show hint', u'return')
palette = [
    ('btn', 'light gray', 'dark blue'),
    ('txt', 'light gray', 'dark blue'),
    ('edt', 'light gray', 'dark blue', 'standout'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),
    ('focus', 'light gray', 'dark cyan', 'standout', '#ff8', '#806'),
    ]

def input_area(amask):
    edit = urwid.Edit(u'',mask=amask)
    borderedEdit = urwid.LineBox(edit)
    return urwid.AttrMap(borderedEdit, 'edt', 'focus')

def input_line(label,ainput):
    body = [urwid.AttrMap(urwid.Text(label),'txt'),ainput]
    return urwid.Columns(body,dividechars=2)

def menu_button(name,callback):
    button = urwid.Button('')
    button._w =urwid.SelectableIcon(['  ',name], 100)
    urwid.connect_signal(button, 'click', callback)
    borderedButton = urwid.LineBox(button)
    return urwid.AttrMap(borderedButton, 'btn', 'focus')

class menu():
    def __init__(self):
	self.login = input_area(None)
	self.pwd = input_area(u'*')
	self.title = u'LOGIN'
	
    def body(self):
	menuTitle = urwid.AttrMap(urwid.Text(self.title,align='center'),'txt')
    	body = [menuTitle, urwid.Divider(), urwid.Divider()]
	body.append(input_line(u'login',self.login))
    	body.append(input_line(u'password',self.pwd))
    	body.append(menu_button(u'validate',validate_login))
    	body.append(menu_button(u'show hint',show_hint))
    	body.append(menu_button(u'return',exit_program))
    	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def exit_program(button):
    raise urwid.ExitMainLoop()

def show_hint(button):
    #call server to show hint
    raise urwid.ExitMainLoop()

def validate_login(button):
    #verify fields are filled,then call server to verify login
    raise urwid.ExitMainLoop()


loginmenu = menu()
mainmenu = urwid.Padding(loginmenu.body(), align='center',left=20,right=20)
mainoverlay = urwid.Overlay(mainmenu, urwid.SolidFill(),
    align='center', width=('relative', 80),
    valign='middle', height=('relative', 80),
    min_width=50, min_height=9)
main = urwid.AttrMap(mainoverlay, 'bg')
urwid.MainLoop(main,palette).run()
