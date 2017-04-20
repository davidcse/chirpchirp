import time
from bson import Binary
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from .. utils import searchDelegator


# main file for database transactions
# Serves as a mongoDB client
class TweetDB:
    def __init__(self, user=None, tweet=None, search=None, follow=None, like=None):
        # set models
        self.user = user
        self.tweet = tweet
        self.search = search
        self.follow = follow
        self.like = like
        # connect to mongo
        # self.client = MongoClient('127.0.0.1', 27017)
        self.client = MongoClient('192.168.1.54', 27017)
        self.db = self.client.tweet
        self.userDB = self.db.user
        self.tweetsDB = self.db.tweets
        self.followsDB = self.db.follows
        self.mediaDB = self.db.media
        self.likesDB = self.db.likes

    # insert disabled user
    def insert_disable(self):
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
    def verify_user(self):
        # assume key matched abracadabra
        u = self.user
        result = self.userDB.update_one({"email": u.email}, {"$set": {"verified": True}}, upsert=False)
        # verify that operation success, else means record does not exist in db.
        # v = self.userDB.find_one({"email":u.email,"verified":True})
        return result.modified_count == 1 #v != None

    #
    def is_verified(self):
        u = self.user
        return self.userDB.find({"username": u.username, "password": u.password, "verified": True}).count() > 0

    #
    def get_uid(self):
        u = self.user
        doc = self.userDB.find_one({"username": u.username, "password": u.password})
        return str(doc["_id"])

    # post a tweet
    # @TODO worry about retweet
    def post_tweet(self):
        t = self.tweet
        tweet_document = {
            "uid": t.uid,
            "username": t.uname,
            "content": t.content,
            "tweetstamp": int(time.time()),
            "likes": 0,
            "retweets": 0
        }
        if (t.parent != None):
            tweet_document["parent"] = t.parent
        if (t.media != None):
            tweet_document["media"] = t.media
        # if i have parent tweets i should...
        return str(self.tweetsDB.insert(tweet_document))

    # increase number of tweet likes by one
    def like_tweet(self, tid, uid):
        lmodel = self.like
        # this code has bugs on update (fix later)
        # like_document = self.likesDB.find_one({"uid": uid, "tid": tid})
        # if like_document != None:
        #     if like_document["liked"] == "true" and lmodel.like == True:
        #             return
        #     elif like_document["liked"] == "false" and lmodel.like == False:
        #             return
        #     self.likesDB.update_one({"uid": uid, "tid": tid}, {"liked": "true" if lmodel.like == True else "false"})
        # else:
        #     self.likesDB.insert({"uid": uid, "tid": tid, "liked": "true" if lmodel.like == True else "false"})
        amount = 1 if lmodel.like == True else -1
        self.tweetsDB.update({'_id': ObjectId(tid)}, {'$inc': {'likes': amount}})

    # individual tweet search
    def retrieve_tweet(self, id):
        t = self.tweetsDB.find_one({"_id": ObjectId(id)})
        if t is None:
            return {
                "status": "error",
                "error": "Id does not exist"
            }

        tweet_response = {
            "status": "OK",
            "item": {
            "id": str(t["_id"]),
            "username": t["username"],
            "content": t["content"],
            "timestamp": t["tweetstamp"],
            "media": t.get("media", [])
            }
        }
        if t.get("parent", None) != None:
            tweet_response["item"]["parent"] = t["parent"]
        return tweet_response


    # deletes tweet associated with id
    # returns True if able to delte completely, False ow
    def delete_tweet(self, id):
        tweet_doc = self.tweetsDB.find_one({"_id": ObjectId(id)})
        if tweet_doc == None:
            return False
        # delete tweet
        self.tweetsDB.delete_one({"_id": ObjectId(id)})
        # retrieve media array (if necessary)
        media_array = tweet_doc.get("media", None)
        if media_array == None:
            self.tweetsDB.delete_one({"_id": ObjectId(id)})
        else:
            # remove all media associated with tweet
            for media in media_array:
                self.mediaDB.delete_one({"_id": ObjectId(media)})
        return True

    # search query
    def tweetsearch(self, loggedin_username):
        searchmodel = self.search
        results = {
            "status": "OK",
            "items": []
        }
        # filter by username
        # if searchmodel.username != None:
        #     return searchDelegate.search_username(searchmodel=searchmodel,tweetsDB=self.tweetsDB,results=results)
        # filter by users that the logged in user is following
        # if searchmodel.following == True:
        #     return searchDelegate.search_following(loggedin_username=loggedin_username,followsDB=self.followsDB,tweetsDB=self.tweetsDB,searchmodel=searchmodel,results=results)
        # else:
            # don't filter by users that user is following
            # if query string is specified
            # return searchDelegate.search_not_following(tweetsDB=self.tweetsDB, searchmodel=searchmodel, results=results)


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

    # save media file
    def save_media(self, f):
        content = f.read()
        return str(self.mediaDB.insert({
            "content": Binary(content)
        }))

    # retrieves media
    def get_media(self, mid):
        media = self.mediaDB.find_one({"_id": ObjectId(mid)})
        return media["content"]

    # close mongo connection
    def close(self):
        self.client.close()
