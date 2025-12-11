from django.shortcuts import render,redirect
from django.http import HttpRequest


def show_home_page(request:HttpRequest):
     if request.session.get("email") is None:
          return redirect("login")
     return render(request,'home.html')
    
