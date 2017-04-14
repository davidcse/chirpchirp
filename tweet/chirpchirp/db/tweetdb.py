import time

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
import .. utils.searchDelegate
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
        # self.client = MongoClient('127.0.0.1', 27017)
        self.client = MongoClient('192.168.1.32', 27017)
        self.db = self.client.tweet
        self.userDB = self.db.user
        self.tweetsDB = self.db.tweets
        self.followsDB = self.db.follows
        # ensure that both email and username form a joint unique key
        # self.userDB.create_index("username", unique=True)
        # self.userDB.create_index("email", unique=True)
        # self.tweetsDB.create_index([("username", pymongo.ASCENDING), ("tweetstamp", pymongo.ASCENDING)])

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
        result = self.tweetsDB.delete_one({"_id": ObjectId(id)})
        return "Success" if result.deleted_count == 1 else "Failure"

    # search query
    def tweetsearch(self, loggedin_username):
        searchmodel = self.search
        results = {
            "status": "OK",
            "items": []
        }
        # filter by username
        if searchmodel.username != None:
            return searchDelegate.search_username(searchmodel=searchmodel,tweetsDB=self.tweetsDB,results=results)
        # filter by users that the logged in user is following
        if searchmodel.following == True:
            return searchDelegate.search_following(loggedin_username=loggedin_username,followsDB=self.followsDB,tweetsDB=self.tweetsDB,searchmodel=searchmodel,results=results)
        else:
            # don't filter by users that user is following
            # if query string is specified
            return searchDelegate.search_not_following(tweetsDB=self.tweetsDB, searchmodel=searchmodel, results=results)


    # this will follow or unfollow a user
    def follow_or_unfollow(self, curr_uname):
        # get request model
        follow_model = self.follow
        status = True
        if follow_model.follow == True:
            print curr_uname, 'following', follow_model.username
            # insert into database, without duplicates.
            upsert_record = {
                "username": follow_model.username,
                "follower_username": curr_uname
            }
            self.followsDB.update_one(upsert_record,{'$set':upsert_record},upsert=True)
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
        print "tweetdb(166)", "retrieved user:", str(doc)
        if(doc==None):
            return None
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
