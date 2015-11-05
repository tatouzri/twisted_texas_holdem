import urwid

choices = u'validate return'.split()
palette = [
    ('btn', 'light gray', 'dark blue'),
    ('txt', 'light gray', 'dark blue'),
    ('edt', 'light gray', 'dark blue', 'standout'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),
    ('focus', 'light gray', 'dark cyan', 'standout', '#ff8', '#806'),
    ]

def input_line(label,amask):
    body = [urwid.AttrMap(urwid.Text(label),'txt')]
    edit = urwid.Edit(u'',mask=amask)
    borderedEdit = urwid.LineBox(edit)
    body.append(urwid.AttrMap(borderedEdit, 'edt', 'focus'))
    return urwid.Columns(body,dividechars=2)

def menu(title, choices):
    menuTitle = urwid.AttrMap(urwid.Text(title,align='center'),'txt')
    body = [menuTitle, urwid.Divider(), urwid.Divider()]
    body.append(input_line(u'login *',None))
    body.append(input_line(u'password *',u'*'))
    body.append(input_line(u'confirm password *',u'*'))
    body.append(input_line(u'hint *',None))
    for c in choices:
        button = urwid.Button('')
	button._w =urwid.SelectableIcon(['  ',c], 100)
        urwid.connect_signal(button, 'click', exit_program)
	borderedButton = urwid.LineBox(button)
        body.append(urwid.AttrMap(borderedButton, 'btn', 'focus'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def exit_program(button):
    raise urwid.ExitMainLoop()

mainmenu = urwid.Padding(menu(u'Registration',choices), align='center',left=20,right=20)

mainadapter = urwid.BoxAdapter(mainmenu,22)
fill = urwid.Filler(mainadapter,'middle')
main = urwid.AttrMap(fill, 'bg')

urwid.MainLoop(main,palette).run()
