from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Category


def show_category_list_page(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    categories = Category.objects.all()
    error = request.GET.get("error")

    return render(request, "list_category.html", {
        "categories": categories,
        "error": error
    })


def show_add_category_page(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    return render(request, "add_category.html")


def add_category(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    if request.method == "GET":
        return show_add_category_page(request)

    name = request.POST.get("name")

    if not name:
        return render(request, "add_category.html", {
            "error": "Category name is required"
        })

    Category.objects.create(name=name)
    return redirect("list-category")


def show_edit_category_page(request: HttpRequest, error=None):
    if not request.session.get("email"):
        return redirect("login")

    id = request.GET.get("id")
    if not id:
        return redirect("list-category")

    category = Category.objects.filter(id=id).first()
    if not category:
        return redirect("list-category")

    return render(request, "edit_category.html", {
        "category": category,
        "error": error
    })


def edit_category(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    if request.method == "GET":
        return show_edit_category_page(request)

    id = request.POST.get("id")
    name = request.POST.get("name")

    category = Category.objects.filter(id=id).first()
    if not category:
        return show_edit_category_page(request, "Category does not exist")

    category.name = name
    category.save()

    return redirect("list-category")


def delete_category(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    id = request.GET.get("id")
    if not id:
        return redirect("list-category")

    category = Category.objects.filter(id=id).first()
    if not category:
        return redirect("list-category")

    category.delete()
    return redirect("list-category")
