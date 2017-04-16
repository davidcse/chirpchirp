#!/usr/bin/env bash
# chmod +x appserver.sh

# script to set up an app server, will be responsible for downloading project, running uwsgi and nginx

# script variables
project_repo="https://github.com/elvis-alexander/chirpchirp"
seperator="---------------------"

# install git
echo $seperator "Update apt-get" $seperator
sleep 2
sudo apt-get update
echo $seperator "Installing Git" $seperator
sudo apt-get install git

# clone repo
echo $seperator "Cloning Project" $seperator
sleep 2
git clone $project_repo

# install all project dependencies (python related)
echo $seperator "Update apt-get" $seperator
sleep 2
sudo apt-get update
echo $seperator "Installing python-dev" $seperator
sleep 2
sudo apt-get install python2.7-dev
echo $seperator "Installing python-pip" $seperator
sleep 2
sudo apt-get install python-pip

# activate virtualenv
echo $seperator "Activate virtual-env" $seperator
sleep 2
cd chirpchirp
source bin/activate
echo $seperator "Moving to /chirpchirp/tweet dir" $seperator
sleep 2
cd tweet
echo $seperator "Collecting static" $seperator
sleep 2
python manage.py collectstatic

echo $seperator "Installing uwsgi" $seperator
sleep 2
sudo pip install uwsgi
echo $seperator "Installing django" $seperator
sleep 2
sudo pip install django
echo $seperator "Installing pymongo" $seperator
sleep 2
sudo pip install pymongo
echo $seperator "Installing memcached" $seperator
sleep 2
sudo pip install python-memcached

# install nginx
echo $seperator "Updating apt-get" $seperator
sleep 2
sudo apt-get update
echo $seperator "Installing Nginx" $seperator
sleep 2
sudo apt-get install nginx

# confingure nginx
echo $seperator "Launching uwsgi" $seperator
sleep 2
#sudo uwsgi --socket /home/ubuntu/chirp.sock --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 10 --threads 2 --chmod-socket=666 --logto /home/ubuntu/uwsgi.log --daemonize /home/ubuntu/daemonize.log
sudo uwsgi --socket /home/ubuntu/chirp.sock --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 1 --threads 1 --chmod-socket=666 --logto /home/ubuntu/uwsgi.log --daemonize /home/ubuntu/daemonize.log
echo $seperator "Connecting nginx to uwsgi" $seperator
sleep 2
sudo ln -s /home/ubuntu/chirpchirp/nginxconfig/chirp_nginx.conf /etc/nginx/sites-enabled/

# run nginx
echo $seperator "Restarting nginx" $seperator
sleep 2
sudo service nginx restart
echo $seperator "Nginx Status" $seperator
sleep 2
sudo service nginx status
