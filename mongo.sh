#!/usr/bin/env bash
# 1 config servers (192.168.1.39, light weight) one machine (config/memcache)
# 2 shards replication 1 (2 machines, 192.168.1.37 and 192.168.1.38), 1 replication
# 1 mongos processes one machine (192.168.1.32/130.245.168.140, throw them in the load balancer, not going over network, well not really)

-------------------------
mkdir ~/mongo
mkdir ~/mongo/mongo_logs
mkdir ~/mongo/config
mkdir ~/mongo/config/conf
mkdir ~/mongo/config/conf1
# config servers store meta data for collections
mongod --configsvr --replSet conf --dbpath ~/mongo/config/conf --bind_ip 192.168.1.39 --port 27030 --logpath ~/mongo/mongo_logs/conf.log --fork
-------------------------
mkdir ~/mongo
mkdir ~/mongo/mongo_logs
mkdir ~/mongo/shard
mkdir ~/mongo/shard/shard1a
mkdir ~/mongo/shard/shard1b
mkdir ~/mongo/shard/shard2a
mkdir ~/mongo/shard/shard2b
# shard servers the actual data, there is only one replication per shard
# maybe a good idea to add more replicas in the future, if you need to change port use 27016
mongod --shardsvr --replSet shard1 --dbpath ~/mongo/shard/shard1a --bind_ip 192.168.1.37 --port 27040 --logpath ~/mongo/mongo_logs/shard1a.log --logappend
mongod --shardsvr --replSet shard1 --dbpath ~/mongo/shard/shard1b --bind_ip 192.168.1.37 --port 27041 --logpath ~/mongo/mongo_logs/shard1b.log --logappend

mongod --shardsvr --replSet shard2 --dbpath ~/mongo/shard/shard2a --bind_ip 192.168.1.38 --port 27040 --logpath ~/mongo/mongo_logs/shard2a.log --logappend
mongod --shardsvr --replSet shard2 --dbpath ~/mongo/shard/shard2b --bind_ip 192.168.1.38 --port 27041 --logpath ~/mongo/mongo_logs/shard2b.log --logappend
-------------------------
mkdir ~/mongo
mkdir ~/mongo/mongo_logs
# mongos (launch as many as you need in theory), for some reason the fork option wouldnt let me back into terminal
mongos --configdb conf/192.168.1.39:27030 --bind_ip 192.168.1.32 --port 27017 --logpath ~/mongo/mongo_logs/mongos.log --logappend --fork
mongos --configdb conf/192.168.1.39:27030 --bind_ip 192.168.1.32 --port 27017
-------------------------







rs.reconfig(
	{
    _id: "conf1",
    configsvr: true,
    members: [
      { _id : 0, host : "192.168.1.39:27019" },
      { _id : 1, host : "192.168.1.39:27020" },
    ]
  }
)

echo
ps -ax | grep mongo


# example of sharding collection:
# sh.shardCollection("week6.foo", {_id:1}, true)
# sh.shardCollection("week6.foo", {_id:1}, true)


# from mongos
# sh.addShard("shard1/192.168.1.37:27040")
# sh.addShard("shard2/192.168.1.38:27040")

# sh.enableSharding("tweet")
# db.user.insert({"username" : "eafernandez", "password" : "password", "verified" : true, "email" : "eafernandez@cs.stonybrook.edu"})
# db.user.insert({"username" : "aaa", "password" : "bbb", "verified" : true, "email" : "ccc"})

# db.tweets.createIndex({"username": 1})
# db.user.createIndex({"username":1})
# db.follows.createIndex({"follower_username": 1})
# db.tweets.getIndexes()
# sh.shardCollection("tweet.tweets", {"username": 1})
# sh.shardCollection("tweet.user", {"username": 1})
# sh.shardCollection("tweet.follows", {"follower_username": 1})


# from config server
# rs.initiate()
# attempted this but was too late
	# rs.initiate({ _id: "myReplSet", version: 1, members: [ { _id: 0, host: "192.168.1.39:27019"}, {_id: 1, host: "192.168.1.39:27020"}]})
# use config
# show collections
# db.shard.find()




