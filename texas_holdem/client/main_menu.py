import urwid

choices = u'Login Signup'.split()
palette = [
    ('btn', 'light gray', 'dark blue'),
    ('txt', 'light gray', 'dark blue'),
    ('edt', 'light gray', 'dark blue', 'standout'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),
    ('focus', 'light gray', 'dark cyan', 'standout', '#ff8', '#806'),
    ]

def menu(choices):
    body = []
    for c in choices:
        button = urwid.Button("")
	urwid.connect_signal(button, 'click', exit_program)
        button._w =urwid.SelectableIcon(['  ',c], 100)
	borderedButton = urwid.LineBox(button)
        body.append(urwid.AttrMap(borderedButton, 'btn', 'focus'))
    return urwid.Columns(body,dividechars=2)

def exit_program(button):
    raise urwid.ExitMainLoop()

mainmenu = urwid.Padding(menu(choices), align='center',left=20,right=20)
fill = urwid.Filler(mainmenu,'middle')
main = urwid.AttrMap(fill, 'bg')
urwid.MainLoop(main,palette).run()
