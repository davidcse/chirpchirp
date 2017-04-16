# THIS IS A MODEL CLASS USED TO PARSE AND EXTRACT A HTTP REQUEST BODY FOR USE BY
# FUNCTIONS THAT PERFORM DATABASE QUERIES, BASED ON THIS MODEL'S FIELDS.

import json
import ast

def destring_to_intlist(stringifiedlist):
    # safely evaluates into python list, str, int, tuple
    aList = ast.literal_eval(stringifiedlist)
    # if list items are string, strip leading and trailing space chars
    intList = [int(i) for i in aList]
    return intList


# used to load a tweet object on a request
class tweetmodel:
    def __init__(self, uname, uid, request):
        body = request.body # expects stringified json
        params = json.loads(body)
        self.uname = uname
        self.uid = uid
        self.content = params.get("content")
        self.parent = params.get('parent',None)
        # convert to int for parent tweet ID
        if(self.parent != None):
            self.parent = int(self.parent)
        self.media = params.get("media",None)
        # if media is stringified list, i.e. "[]", convert to actual list [].
        if(isinstance(self.media,str)):
            self.media = destring_to_intlist(self.media)
