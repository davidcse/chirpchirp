from django.conf.urls import url
from controllers import user
from controllers import tweet
from controllers import endpoint


urlpatterns = [
    # /adduser
    url(r'^adduser$', user.adduser, name="adduser"),
    # /verify
    url(r'^verify$', user.verify, name="verify"),
    # /login
    url(r'^login$', user.login, name="login"),
    # /logout
    url(r'^logout$', user.logout, name="logout"),
    # /additem
    url(r'^additem$', tweet.additem, name='additem'),
    # /item/123
    url(r'^item/(?P<id>[0-9]+)$', tweet.item, name="item"),
    # /search
    url(r'^search$', tweet.search, name="search"),


    # /testhomepage
    url(r'^testhomepage$', endpoint.testhomepage, name="testhomepage"),
    # /testhomepage
    url(r'^testindex$', endpoint.testindex, name="testindex"),
]
