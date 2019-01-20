from django.shortcuts import render

# Create your views here.

def demo1(request):
    return render(request, 'demo1_chandishuju.html')

def demo2(request):
    return render(request, 'demo2_fuzujianchuandishuju.html')

def demo3(request):
    return render(request, 'demo3_zizujianchuandishuju.html')

def demo4(request):
    return render(request, 'demo4.html')