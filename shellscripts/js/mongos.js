sh.enableSharding("tweet");
sh.shardCollection("tweet.user", {"username": 1});
sh.shardCollection("tweet.tweets", {"username": 1})
sh.shardCollection("tweet.follows", {"follower_username": 1});
sh.shardCollection("tweet.media", {"_id": 1})
sh.shardCollection("tweet.likes", {"uid": 1})
sh.status();
