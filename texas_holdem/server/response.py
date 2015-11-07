import json

class Response(object):
    def __init__(self,msg,response_type,status):
	self.message = msg
	self.message_type = response_type
	self.status = status

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

