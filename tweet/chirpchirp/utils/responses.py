from django.http import JsonResponse


def returnresp(obj):
    return JsonResponse(obj)


def ok_response():
    return JsonResponse({"status": "OK"})


def err_response(errmsg):
    return JsonResponse({
            "status": "ERROR",
            "error": errmsg
    })


def tweet(tid):
    return JsonResponse({
        "status": "OK",
        "id": tid
    })
