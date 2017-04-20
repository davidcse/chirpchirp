#!/usr/bin/env bash

# chmod +x mongoshard.sh
# USAGE: ./mongoshard.sh

# script variables
host_ip=$1
host_port=$2
seperator="---------------------"
sleep_limit=5
mongoshard_js="https://raw.githubusercontent.com/elvis-alexander/chirpchirp/master/shellscripts/js/mongoshard.js"

# installing mongodb
echo $seperator "Installing MongoDB" $seperator
sleep $sleep_limit
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
sudo echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# creating directories
echo $seperator "Creating config directories" $seperator
sleep $sleep_limit
mkdir mongo
mkdir mongo/mongo_logs
mkdir mongo/shard

# running shard
echo $seperator "Running Shard" $seperator
sleep $sleep_limit
mongod --shardsvr --replSet shard1 --dbpath /home/ubuntu/mongo/shard/ --bind_ip $host_ip --port $host_port --logpath /home/ubuntu/mongo/mongo_logs/shard.log --logappend --fork
#(Ignore) mongod --bind_ip 192.168.1.37 --port 27017 --dbpath /home/ubuntu/db --logpath /home/ubuntu/log/user.log --logappend --fork

# retrieving js file
echo $seperator "Wget js file" $seperator
sleep $sleep_limit
wget $mongoshard_js

# feeding js input
echo $seperator "Feeding js input" $seperator
sleep $sleep_limit
mongo --host 192.168.1.37 --port 27018 < mongshard.js