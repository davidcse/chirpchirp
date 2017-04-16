# chirpchirp




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
ps -ax | grep uwsgi