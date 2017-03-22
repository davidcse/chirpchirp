from .. utils import responses
from .. db.tweetdb import tweetdb
from .. models.tweetmodel import tweetmodel
from .. models.searchmodel import searchmodel
from django.views.decorators.csrf import csrf_exempt


# creates a new tweet {content}
@csrf_exempt
def additem(request):
    uid = request.session.get("uid", None)
    uname = request.session.get("uname", None)
    if uid is None:
        return responses.err_response("Please login before adding item")
    t = tweetmodel(uname, uid, request)
    if len(t.content) > 140:
        return responses.err_response("Please make sure contents is at most 140 characters long")
    db = tweetdb(tweet=t)
    tid = db.posttweet()
    db.close()
    return responses.tweet(tid)


# returns tweet from id (<int:id>) for int
@csrf_exempt
def item(request, id):
    db = tweetdb()
    r = db.itemsearch(id)
    db.close()
    return responses.returnresp(r)


# {timestamp, limit}
@csrf_exempt
def search(request):
    tsearch = searchmodel(request)
    db = tweetdb(search=tsearch)
    r = db.tweetsearch()
    db.close()
    return responses.returnresp(r)
