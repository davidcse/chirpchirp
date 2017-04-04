from .. utils import responses
from .. db.tweetdb import tweetdb
from .. models.followmodel import FollowModel
from django.views.decorators.csrf import csrf_exempt


# /follow {username, follow=True}
@csrf_exempt
def follow(request):
    uid = request.session.get("uid", None)
    uname = request.session.get("uname", None)
    print 'uid', uid
    print 'uname', uname
    if uid is None:
        return responses.err_response("Please login before following.")
    # get request model
    f_model = FollowModel(request=request)
    # connect to mongo
    db = tweetdb(follow=f_model)
    # perform database transaction
    db.follow_or_unfollow(uname)
    # close connection
    db.close()
    return responses.ok_response()


# /user/<username>
def user(request, username):
    db = tweetdb()
    r = db.retrieve_user(username)
    db.close()
    return responses.returnresp(r)


# /user/<username>/followers @Change
@csrf_exempt
def followers(request, username):
    limit = int(request.GET.get('limit', 50))
    if limit > 200:
        limit = 200
    db = tweetdb()
    r = db.get_followers(username, limit)
    db.close()
    return responses.returnresp(r)


# /user/<username>/following
@csrf_exempt
def following(request, username):
    limit = int(request.GET.get('limit', 50))
    if limit > 200:
        limit = 200
    db = tweetdb()
    r = db.get_following(username, limit)
    db.close()
    return responses.returnresp(r)
