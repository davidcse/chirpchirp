from django.conf.urls import url
from controllers import user
from controllers import tweet
from controllers import endpoint
from controllers import testEndpoint


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
    url(r'^item/(?P<id>[\w]+)$', tweet.item, name="item"),
    # /search
    url(r'^search$', tweet.search, name="search"),
    # /test/homepage
    url(r'^homepage$', endpoint.homepage, name="homepage"),
    # /index
    url(r'^$', endpoint.index, name="index"),

    # /test/homepage
    url(r'^test/homepage$', testEndpoint.homepage, name="testhomepage"),
    # /test/index
    url(r'^test/index$', testEndpoint.index, name="testindex")
]
