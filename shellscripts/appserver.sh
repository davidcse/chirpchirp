#!/usr/bin/env bash
# chmod +x appserver.sh

# script to set up an app server, will be responsible for downloading project, running uwsgi and nginx

# script variables
project_repo="https://github.com/elvis-alexander/chirpchirp"
seperator="---------------------"

# install git
echo $seperator "Installing Git" $seperator
sudo apt-get update
sleep 2
sudo apt-get install git
sleep 2

# clone repo
echo $seperator "Cloning Project" $seperator
git clone $project_repo
sleep 2

# install all project dependencies (python related)
echo $seperator "Update apt-get" $seperator
sudo apt-get update
sleep 2
echo $seperator "Installing python-dev" $seperator
sudo apt-get install python2.7-dev
sleep 2
echo $seperator "Installing python-pip" $seperator
sudo apt-get install python-pip
sleep 2

# activate virtualenv
echo $seperator "Activate virtual-env" $seperator
cd chirpchirp
source bin/activate
echo $seperator "Moving to /chirpchirp/tweet dir" $seperator
cd tweet
echo $seperator "Installing uwsgi" $seperator
sudo pip install uwsgi
sleep 2
echo $seperator "Installing django" $seperator
sudo pip install django
sleep 2
echo $seperator "Installing pymongo" $seperator
sudo pip install pymongo
sleep 2
echo $seperator "Installing memcached" $seperator
sudo pip install python-memcached
sleep 2

# install nginx
echo $seperator "Updating apt-get" $seperator
sudo apt-get update
sleep 2
echo $seperator "Installing Nginx" $seperator
sudo apt-get install nginx
sleep 2

# confingure nginx
echo $seperator "Launching uwsgi" $seperator
#sudo uwsgi --socket /home/ubuntu/chirp.sock --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 10 --threads 2 --chmod-socket=666 --logto /home/ubuntu/uwsgi.log --daemonize /home/ubuntu/daemonize.log
sudo uwsgi --socket /home/ubuntu/chirp.sock --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 1 --threads 1 --chmod-socket=666 --logto /home/ubuntu/uwsgi.log --daemonize /home/ubuntu/daemonize.log
sleep 2
echo $seperator "Connecting nginx to uwsgi" $seperator
sudo ln -s /home/ubuntu/chirpchirp/nginxconfig/chirp_nginx.conf /etc/nginx/sites-enabled/
sleep 2

# run nginx
echo $seperator "Restarting nginx" $seperator
sudo service nginx restart
sleep 2
echo $seperator "Nginx Status" $seperator
sudo service nginx status
sleep 2
