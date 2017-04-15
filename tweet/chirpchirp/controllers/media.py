from .. utils import responses
from django.views.decorators.csrf import csrf_exempt
from .. db.tweetdb import tweetdb
from django.http import HttpResponse

@csrf_exempt
def add_media(request):
    f = request.FILES['content']
    db = tweetdb()
    mid = db.save_media(f)
    db.close()
    return responses.id_response(mid)

@csrf_exempt
def retrieve(request, id):
    db = tweetdb()
    content = db.get_media(id)
    db.close()
    r = HttpResponse(content)
    r["Content-Type"] = "image/jpg"
    return r
