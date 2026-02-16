from django.contrib import admin
from .models import Turf

@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "price_per_hour")
