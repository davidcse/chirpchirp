from .. utils import responses
from .. db.tweetdb import tweetdb
from .. models.usermodel import usermodel
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# /adduser {username, email, password}
# no bad result maybe if username already exists
@csrf_exempt
def adduser(request):
    u = usermodel(request)
    db = tweetdb(user=u)
    # actually add user here
    db.insertdisable()
    db.close()
    return responses.ok_response()


# /verify {email, key}
# no check to see if a user with this email
@csrf_exempt
def verify(request):
    u = usermodel(request)
    db = tweetdb(user=u)
    db.verifyuser()
    db.close()
    return responses.ok_response()


# login resource (username, password)
@csrf_exempt
def login(request):
    # used to login
    u = usermodel(request)
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

# logout {}
@csrf_exempt
def logout(request):
    try:
        del request.session['username']
        del request.session['convo_id']
        return responses.ok_response()
    except KeyError:
        return responses.err_response("Please login, before logging out")
