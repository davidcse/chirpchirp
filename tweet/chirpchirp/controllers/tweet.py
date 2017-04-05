from .. utils import responses
from .. db.tweetdb import tweetdb
from .. models.tweetmodel import tweetmodel
from .. models.searchmodel import searchmodel
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# creates a new tweet {content}
@csrf_exempt
def additem(request):
    uid = request.session.get("uid", None)
    uname = request.session.get("uname", None)
    if uid is None:
        return responses.err_response("Please login before adding item")
    t = tweetmodel(uname, uid, request)
    db = tweetdb(tweet=t)
    tid = db.posttweet()
    db.close()
    return responses.tweet(tid)


# /item/<id> retrieve/delete
@csrf_exempt
def item(request, id):
    db = tweetdb()
    if request.method == "DELETE":
        delete_response = db.delete_tweet(id)
        db.close()
        return HttpResponse(delete_response)
    # insert tweet on POST request
    r = db.itemsearch(id)
    db.close()
    return responses.returnresp(r)


# {timestamp, limit}
@csrf_exempt
def search(request):
    uname = request.session.get("uname", None)
    if uname is None:
        return responses.err_response("Please using search")
    tsearch = searchmodel(request)
    db = tweetdb(search=tsearch)
    r = db.tweetsearch(loggedin_username=uname)
    db.close()
    return responses.returnresp(r)
