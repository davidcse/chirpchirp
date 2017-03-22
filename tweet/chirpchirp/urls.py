from django.conf.urls import url
from controllers import user
from controllers import tweet

urlpatterns = [
    url('^adduser', user.adduser, name="adduser"),
    url('^verify', user.verify, name="verify"),
    url('^login', user.login, name="login"),
    url('^logout', user.logout, name="logout"),
    url('^item/(?P<id>[0-9]+)/$', tweet.item, name="item"),

]