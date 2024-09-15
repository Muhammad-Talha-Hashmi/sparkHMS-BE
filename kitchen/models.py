from django.db import models

from organization.models import Hotel
from utils.base_model import Base


class Kitchen(Base):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='kitchen_hotel')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class KitchenInventory(Base):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_inventory')
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    restock_level = models.PositiveIntegerField()
    last_restock_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_name} ({self.kitchen.name})"


class Restock(Base):
    inventory_item = models.ForeignKey(KitchenInventory, on_delete=models.CASCADE, related_name='kitchen_restocks')
    restock_quantity = models.PositiveIntegerField()
    restock_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Restock {self.inventory_item.item_name} ({self.restock_quantity}) on {self.restock_date}"


class KitchenTransaction(Base):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Transaction ({self.amount}) on {self.date}"

class KitchenExpense(KitchenTransaction):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='expenses')
    CATEGORY_CHOICES = [
        ('Supplies', 'Supplies'),
        ('Utilities', 'Utilities'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.CharField(max_length=50)

    def __str__(self):
        return f"Kitchen Expense ({self.category}) - {self.amount} on {self.date}"


class KitchenRevenue(KitchenTransaction):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='revenues')
    date = models.CharField(max_length=50)
    CATEGORY_CHOICES = [
        ('Room Service', 'Room Service'),
        ('Restaurant Sales', 'Restaurant Sales'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"Kitchen Revenue ({self.category}) - {self.amount} on {self.date}"


class KitchenFinancialStatement(Base):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='kitchen_financial_statements')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='financial_statements')
    period_start = models.DateField()
    period_end = models.DateField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_revenues = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return f"Kitchen Financial Statement ({self.period_start} to {self.period_end}) for {self.kitchen.name} in {self.hotel.name}"

from django.db import models

class Category(Base):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_category')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')

    def __str__(self):
        return self.name
