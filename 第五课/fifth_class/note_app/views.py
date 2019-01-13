import json
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse


# Create your views here.


def note(request):
    return render(request, 'note.html')


def login(request):
    if "POST" == request.method:
        body = request.body
        res = json.loads(body)
        if "user" not in res and "pwd" not in res:
            return JsonResponse({"success": False}, safe=False)
        user = res["user"]
        pwd = res["pwd"]
        if "admin" == user and "password" == pwd:
            return JsonResponse({"success": True}, safe=False)
        return JsonResponse({"success": False}, safe=False)
    else:
        return HttpResponse(status=404)


def register(request):
    if "POST" == request.method:
        body = request.body
        res = json.loads(body)
        if "user" not in res and "pwd" not in res:
            return JsonResponse({"success": False}, safe=False)
        user = res["user"]
        pwd = res["pwd"]
        if "admin" == user and "password" == pwd:
            return JsonResponse({"success": True}, safe=False)
        return JsonResponse({"success": False}, safe=False)
    else:
        return HttpResponse(status=404)
