from django.conf.urls import url
from controllers import user
from controllers import tweet
from controllers import views
from controllers import testEndpoint
from controllers import follow
from controllers import media

urlpatterns = [
    # /adduser
    url(r'^adduser/?$', user.adduser, name="adduser"),
    # /verify
    url(r'^verify/?$', user.verify, name="verify"),
    # /login
    url(r'^login/?$', user.login, name="login"),
    # /logout
    url(r'^logout/?$', user.logout, name="logout"),
    # /additem
    url(r'^additem/?$', tweet.additem, name='additem'),
    # /item/<id>
    url(r'^item/(?P<id>[\w]+)/?$', tweet.item, name="item"),
    # /search
    url(r'^search/?$', tweet.search, name="search"),
    # /follow
    url(r'^follow/?$', follow.follow, name="follow"),
    # /user/<username>
    url(r'^user/(?P<username>[\w\d]+)/?$', follow.user, name='user'),
    # /user/<username>/followers
    url(r'^user/(?P<username>[\w\d]+)/followers/?$', follow.followers, name='followers'),
    # /user/<username>/following
    url(r'^user/(?P<username>[\w\d]+)/following/?$', follow.following, name='following'),
    # adds media
    url(r'^addmedia', media.add_media, name='addmedia'),
    # retrieves media
    url(r'^media/(?P<id>[\w\d]+)?$', media.retrieve, name='media'),
    # /profile
    url(r'^profile/?$', views.searchprofilepage, name='searchprofilepage'),
    # /tweetsearch
    url(r'^tweetsearch/?$', views.tweetsearchpage, name='tweetsearchpage'),
    # /userpage
    url(r'^userpage/?$', views.userpage, name='userpage'),
    # /homepage
    url(r'^homepage$', views.homepage, name="homepage"),

    # /index
    url(r'^$', views.index, name="index"),

    # /test/homepage
    url(r'^test/homepage$', testEndpoint.homepage, name="testhomepage"),
    # /test/index
    url(r'^test/index$', testEndpoint.index, name="testindex")
]
