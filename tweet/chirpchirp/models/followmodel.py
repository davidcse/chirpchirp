import json


# helper for a follow query
class FollowModel:
    def __init__(self, request):
        body = request.body
        params = json.loads(body)
        self.username = params.get("username", "")
        self.follow = params.get("follow", True)