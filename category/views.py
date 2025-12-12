from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
# Create your views here.


def add_category(request:HttpRequest):
    return render(request,"add_category.html")
