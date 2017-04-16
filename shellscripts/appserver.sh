#!/usr/bin/env bash



# script to set up an app server, will be responsible for downloading project, running uwsgi and nginx

# script variables
project_repo="https://github.com/elvis-alexander/chirpchirp"
project_dest="/home/ubuntu/"
seperator="---------------------"

# install git
echo $seperator "Installing Git" $seperator
sudo apt-get update
sudo apt-get install git

# clone repo
echo $seperator "Cloning Project" $seperator
git clone $project_repo $project_dest

# install all project dependencies (python related)
echo $seperator "Update apt-get" $seperator
sudo apt-get update
echo $seperator "Installing python-dev" $seperator
sudo apt-get install python2.7-dev
echo $seperator "Installing python-pip" $seperator
sudo apt-get install python-pip
echo $seperator "Installing uwsgi" $seperator
sudo pip install uwsgi

# install nginx
echo $seperator "Updating apt-get" $seperator
sudo apt-get update
echo $seperator "Installing Nginx" $seperator
sudo apt-get install nginx

# confingure nginx
#sudo uwsgi --http :80 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 4 --threads 1
uwsgi --socket chirp.sock --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 1 --threads 1
sudo ln -s /home/ubuntu/chirpchirp/nginxconfig/chirp_nginx.conf /etc/nginx/sites-enabled/


# run nginx
echo $seperator "Stopping nginx (if necessary)" $seperator
sudo service nginx stop
echo $seperator "Starting nginx" $seperator
sudo service nginx start
echo $seperator "Nginx status" $seperator
sudo service nginx status
