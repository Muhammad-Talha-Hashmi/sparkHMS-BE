from django.contrib import admin

from .models import *



# Register your models here.
admin.site.register(Organization)
admin.site.register(Hotel)
admin.site.register(HotelInventory)
admin.site.register(InventoryRestock)
