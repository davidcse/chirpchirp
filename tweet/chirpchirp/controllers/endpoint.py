from django.shortcuts import render
from .. utils import auth

def homepage(request):
    username = request.session.get("uname", "defaultuser")
    context = {
        'greeting': "Welcome to Chirp Chirp",
        'username': username
    }
    return render(request, "chirpchirp/homepage.html", context)

#send user to login page
def index(request):
    if(auth.auth_session(request)):
        return homepage(request) # foreward to homepage rendering.
    else:
        return render(request, "chirpchirp/index.html")
