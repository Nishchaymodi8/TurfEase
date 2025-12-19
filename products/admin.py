from django.contrib import admin
from .models import Product


class ProductWithFilters(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name', 'price',)

admin.site.register(Product, ProductWithFilters)
