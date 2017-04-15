from django.shortcuts import get_object_or_404, render

# testing only /test/homepage
def homepage(request):
    context = {
        'greeting': "WELCOME TO CHIRP CHIRP",
        'username': "hardcodedUser95"
    }
    return render(request, "chirpchirp/homepage.html", context)
    
# testing only /test/homepage
def index(request):
    return render(request, "chirpchirp/index.html")
