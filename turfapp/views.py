from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

# Create your views here.

def home(reaquest):
    return render(reaquest,"home.html")