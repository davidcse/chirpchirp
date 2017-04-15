#!/usr/bin/env bash



# script to set up an app server, will be responsible for downloading project, running uwsgi and nginx

# script variables
project_repo="https://github.com/elvis-alexander/chirpchirp"
project_dest="/home/ubuntu/"
seperator="---------------------"

# clone repo
echo $seperator "Cloning Project" $seperator
git clone $project_repo $project_dest

# install nginx
echo $seperator "Updating apt-get pm" $seperator
sudo apt-get update
echo $seperator "Installing Nginx" $seperator
sudo apt-get install nginx

# confingure nginx
#sudo uwsgi --http :80 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 4 --threads 1

# run nginx
echo $seperator "Stopping nginx (if necessary)" $seperator
sudo service nginx stop
echo $seperator "Starting nginx" $seperator
sudo service nginx start
echo $seperator "Nginx status" $seperator
sudo service nginx status
