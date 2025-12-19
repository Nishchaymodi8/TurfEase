from django.db import models
from category.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
   
    def __str__(self):
        return self.name
