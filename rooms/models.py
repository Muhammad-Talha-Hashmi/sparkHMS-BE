from django.db import models

# Create your models here.
class amenitiesTable(models.Model):
    name = models.CharField(max_length=100)


class roomsTable(models.Model):
    room = models.CharField(max_length=120, blank=True)
    room_type = models.CharField(max_length=60, blank=True)
    bed_type = models.CharField(max_length=60, blank=True)
    price = models.CharField(max_length=120, blank=True)
    amenities = models.ManyToManyField(amenitiesTable)
    availability = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=120, blank=True)