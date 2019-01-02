from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'demo1.html')


def get_array(request):
    ret = [1,2,3,4,5,6]
    return JsonResponse(ret, safe=False)