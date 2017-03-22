from .. db import tweetdb
from .. utils import responses
from .. models import tweetmodel
from .. models import searchmodel
from django.views.decorators.csrf import csrf_exempt


# creates a new tweet {content}
@csrf_exempt
def additem(request, id):
    uid = request.session.get("uid", None)
    uname = request.session.get("uname", None)
    if uid is None:
        return responses.error("Please login before adding item")
    t = tweetmodel.tweetmodel(uname, uid, request)
    if len(t.content) > 140:
        return responses.error("Please make sure contents is at most 140 characters long")
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
def search(request):
    tsearch = searchmodel.searchmodel(request)
    db = tweetdb(search=tsearch)
    r = db.tweetsearch()
    db.close()
    return responses.returnresp(r)
