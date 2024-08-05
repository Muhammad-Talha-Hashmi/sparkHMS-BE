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
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    restock_level = models.PositiveIntegerField()
    last_restock_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_name} ({self.kitchen.name})"


class Restock(Base):
    inventory_item = models.ForeignKey(KitchenInventory, on_delete=models.CASCADE, related_name='restocks')
    restock_quantity = models.PositiveIntegerField()
    restock_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Restock {self.inventory_item.item_name} ({self.restock_quantity}) on {self.restock_date}"


class KitchenTransaction(Base):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Transaction ({self.amount}) on {self.date}"


class KitchenExpense(KitchenTransaction):
    CATEGORY_CHOICES = [
        ('Supplies', 'Supplies'),
        ('Utilities', 'Utilities'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"Kitchen Expense ({self.category}) - {self.amount} on {self.date}"


class KitchenRevenue(KitchenTransaction):
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
    period_start = models.DateField()
    period_end = models.DateField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_revenues = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def generate_statement(self):
        expenses = KitchenExpense.objects.filter(hotel=self.hotel, date__range=[self.period_start, self.period_end])
        revenues = KitchenRevenue.objects.filter(hotel=self.hotel, date__range=[self.period_start, self.period_end])
        self.total_expenses = sum(expense.amount for expense in expenses)
        self.total_revenues = sum(revenue.amount for revenue in revenues)
        self.net_profit = self.total_revenues - self.total_expenses
        self.save()

    def __str__(self):
        return f"Kitchen Financial Statement ({self.period_start} to {self.period_end}) for {self.hotel.name}"
