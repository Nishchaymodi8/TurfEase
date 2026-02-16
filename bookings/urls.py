from django.urls import path
from . import views

urlpatterns = [
    path("book/<int:turf_id>/", views.book_page, name="book_page"),
    path("api/slots/<int:turf_id>/", views.available_slots, name="available_slots"),
    path("book/<int:turf_id>/confirm/", views.confirm_booking, name="confirm_booking"),
    path("create-order/<int:turf_id>/", views.create_razorpay_order, name="create_order"),
    path("invoice/<str:order_id>/", views.invoice_page, name="invoice"),
    path("verify-payment/<int:turf_id>/", views.verify_payment, name="verify_payment"),

]
