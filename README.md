# chirpchirp

#dependencies before running:
memcached
mongodb
nginx(production)


sudo apt-get install python2.7-dev
sudo apt-get install python-pip
sudo pip install uwsgi
sudo uwsgi --http :80 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 4 --threads 1

```
source bin/activate
cd tweet
python manage.py runserver
```

Start testing locally

http://localhost:8000/login
<br>
http://localhost:8000/...


<br>
Some Memached Stuff<br>
service memcached start<br>
telnet 127.0.0.1 11211<br>


view logs<br>
cat /var/log/memcached.log<br>
sudo vim /etc/memcached.conf<br>

<br>
Setup for NGINX load balancer, by default will do round robin

sudo nano /etc/nginx/sites-available/default<br>
cat /var/log/nginx/error.log<br>

upstream django_webservers {
        server 130.245.168.162;
        #server IP;
}
<br>
server {
        listen 80;
        location / {
                proxy_pass http://django_webservers;
        }
}
<br>
uname -n | sudo tee /usr/share/nginx/html/index.html


<br>

sudo mongod status
sudo mongod start
sudo mongod status
use tweet

tweet.user.find({})
tweet.tweets.find({})



Config for mongodb
0.0.0.0 (any host)
or
specify host

sudo pip install django
sudo pip install pymongo
sudo pip install python-memcached
<br>

Using uwsgi,
sudo python manage.py runserver 0.0.0.0:80
sudo uwsgi --http :80 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 4 --threads 1

sudo python manage.py runserver 0.0.0.0:8000
sudo uwsgi --http :8000 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 1 --threads 1


# MongoDB sharding
user: {_id, username, password, verified, email}<br>
tweets: {_id, username, content, uid, tweetstamp}<br>
follows: {_id, username, follower_username}
