# chirpchirp

#dependencies before running:
memcached
mongodb
nginx(production)

# PRODUCTION vs DEV
In settings tweet folder /tweet/settings.py
In application chirpchirp folder /chirpchirp/config/settings.py
Change the variable PRODUCTION = True or False for both files.


#####################################<br>
loadbalancer ip: {130.245.169.41} {mongos: port: {27017}, memcached: port: {11211}}
config ip: {192.168.1.49} port: {27030}
shard1 ip: {192.168.1.45} port: {27040}
shard2 ip: {192.168.1.46} port: {27040}
shard3 ip: {192.168.1.47} port: {27040}
shard4 ip: {192.168.1.48} port: {27040}
appserver1 ip: {192.168.1.55}
appserver2 ip: {192.168.1.51}
appserver3 ip: {192.168.1.52}
appserver4 ip: {192.168.1.53}

27017, 11211, 27030, 27040, 8080, 80

<!---->
Things to question:<br>
If i delete a retweet should the number of retweets for that tweet go down by one


/etc/sysctl.conf
fs.file-max = 500000
sudo sysctl --system
ulimit -f unlimited -t unlimited -v unlimited -n 64000 -m unlimited -u 64000
ulimit -f
sysctl -a

http://stackoverflow.com/questions/22697584/nginx-uwsgi-104-connection-reset-by-peer-while-reading-response-header-from-u

uwsgi --socket /home/ubuntu/chirp.sock --wsgi-file /home/ubuntu/chirpchirp/tweet/tweet/wsgi.py --master --processes 4 --threads 1 --chmod-socket=666 --logto /home/ubuntu/uwsgi.log --daemonize /home/ubuntu/daemonize.log


shards - {8}
appservers - {8}
loadbalancer - {1}
config - {1}
mongos - {2}

memcached server - {on appserver8}

-f (file size): unlimited
-t (cpu time): unlimited
-v (virtual memory): unlimited [1]
-n (open files): 64000
-m (memory size): unlimited [1] [2]
-u (processes/threads): 64000

ulimit -f unlimited
ulimit -t unlimited
ulimit -v unlimited
ulimit -n 64000
ulimit -m unlimited
ulimit -u unlimited



set up load balancer
set up ulimit
set up sysctl
set up shards
set up config
set up mongos1
set up mongos2

sysctl -p

Safety Checks:
ulimit -u;
sysctl fs.file-max;

mongos: {lb:}
memcache for app: {config}
memcache for sessions: {lb: }

shard1/192.168.1.70:27040
shard2/192.168.1.73:27040
shard3/192.168.1.76:27040
shard4/192.168.1.79:27040