# chirpchirp

#dependencies before running:
memcached
mongodb
nginx(production)




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

Using uwsgi,
sudo python manage.py runserver 0.0.0.0:80
sudo uwsgi --http :80 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 4 --threads 1

sudo python manage.py runserver 0.0.0.0:8000
sudo uwsgi --http :8000 --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 1 --threads 1


# MongoDB sharding
user: {_id, username, password, verified, email}<br>
tweets: {_id, username, content, uid, tweetstamp}<br>
follows: {_id, username, follower_username}




ps -ax | grep uwsgi
