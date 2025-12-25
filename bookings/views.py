from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Booking
from turfs.models import Turf


@login_required(login_url="login")
def book_turf(request, turf_id):
    # ✅ Safe turf fetch (prevents 500 error)
    turf = get_object_or_404(Turf, id=turf_id)

    if request.method == "POST":
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        # ❌ Basic validation
        if not date or not start_time or not end_time:
            messages.error(request, "⚠️ All fields are required.")
            return redirect(request.path)

        # 🔒 DOUBLE BOOKING CHECK
        exists = Booking.objects.filter(
            turf=turf,
            date=date,
            start_time=start_time,
            end_time=end_time
        ).exists()

        if exists:
            messages.error(request, "❌ This slot is already booked.")
            return redirect(request.path)

        # ✅ CREATE BOOKING
        Booking.objects.create(
            turf=turf,
            user=request.user,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(request, "✅ Booking confirmed!")
        return redirect("home")

    # ✅ GET request – show booking form
    return render(request, "book_turf.html", {
        "turf": turf
    })
