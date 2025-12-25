from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_turf_list, name="list-turfs"),
    path("<int:id>/", views.turf_detail, name="turf-detail"),
]
