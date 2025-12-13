from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
# Create your views here.

def  show_addcategory(request:HttpRequest):

    category=category.objects.all().values('id','name')
    return render(request,"add_category.html",{
        "category":category
    })


def add_category(request:HttpRequest):
    if request.method=="get":
        return show_addproduct(request)




def  edit_category(request:HttpRequest):
    return render(request,"edit_category.html")

