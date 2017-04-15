from .. utils import responses
from .. db.tweetdb import tweetdb
from .. models.tweetmodel import tweetmodel
from .. models.searchmodel import searchmodel
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .. utils import auth


# creates a new tweet {content}
@csrf_exempt
def additem(request):
    if not auth.auth_session(request):
        return responses.err_response("Please login before adding item")
    uname = request.session.get("uname","")
    uid = request.session.get("uid","")
    t = tweetmodel(uname, uid, request)
    db = tweetdb(tweet=t)
    tid = db.posttweet()
    db.close()
    return responses.id_response(tid)


# /item/<id> retrieve/delete
@csrf_exempt
def item(request, id):
    db = tweetdb()
    if request.method == "DELETE":
        delete_response = db.delete_tweet(id)
        db.close()
        if delete_response == "Failure":
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    # insert tweet on POST request
    r = db.itemsearch(id)
    db.close()
    return responses.returnresp(r)


# {timestamp, limit}
@csrf_exempt
def search(request):
    if not auth.auth_session(request):
        return responses.err_response("Please log in before using search")
    uname = request.session.get("uname", "")
    tsearch = searchmodel(request)
    db = tweetdb(search=tsearch)
    r = db.tweetsearch(loggedin_username=uname)
    db.close()
    return responses.returnresp(r)
