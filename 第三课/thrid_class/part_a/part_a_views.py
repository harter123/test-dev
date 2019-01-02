from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

def part_a(request):
    return render(request, 'part_a.html')

def part_b(request):
    return render(request, 'part_b.html')

def part_c(request):
    return render(request, 'part_c.html')

def part_d(request):
    return render(request, 'part_d.html')

def get_array(request):
    ret = ["apple", "orange", "banana"]
    return JsonResponse(ret, safe=False)


def get_json(request):
    ret = dict()
    ret["apple"] = 10
    ret["orange"] = 5
    ret["banana"] = 6
    return JsonResponse(ret, safe=False)
