from django.shortcuts import render
from django.http import HttpRequest


def show_home_page(reaquest:HttpRequest):
     return render(reaquest,'home.html')
    
