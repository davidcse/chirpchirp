#!/usr/bin/env bash
# make four shard with three replicate set each
mkdir a0
mkdir a1
mkdir a2
mkdir b0
mkdir b1
mkdir b2
mkdir c0
mkdir c1
mkdir c2
mkdir d0
mkdir d1
mkdir d1

# directory for configuration servers
mkdir cfg0
mkdir cfg1
mkdir cfg2

# start config servers
mongod --configsvr --dbpath cfg0 --port 26050 --fork --logpath log.cfg0 --logappend
mongod --configsvr --dbpath cfg1 --port 26051 --fork --logpath log.cfg1 --logappend
mongod --configsvr --dbpath cfg2 --port 26052 --fork --logpath log.cfg2 --logappend

# create shard servers with replica sets

# create a shard
mongod --shardsvr --replSet a --dbpath a0 --logpath log.a0 --port 27000 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet a --dbpath a1 --logpath log.a1 --port 27001 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet a --dbpath a2 --logpath log.a2 --port 27002 --fork --logallfiles --oplogSize 50
# create b shard
mongod --shardsvr --replSet b --dbpath b0 --logpath log.b0 --port 27100 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet b --dbpath b1 --logpath log.b1 --port 27101 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet b --dbpath b2 --logpath log.b2 --port 27102 --fork --logallfiles --oplogSize 50
# create c shard
mongod --shardsvr --replSet c --dbpath c0 --logpath log.c0 --port 27200 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet c --dbpath c1 --logpath log.c1 --port 27201 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet c --dbpath c2 --logpath log.c2 --port 27202 --fork --logallfiles --oplogSize 50
# create d shard
mongod --shardsvr --replSet d --dbpath d0 --logpath log.d0 --port 27300 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet d --dbpath d1 --logpath log.d1 --port 27301 --fork --logallfiles --oplogSize 50
mongod --shardsvr --replSet d --dbpath d2 --logpath log.d2 --port 27302 --fork --logallfiles --oplogSize 50


# start mongos processes linking configuration databases
mongos --configdb 10gen.local:26050,10gen.local:26051,10gen.local:26052 --fork --logallfiles
mongos --configdb 10gen.local:26050,10gen.local:26051,10gen.local:26052 --fork --logallfiles --port 26061
mongos --configdb 10gen.local:26050,10gen.local:26051,10gen.local:26052 --fork --logallfiles --port 26062
mongos --configdb 10gen.local:26050,10gen.local:26051,10gen.local:26052 --fork --logallfiles --port 26063

# echo processes
ps -A | grep mongo

# echo log files for configs
echo
tail -n 1 log.cfg0
tail -n 1 log.cfg1
tail -n 1 log.cfg2


# echo log files for shards
echo
tail -n 1 log.a0
tail -n 1 log.a1
tail -n 1 log.a2
tail -n 1 log.b0
tail -n 1 log.b1
tail -n 1 log.b2
tail -n 1 log.c0
tail -n 1 log.c1
tail -n 1 log.c2
tail -n 1 log.d0
tail -n 1 log.d1
tail -n 1 log.d2

echo
tail -n 1 log.mongos0
tail -n 1 log.mongos1
tail -n 1 log.mongos2
tail -n 1 log.mongos3