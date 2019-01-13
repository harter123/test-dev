from django.shortcuts import render

# Create your views here.

def note(request):
    return render(request, 'note.html')