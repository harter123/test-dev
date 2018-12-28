from django.shortcuts import render

# Create your views here.

def one(request):
    return render(request, 'one.html')