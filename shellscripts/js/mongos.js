//verifying this is committed
use tweet;
sh.addShard("shard1/shard1_ip:27040");
sh.addShard("shard2/shard2_ip:27040");
sh.addShard("shard3/shard3_ip:27040");
sh.addShard("shard4/shard4_ip:27040");
sh.enableSharding("tweet");
sh.shardCollection("tweet.user", {"email": 1});
sh.shardCollection("tweet.tweets", {"username": 1})
sh.shardCollection("tweet.follows", {"follower_username": 1});
sh.shardCollection("tweet.media", {"_id": 1})
sh.shardCollection("tweet.likes", {"uid": 1, "tid": 1})
sh.status();