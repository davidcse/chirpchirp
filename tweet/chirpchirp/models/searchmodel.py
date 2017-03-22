import json

# helper for a search query
class searchmodel:
    def __init__(self, request):
        body = request.body
        params = json.loads(body)
        self.tweetstamp = params.get("timestamp")
        limit = params.get("limit", "")
        # set default
        if limit == "":
            limit = 25
        # set max
        elif limit > 100:
            limit = 100
        self.limit = limit
    def fo(self):
        print r''