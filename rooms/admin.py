from django.contrib import admin

from rooms.models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Amenities)
admin.site.register(RoomBooking)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(OrderItem)