import json

# used for loading a User object on a request
class usermodel:
    def __init__(self, request):
        body = request.body
        params = json.loads(body)
        self.username = params.get("username", "")
        self.email = params.get("email", "")
        self.password = params.get("password", "")
        self.key = params.get("key", "")
