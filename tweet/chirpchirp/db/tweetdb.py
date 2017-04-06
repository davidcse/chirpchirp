import time

import pymongo
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
            print 'filtering by username: ', searchmodel.username
            for word in searchmodel.q:
                if word != ".*":
                    word = r"\b{}\b".format(word)
                filtered_tweets = self.tweetsDB.find({"username": searchmodel.username, "content": {"$regex": word}, "tweetstamp": {"$lte": searchmodel.tweetstamp}}).limit(searchmodel.limit)
                for tweet in filtered_tweets:
                    if len(results["items"]) >= searchmodel.limit:
                        return results
                    if tweet["content"] not in results["items"]:
                        results["items"].append({
                            "id": str(tweet["_id"]),
                            "username": tweet["username"],
                            "content": tweet["content"],
                            "timestamp": tweet["tweetstamp"]
                        })
            return results
        # filter by users that the logged in user is following
        if searchmodel.following == True:
            # get users logged in user is following
            following_users = self.followsDB.find({"follower_username": loggedin_username}).limit(searchmodel.limit)
            for user in following_users:
                # if query string is specified fix hereeeee
                for word in searchmodel.q:
                    if word != ".*":
                        word = r"\b{}\b".format(word)
                    tweets = self.tweetsDB.find({"content": {"$regex": word}, "username": user["username"], "tweetstamp": {"$lte": searchmodel.tweetstamp}}).limit(searchmodel.limit)
                    for tweet in tweets:
                        if len(results["items"]) >= searchmodel.limit:
                            break
                        if tweet["content"] not in results["items"]:
                            results["items"].append({
                                "id": str(tweet["_id"]),
                                "username": tweet["username"],
                                "content": tweet["content"],
                                "timestamp": tweet["tweetstamp"]
                            })
        else:
            # don't filter by users that user is following
            # if query string is specified
            for word in searchmodel.q:
                if word != ".*":
                    word = r"\b{}\b".format(word)
                tweets = self.tweetsDB.find({"content": {"$regex": word},"tweetstamp": {"$lte": searchmodel.tweetstamp}}).limit(searchmodel.limit)
                for tweet in tweets:
                    if len(results["items"]) >= searchmodel.limit:
                        break
                    if tweet["content"] not in results["items"]:
                        results["items"].append({
                            "id": str(tweet["_id"]),
                            "username": tweet["username"],
                            "content": tweet["content"],
                            "timestamp": tweet["tweetstamp"]
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
            self.followsDB.insert({
                "username": follow_model.username,
                "follower_username": curr_uname
            })
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

