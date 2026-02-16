from django.db import models

class Turf(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    price_per_hour = models.IntegerField()
    image = models.ImageField(
        upload_to="turf_images/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
