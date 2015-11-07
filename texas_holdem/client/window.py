import urwid
from ..message import user

class MainWindow(object):

    palette = [
        ('banner', 'yellow', 'dark red'),
        ('btn', 'light gray', 'dark blue'),
        ('txt', 'light gray', 'dark blue'),
	('error', 'light red', 'dark blue'),
	('success', 'light green', 'dark blue'),
        ('edt', 'light gray', 'dark blue', 'standout'),
        ('streak', 'black', 'dark red'),
        ('bg', 'black', 'dark blue'),
        ('focus', 'light gray', 'dark cyan', 'standout', '#ff8', '#806'),
    ]

    def __init__(self, controller):
        """
	init screen
        """
	self.controller = controller
        text = urwid.Text(('banner', u" Connecting ... "), align='center')
	self.fill = urwid.Filler(text)
	self.frame = urwid.AttrMap(self.fill, 'bg')
	self.message = urwid.AttrMap(urwid.Text('',align='center'),'txt')

    def line_write(self, new_text):
        """ change message if connected. """
	new_txt_spaced = " " + new_text + " "
	new_text_widget = urwid.Text(('banner', new_txt_spaced.encode("utf-8")), align='center')
	self.fill.original_widget = new_text_widget

    def menu_button(self,txt,callback,callback_params):
	""" a modular button for menus, with modified look and feel: bordered """
        button = urwid.Button("")
	if callback_params is not None:
	    urwid.connect_signal(button, 'click', callback,callback_params)
	else:
	    urwid.connect_signal(button, 'click', callback)
	button._w = urwid.AttrMap(urwid.SelectableIcon(['  ',txt], 100), 'btn', 'focus')
	borderedButton = urwid.LineBox(button)
        return urwid.AttrMap(borderedButton, 'btn', 'focus')

    def main_menu(self):
	""" login, signup within columns """
	body = [self.menu_button(u'Login',self.open_login_page,None),self.menu_button(u'Signup',self.open_registration_page,None)]
        return urwid.Columns(body,dividechars=2)

    def diplay_connection_page(self):
	""" login or signup. """
	choices = u'Login Signup'.split()
	mainmenu = urwid.Padding(self.main_menu(), align='center',left=20,right=20)
	self.fill.original_widget = mainmenu

    def input_area(self,edit):
    	borderedEdit = urwid.LineBox(edit)
    	return urwid.AttrMap(borderedEdit, 'edt', 'focus')

    def input_line(self,label,ainput):
    	body = [urwid.AttrMap(urwid.Text(label),'txt'),ainput]
    	return urwid.Columns(body,dividechars=2)

    def login_page(self):
	menuTitle = urwid.AttrMap(urwid.Text(u'LOGIN',align='center'),'txt')
	self.message.original_widget.set_text('')
    	body = [menuTitle, urwid.Divider(), urwid.Divider(),self.message, urwid.Divider()]
	
	login_input = urwid.Edit(u'')
	body.append(self.input_line(u'login',self.input_area(login_input)))
	password_input = urwid.Edit(u'',mask=u'*')
    	body.append(self.input_line(u'password',self.input_area(password_input)))
    	body.append(self.menu_button(u'validate',self.validate_login, (login_input, password_input)))
    	body.append(self.menu_button(u'show hint',self.show_hint,(login_input,)))
    	body.append(self.menu_button(u'return',self.return_connection_page,None))
    	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def registration_page(self):
	menuTitle = urwid.AttrMap(urwid.Text(u'REGISTRATION',align='center'),'txt')
	self.message.original_widget.set_text('')
    	body = [menuTitle, urwid.Divider(), urwid.Divider(),self.message, urwid.Divider()]
	
	login_input = urwid.Edit(u'')
	body.append(self.input_line(u'login',self.input_area(login_input)))

	password_input = urwid.Edit(u'',mask=u'*')
    	body.append(self.input_line(u'password',self.input_area(password_input)))
	confirm_password_input = urwid.Edit(u'',mask=u'*')
    	body.append(self.input_line(u'confirm password',self.input_area(confirm_password_input)))

	hint_input = urwid.Edit(u'')
	body.append(self.input_line(u'hint',self.input_area(hint_input)))

	params=(login_input,password_input,confirm_password_input,hint_input)
	body.append(self.menu_button(u'validate',self.validate_registration,params))
	body.append(self.menu_button(u'return',self.return_connection_page,None))
    	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def open_login_page(self,button):
        mainmenu = urwid.Padding(self.login_page(), align='center',left=20,right=20)
	mainadapter = urwid.BoxAdapter(mainmenu,25)
	self.fill.original_widget = mainadapter

    def open_registration_page(self,button):
        mainmenu = urwid.Padding(self.registration_page(), align='center',left=20,right=20)
	mainadapter = urwid.BoxAdapter(mainmenu,25)
	self.fill.original_widget = mainadapter

    def exit_program(self,button):
        raise urwid.ExitMainLoop()

    def validate_login(self,button,params):
	username = params[0].get_edit_text()
	pwd = params[1].get_edit_text()
	if (not username or not pwd):
	    self.display_error_message('please verify your inputs')
	else:
	    usr = user.LoginUser(username,pwd)
	    json_usr = usr.to_JSON()
	    self.controller.send_data(json_usr)

    def validate_registration(self,button,params):
	username = params[0].get_edit_text()
	pwd = params[1].get_edit_text()
	verif_pwd = params[2].get_edit_text()
	hint = params[3].get_edit_text()
	if (not username or not pwd or not hint or pwd!= verif_pwd):
	    self.display_error_message('please verify your inputs')
	else:
	    usr = user.RegisterUser(username,pwd,hint)
	    json_usr = usr.to_JSON()
	    self.controller.send_data(json_usr)

    def show_hint(self,button,params):
	username = params[0].get_edit_text()
	if (not username):
	    self.display_error_message('please verify your inputs')
	else:
	    usr = user.AskForHintUser(username)
	    json_usr = usr.to_JSON()
	    self.controller.send_data(json_usr)

    def display_error_message(self,message):
	self.message.original_widget.set_text(message)
	self.message.set_attr_map({None:'error'})

    def display_success_message(self,message):
	self.message.original_widget.set_text(message)
	self.message.set_attr_map({None:'success'})

    def display_message(self,message):
	self.message.original_widget.set_text(message)
	self.message.set_attr_map({None:'txt'})

    def return_connection_page(self,button):
	self.diplay_connection_page()

