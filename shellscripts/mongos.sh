#!/usr/bin/env bash

# chmod +x mongos.sh
# USAGE: ./mongos.sh {host_ip} {config_ip} {config_port}

# script variables
seperator="---------------------"
host_ip=$1
config_ip=$2
config_port=$3


echo $seperator "Installing MongoDB" $seperator
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
sudo echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# creating directories
echo $seperator "Creating config directories" $seperator
sleep 2
mkdir mongo
mkdir mongo/mongo_logs

# configuring mongos
echo $seperator "Running Mongos" $seperator
sleep 2
mongos --configdb conf/$config_ip:$config_port --bind_ip $host_ip --port 27017 --logpath /home/ubuntu/mongo/mongo_logs/mongos.log --logappend --fork
#mongos --configdb conf/192.168.1.39:27030 --bind_ip 192.168.1.32 --port 27017 --logpath /home/ubuntu/mongo/mongo_logs/mongos.log --logappend --fork
#(example w multiple configs) mongos --configdb conf/192.168.1.39:27030,192.168.1.39:27020 --bind_ip 192.168.1.32 --port 27017 --logpath /home/ubuntu/mongo/mongo_logs/mongos.log --logappend --fork

# connect mongo client
mongo --host $host_ip --port 27017 < mongos.js
