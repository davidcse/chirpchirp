#!/usr/bin/env bash



mkdir mongo
mkdir mongo/mongo_logs
mkdir mongo/shard
mkdir mongo/shard/shard1
mkdir mongo/shard/shard2

mongod --shardsvr --replSet shard1 --dbpath /home/ubuntu/mongo/shard/shard1a --bind_ip 192.168.1.37 --port 27040 --logpath /home/ubuntu/mongo/mongo_logs/shard1a.log --logappend --fork
mongod --shardsvr --replSet shard1 --dbpath /home/ubuntu/mongo/shard/shard1b --bind_ip 192.168.1.37 --port 27041 --logpath /home/ubuntu/mongo/mongo_logs/shard1b.log --logappend --fork
mongod --bind_ip 192.168.1.37 --port 27017 --dbpath /home/ubuntu/db --logpath /home/ubuntu/log/user.log --logappend --fork


mongo --host 192.168.1.37 --port 27018


#rs.initiate()
#rs.add("192.168.1.37:27041")