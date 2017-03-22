from django.http import JsonResponse


def returnresp(app, obj):
    return JsonResponse(obj)


def ok_response():
    return JsonResponse({"status": "OK"})


def err_response(errmsg):
    return JsonResponse({
            "status": "error",
            "error": errmsg
    })


def tweet(app, tid):
    return JsonResponse({
        "status": "OK",
        "id": tid
    })