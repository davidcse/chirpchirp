#!/usr/bin/env bash

# chmod +x mongos.sh
# USAGE: ./mongoconf.sh {host_ip} {host_port}

# script variables
seperator="---------------------"
host_ip=$1
# 27030
host_port=$2


echo $seperator "Installing MongoDB" $seperator
sleep 2
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
sudo echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# creating directories
echo $seperator "Creating config directories" $seperator
sleep 2
mkdir mongo
mkdir mongo/mongo_logs
mkdir mongo/config/conf

# running mongo config server
echo $seperator "Running config server" $seperator
sleep 2
mongod --configsvr --replSet conf --dbpath ~/mongo/config/conf --bind_ip $host_ip --port $host_port --logpath ~/mongo/mongo_logs/conf.log --fork
#mongod --configsvr --replSet conf --dbpath ~/mongo/config/conf --bind_ip $host_ip --port $host_port --logpath ~/mongo/mongo_logs/conf.log --fork
