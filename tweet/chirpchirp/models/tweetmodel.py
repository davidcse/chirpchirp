import json

# used to load a tweet object on a request
class tweetmodel:
    def __init__(self, uname, uid, request):
        body = request.body # expects stringified json
        params = json.loads(body)
        self.uname = uname
        self.uid = uid
        self.content = params.get("content")
