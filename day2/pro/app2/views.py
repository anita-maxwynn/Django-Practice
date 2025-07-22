from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("<h1>Welcome to App2</h1>")
def about(request):
    context = {
        'title': 'About App2',
        'description': 'This is the about page for App2.'
    }
    return render(request, 'about.html', context)
