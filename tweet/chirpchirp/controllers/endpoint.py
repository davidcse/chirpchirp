from django.shortcuts import get_object_or_404, render


def testhomepage(request):
    context = {'greeting': "WELCOME TO CHIRP CHIRP"}
    return render(request, "chirpchirp/homepage.html", context)


def testindex(request):
    return render(request, "chirpchirp/index.html")
