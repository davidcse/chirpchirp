import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from bson import json_util
# main file for database transactions

# used to represent mongo client
class tweetdb:
    def __init__(self, user=None, tweet=None, search=None):
        # set models
        self.user = user
        self.tweet = tweet
        self.search = search
        # connect to mongo
        self.client = MongoClient()
        self.db = self.client.tweet
        self.userDB = self.db.user
        self.tweetsDB = self.db.tweets

    # insert disabled user
    def insertdisable(self):
        u = self.user
        self.userDB.insert({
            "username": u.username,
            "email": u.email,
            "password": u.password,
            "verified": False
        })

    # verify user
    def verifyuser(self):
        # assume key matched abracadabra
        u = self.user
        self.userDB.update_one({"email": u.email}, {"$set": {"verified": True}}, upsert=False)

    #
    def isverified(self):
        u = self.user
        print u.username
        print u.password
        return self.userDB.find({"username": u.username, "password": u.password, "verified": True}).count() > 0

    #
    def getuid(self):
        u = self.user
        doc = self.userDB.find_one({"username": u.username, "password": u.password})
        return str(doc["_id"])

    # post a tweet
    def posttweet(self):
        t = self.tweet
        return str(self.tweetsDB.insert({
            "uid": t.uid,
            "username": t.uname,
            "content": t.content,
            "tweetstamp": int(time.time())
        }))

    # individual tweet search
    def itemsearch(self, id):
        t = self.tweetsDB.find_one({"_id": ObjectId(id)})
        if t is None:
            return {
                "status": "error",
                "error": "Id does not exist"
            }
        return {
            "status": "OK",
            "item": {
                "id": str(t["_id"]),
                "username": t["username"],
                "content": t["content"],
                "timestamp": t["tweetstamp"]
            }
        }

    def tweetsearch(self):
        s = self.search
        stamp = s.tweetstamp
        lim = s.limit
        results = {
            "status": "OK",
            "items": []
        }
        # @todo implement sort by
        tweets = self.tweetsDB.find({}).sort("tweetstamp", -1).limit(lim)
        for t in tweets:
            results["items"].append({
                "id": str(t["_id"]),
                "username": t["username"],
                "content": t["content"],
                "timestamp": t["tweetstamp"]
            })
        return results

    # close mongo connection
    def close(self):
        self.client.close()
