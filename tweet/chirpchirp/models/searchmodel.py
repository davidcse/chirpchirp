import json
import time

# helper for a search query
class searchmodel:
    def __init__(self, request):
        body = request.body
        params = json.loads(body) # expects stringified json
        self.tweetstamp = params.get("timestamp", int(time.time()))
        limit = params.get("limit", 25)
        # set default
        if limit > 100:
            limit = 100
        self.limit = limit
        # search query, default to any string
        self.q = params.get("q", ".*")
        # username
        self.username = params.get("username", None)
        # following param
        self.following = params.get("following", True)


    def fo(self):
        print r''
