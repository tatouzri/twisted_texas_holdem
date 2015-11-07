import json

class User(object):
    def __init__(self, username='',message_type=''):
        self.username = username
	self.message_type = message_type

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class RegisterUser(User):
    def __init__(self, username='', pwd='',hint=''):
	super(RegisterUser, self).__init__(username,'registration')
	self.password = pwd
        self.hint = hint

class LoginUser(User):
    def __init__(self, username='', pwd=''):
	super(LoginUser, self).__init__(username,'login')
	self.password = pwd

class AskForHintUser(User):
    def __init__(self, username=''):
	super(AskForHintUser, self).__init__(username,'hint')
