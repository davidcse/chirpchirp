#################################################################
#   DELEGATOR THAT PERFORMS THE DETAILS OF THE SEARCH PROCESS
################################################################

def insert_tweet_nonrepeat(tweet,results):
    if tweet["content"] not in results["items"]:
        results["items"].append({
        "id": str(tweet["_id"]),
        "username": tweet["username"],
        "content": tweet["content"],
        "timestamp": tweet["tweetstamp"]
    })



def search_following(loggedin_username, followsDB, tweetsDB, searchmodel, results):
    # get users logged in user is following
    following_users = followsDB.find({"follower_username": loggedin_username}).limit(searchmodel.limit)
    for user in following_users:
        # if query string is specified fix hereeeee
        for word in searchmodel.q:
            if word != ".*":
                word = r"\b{}\b".format(word)
            tweets = self.tweetsDB.find({"content": {"$regex": word}, "username": user["username"], "tweetstamp": {"$lte": searchmodel.tweetstamp}}).limit(searchmodel.limit)
            for tweet in tweets:
                if len(results["items"]) >= searchmodel.limit:
                    break
                insert_tweet_nonrepeat(tweet,results)



# don't filter by users that user is following
# if query string is specified
def search_not_following(tweetsDB, searchmodel,results):
    for word in searchmodel.q:
        if word != ".*":
            word = r"\b{}\b".format(word)
        tweets = tweetsDB.find({"content": {"$regex": word},"tweetstamp": {"$lte": searchmodel.tweetstamp}}).limit(searchmodel.limit)
        for tweet in tweets:
            if len(results["items"]) >= searchmodel.limit:
                break
            insert_tweet_nonrepeat(tweet,results)



def search_username(tweetsDB, searchmodel,results):
    print 'filtering by username: ', searchmodel.username
    for word in searchmodel.q:
        if word != ".*":
            word = r"\b{}\b".format(word)
        filtered_tweets = self.tweetsDB.find({"username": searchmodel.username, "content": {"$regex": word}, "tweetstamp": {"$lte": searchmodel.tweetstamp}}).limit(searchmodel.limit)
        for tweet in filtered_tweets:
            if len(results["items"]) >= searchmodel.limit:
                return results
            insert_tweet_nonrepeat(tweet,results)
