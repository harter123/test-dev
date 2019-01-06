import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

data = [
    "apple",
    "banana",
    "orange",
    "melons",
    "peach"
]

def index(request):
    return render(request, 'my_demo.html')


def search(request):
    # return JsonResponse([], safe=False)
    if "POST" == request.method:
        parameters = json.loads(request.body)
        ret = list()
        if "key" not in parameters:
            return JsonResponse([], safe=False)

        key = parameters["key"]
        for item in data:
            if key in item:
                ret.append(item)

        return JsonResponse(ret, safe=False)
    else:
        return HttpResponse(status=404)
