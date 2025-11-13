from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models import User, Role
from turfapp.utils.validators import email_validator, password_validator

def show_home_page(reaquest:HttpRequest):
    if reaquest.method=="GET":
        return render(reaquest,'home.html')
    
