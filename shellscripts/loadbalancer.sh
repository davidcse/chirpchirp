#!/usr/bin/env bash

# chmod +x loadbalancer.sh
# USAGE: ./loadbalancer.sh IP_ONE IP_TWO IP_THREE IP_FOUR

loadbalancer_conf="https://github.com/elvis-alexander/chirpchirp/blob/master/nginxconfig/chirp_nginx.conf"
seperator="---------------------"

echo $seperator "Downloading nginx config" $seperator
wget $loadbalancer_conf

# /home/ubuntu/chirpchirp/nginx

# setting nginx config file
echo $seperator "Setting up config file..." $seperator
sed -ie 's/IP_ONE/'$1'/g' loadbalancer.conf
sed -ie 's/IP_TWO/'$2'/g' loadbalancer.conf
sed -ie 's/IP_THREE/'$3'/g' loadbalancer.conf
sed -ie 's/IP_FOUR/'$4'/g' loadbalancer.conf

# install nginx
#echo $seperator "Updating apt-get" $seperator
#sleep 2
#sudo apt-get update
#echo $seperator "Installing Nginx" $seperator
#sleep 2
#sudo apt-get install nginx

# moving config to correct directory


#