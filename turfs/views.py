from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Turf

def show_turf_list(request: HttpRequest):
    if not request.session.get("email"):
        return redirect("login")

    turfs = Turf.objects.all()
    return render(request, "list_turfs.html", {
        "turfs": turfs
    })

def turf_detail(request, id):
    if not request.session.get("email"):
        return redirect("login")

    turf = get_object_or_404(Turf, id=id)

    return render(request, "turf_detail.html", {
        "turf": turf
    })
