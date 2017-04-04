import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
# main file for database transactions


# @Todo refactor this class
# Serves as a mongoDB client
class tweetdb:
    def __init__(self, user=None, tweet=None, search=None, follow=None):
        # set models
        self.user = user
        self.tweet = tweet
        self.search = search
        self.follow = follow
        # connect to mongo, eventually migrate to sharding...
        # if not user is None:
        #     self.client = MongoClient('130.245.168.162',27017)
        # else:
        #     self.client = MongoClient('130.245.168.191', 27017)
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client.tweet
        self.userDB = self.db.user
        self.tweetsDB = self.db.tweets
        self.followsDB = self.db.follows
        # ensure that both email and username form a joint unique key
        self.userDB.create_index("username", unique=True)
        self.userDB.create_index("email", unique=True)

    # insert disabled user
    def insertdisable(self):
        u = self.user
        try:
            self.userDB.insert({
                "username": u.username,
                "email": u.email,
                "password": u.password,
                "verified": False
            })
            return True
        except DuplicateKeyError:
            return False

    # verify user
    def verifyuser(self):
        # assume key matched abracadabra
        u = self.user
        result = self.userDB.update_one({"email": u.email}, {"$set": {"verified": True}}, upsert=False)
        # verify that operation success, else means record does not exist in db.
        # v = self.userDB.find_one({"email":u.email,"verified":True})
        return result.modified_count == 1 #v != None

    #
    def isverified(self):
        u = self.user
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

    # deletes tweet associated with id
    def delete_tweet(self, id):
        result = self.tweetsDB.delete_one({"uid": id})
        return "Success" if result.deleted_count == 1 else "Failure"

    # search query
    def tweetsearch(self):
        s = self.search
        stamp = s.tweetstamp
        lim = s.limit
        results = {
            "status": "OK",
            "items": []
        }
        #
        tweets = self.tweetsDB.find({}).sort("tweetstamp", -1).limit(lim)
        for t in tweets:
            results["items"].append({
                "id": str(t["_id"]),
                "username": t["username"],
                "content": t["content"],
                "timestamp": t["tweetstamp"]
            })
        return results

    # this will follow or unfollow a user
    def follow_or_unfollow(self, curr_uname):
        # get request model
        follow_model = self.follow
        status = True
        if follow_model.follow == True:
            print curr_uname, 'following', follow_model.username
            # insert into database, without duplicates.
            self.followsDB.update_one({
                "username": follow_model.username,
                "follower_username": curr_uname
            },upsert=True)
        elif follow_model.follow == False:
            print curr_uname, 'unfollowing', follow_model.username
            # delete record representing a follow relationship
            self.followsDB.delete_one({
                "username": follow_model.username,
                "follower_username": curr_uname
            })
        else:
            status = False
        return status

    # returns followers of user (username)
    def get_followers(self, username, limit):
        results = {
            "status": "OK",
            "users": []
        }
        following = self.followsDB.find({"username": username}).limit(limit)
        for f in following:
            results["users"].append(f["follower_username"])
        return results

    # returns users that username is following
    def get_following(self, username, limit):
        results = {
            "status": "OK",
            "users": []
        }
        following = self.followsDB.find({"follower_username": username}).limit(limit)
        for f in following:
            results["users"].append(f["username"])
        return results

    # Gets user profile information
    def retrieve_user(self, username):
        doc = self.userDB.find_one({"username": username})
        following_count = self.followsDB.find({"follower_username": username}).count()
        followers_count = self.followsDB.find({"username": username}).count()
        results = {
            "status": "OK",
            "user": {
                "email": doc["email"],
                "followers": followers_count,
                "following": following_count
            }
        }
        return results

    # close mongoDB connection
    def close(self):
        self.client.close()
