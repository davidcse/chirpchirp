from .. db import tweetdb
from .. utils import responses
from .. models import usermodel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def adduser(request):
    u = usermodel(request)
    db = tweetdb(user=u)
    # actually add user here
    db.insertdisable()
    db.close()
    return responses.ok_response()


@csrf_exempt
def verify(request):
    u = usermodel(request)
    db = tweetdb(user=u)
    db.verifyuser()
    db.close()
    return responses.ok_response()

@csrf_exempt
def login(request):
    # used to login
    u = usermodel.usermodel(request)
    db = tweetdb(user=u)
    # verify user and account details
    if db.isverified() == False:
        db.close()
        return responses.err_response("Not Verified")
    # store cookie/session
    request.session["uid"] = db.getuid()
    request.session["uname"] = u.username
    db.close()
    return responses.ok_response()


@csrf_exempt
def logout(request):
    try:
        del request.session['username']
        del request.session['convo_id']
        return responses.ok_response()
    except KeyError:
        return responses.err_response("Please login, before logging out")
