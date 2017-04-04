from django.shortcuts import render
from .. utils import auth
from .. db.tweetdb import tweetdb

# For unauthenticated users, redirect to standard index page.
def defaultpage(request):
    return render(request, "chirpchirp/index.html")


# Page used to render profile cards of other users to follow.
def followpage(request):
    if not auth.auth_session(request):
        return defaultpage(request)
    return render(request,"chirpchirp/followpage.html")


def homepage(request):
    if not auth.auth_session(request):
        return defaultpage(request)
    # render template based on user's data
    username = request.session.get("uname", "")
    db = tweetdb()
    results = db.retrieve_user(username)
    follower_count, following_count = 0,0
    if(results):
        follower_count = follower_count
        following_count = following_count
    context = {
        'username': username,
        'follower_count':follower_count,
        'following_count':following_count
    }
    return render(request, "chirpchirp/homepage.html", context)

#send user to login page
def index(request):
    if(not auth.auth_session(request)):
        return defaultpage(request)
    # foreward to homepage rendering.
    return homepage(request)
