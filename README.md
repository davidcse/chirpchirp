# chirpchirp

#dependencies before running:
memcached
mongodb
nginx(production)





uname -n | sudo tee /usr/share/nginx/html/index.html

ps -ax | grep uwsgi


config
shard1 (done)
shard2
shard3
shard4
appserver1
appserver2
appserver3
appserver4
loadbalancer(mongos, memcached: {130.245.169.41:11211})
