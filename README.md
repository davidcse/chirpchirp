# chirpchirp

#dependencies before running:
memcached
mongodb
nginx(production)





uname -n | sudo tee /usr/share/nginx/html/index.html

ps -ax | grep uwsgi<br>
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


@TODO shouldnt return media array on /item if no media loaded in the first place
sudo killall uwsgi
