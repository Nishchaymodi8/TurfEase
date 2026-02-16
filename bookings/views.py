from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from datetime import datetime
from .models import Booking
from turfs.models import Turf
import razorpay
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)
SLOTS = [
    ("06:00", "07:00"), ("07:00", "08:00"), ("08:00", "09:00"),
    ("09:00", "10:00"), ("10:00", "11:00"), ("11:00", "12:00"),
    ("12:00", "13:00"), ("13:00", "14:00"), ("14:00", "15:00"),
    ("15:00", "16:00"), ("16:00", "17:00"), ("17:00", "18:00"),
    ("18:00", "19:00"), ("19:00", "20:00"), ("20:00", "21:00"),
    ("21:00", "22:00"), ("22:00", "23:00")
]


# --------------------------
# BOOK PAGE
# --------------------------
@login_required
def book_page(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)
    today = timezone.localdate()

    return render(request, "book_turf.html", {
        "turf": turf,
        "today": today,
    })


# --------------------------
# AVAILABLE SLOTS (AJAX)
# --------------------------
@require_GET
def available_slots(request, turf_id):

    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"slots": []})

    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = timezone.localdate()
    now_time = timezone.localtime().time()

    if selected_date < today:
        return JsonResponse({"slots": []})

    booked_slots = set(
        Booking.objects.filter(
            turf_id=turf_id,
            date=selected_date
        ).values_list("slot", flat=True)
    )

    available = []

    for start, end in SLOTS:
        slot = f"{start}-{end}"
        start_time = datetime.strptime(start, "%H:%M").time()

        if slot in booked_slots:
            continue

        if selected_date == today and start_time <= now_time:
            continue

        available.append(slot)

    return JsonResponse({"slots": available})


# --------------------------
# CONFIRM BOOKING (AJAX)
# --------------------------
@login_required
@require_POST
def confirm_booking(request, turf_id):

    turf = get_object_or_404(Turf, id=turf_id)

    date = request.POST.get("date")
    slots = request.POST.getlist("slots")

    if not date or not slots:
        return JsonResponse({"error": "Select date and slot"}, status=400)

    selected_date = datetime.strptime(date, "%Y-%m-%d").date()

    # Re-check availability
    for slot in slots:
        if Booking.objects.filter(
            turf=turf,
            date=selected_date,
            slot=slot
        ).exists():
            return JsonResponse({"error": f"{slot} already booked"}, status=400)

    total_price = len(slots) * turf.price_per_hour
    
    request.session["booking_date"] = date
    request.session["booking_slots"] = slots


    return JsonResponse({
        "success": True,
        "total_price": total_price,
        "slots": slots,
        "date": date
    })



@login_required
@require_POST
def create_razorpay_order(request, turf_id):

    turf = get_object_or_404(Turf, id=turf_id)

    amount = int(request.POST.get("amount"))  # amount in rupees
    amount_paise = amount * 100

    order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })
    request.session["razorpay_order_id"] = order["id"]


    return JsonResponse({
        "order_id": order["id"],
        "amount": amount,
        "key": settings.RAZORPAY_KEY_ID
    })
@login_required
@require_POST
@login_required
@require_POST
def verify_payment(request, turf_id):

    try:
        payment_id = request.POST.get("razorpay_payment_id")
       # order_id = request.POST.get("razorpay_order_id")
        order_id = request.session.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        print("PAYMENT ID:", payment_id)
        print("ORDER ID:", order_id)
        print("SIGNATURE:", signature)

        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        print("SIGNATURE VERIFIED SUCCESSFULLY")

        turf = get_object_or_404(Turf, id=turf_id)

        date = request.session.get("booking_date")
        slots = request.session.get("booking_slots")

        print("SESSION DATE:", date)
        print("SESSION SLOTS:", slots)

        for slot in slots:
         Booking.objects.create(
        turf=turf,
        user=request.user,
        date=date,
        slot=slot,
        order_id=order_id,   # ADD THIS FIELD
        payment_id=payment_id
         )


        return JsonResponse({
            "success": True,
            "redirect_url": f"/invoice/{order_id}/"
        })

    except Exception as e:
        print("VERIFY ERROR:", str(e))
        return JsonResponse({
            "success": False,
            "error": str(e)
        })

@login_required
def invoice_page(request, order_id):

    bookings = Booking.objects.filter(
        user=request.user,
        order_id=order_id
    )

    if not bookings.exists():
        return redirect("book_page")

    total = sum([b.turf.price_per_hour for b in bookings])

    return render(request, "invoice.html", {
        "order_id": order_id,
        "bookings": bookings,
        "total": total,
        "today": timezone.now()
    })
