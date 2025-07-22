from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("<h1>Welcome to App1</h1>")
def about(request):
    return HttpResponse("<h1>About App1</h1>")

def render1(request):
    return render(request, 'index.html')