import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


# Create your views here.

def demo1(request):
    return render(request, 'demo1.html')

def demo2(request):
    return render(request, 'demo2.html')

data = [
    "apple",
    "banana",
    "orange",
    "lemon",
    "pear",
]

def search(request):
    method = request.method
    if "POST" == method:
        body = json.loads(request.body)
        if "key" not in body:
            return JsonResponse([], safe=False)
        key = body["key"]
        ret = []
        for i in data:
            if key in i:
                ret.append(i)
        return JsonResponse(ret, safe=False)
    else:
        return HttpResponse(status=404)
