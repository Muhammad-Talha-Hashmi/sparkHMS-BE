from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Kitchen)
admin.site.register(KitchenInventory)
admin.site.register(Restock)
admin.site.register(KitchenExpense)
admin.site.register(KitchenRevenue)
admin.site.register(KitchenFinancialStatement)
