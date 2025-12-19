from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from category.models import Category
from .models import Product


def show_product_list_page(request: HttpRequest):
    if request.session.get("email") is None:
        return redirect("login")

    products = Product.objects.all()
    return render(request, "list_products.html", {
        "products": products,
    })


def show_add_product_page(request: HttpRequest, error: str = None):
    if request.session.get("email") is None:
        return redirect("login")

    if error is not None:
        return render(request, "add_product.html", {"error": error})

    category = Category.objects.all().values('id', 'name')
    return render(request, "add_product.html", {
        "category": category
    })


def add_product(request: HttpRequest):
    if request.session.get("email") is None:
        return redirect("login")

    if request.method == 'GET':
        return show_add_product_page(request)

    name = request.POST.get("name")
    price = request.POST.get("price")
  
    product = Product()
    product.name = name
    product.price = price
    product.save()

    return redirect("list-products")

def show_edit_product_page(request: HttpRequest, error: str = None):
    if request.session.get("email") is None:
        return redirect("login")

    if error is not None:
        return render(request, "edit_product.html", {"error": error})

    id = request.GET.get("id")
    if id is None:
        return redirect("list-products")

    product = Product.objects.filter(id=id).first()
    if product is None:
        return redirect("list-products")

    return render(request, "edit_product.html", {
        "product": product
    })

def edit_product(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    if request.method == "GET":
        return show_edit_product_page(request)  

    id = request.POST.get("id")
    name = request.POST.get("name")

    product = Product.objects.filter(id=id).first()
    if not product:
        return redirect("list-products")

    product.name = name
    product.save()

    return redirect("list-products")


def delete_product(request: HttpRequest):
    if request.session.get("email") is None:
        return redirect("login")

    id = request.GET.get("id")
    if id is None:
        return redirect("list-products")

    product = Product.objects.filter(id=id).first()
    if product is None:
        return redirect("list-products")

    product.delete()
    return redirect("list-products")
