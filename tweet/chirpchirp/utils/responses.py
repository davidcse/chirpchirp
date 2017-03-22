from django.http import JsonResponse


def returnresp(obj):
    return JsonResponse(obj)


def ok_response():
    return JsonResponse({"status": "OK"})

def redirect_ok_response(url):
    return JsonResponse({"status": "OK","redirect": url})

def err_response(errmsg):
    return JsonResponse({
            "status": "error",
            "error": errmsg
    })


def tweet(tid):
    return JsonResponse({
        "status": "OK",
        "id": tid
    })
