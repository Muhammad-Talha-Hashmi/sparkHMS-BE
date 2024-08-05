from django.db import models

from organization.models import Hotel
from utils.base_model import Base


class HotelTransaction(Base):
    hotel = models.ForeignKey('organization.Hotel', on_delete=models.CASCADE, related_name='%(class)ss')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Expense(HotelTransaction):
    CATEGORY_CHOICES = [
        ('Inventory', 'Inventory'),
        ('Salary', 'Salary'),
        ('Maintenance', 'Maintenance'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"Expense ({self.category}) - {self.amount} on {self.date}"


class Revenue(HotelTransaction):
    CATEGORY_CHOICES = [
        ('Room Booking', 'Room Booking'),
        ('Food & Beverage', 'Food & Beverage'),
        ('Service', 'Service'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"Revenue ({self.category}) - {self.amount} on {self.date}"


class HotelFinancialStatement(Base):
    hotel = models.ForeignKey('organization.Hotel', on_delete=models.CASCADE, related_name='financial_statements')
    period_start = models.DateField()
    period_end = models.DateField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_revenues = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def generate_statement(self):
        expenses = Expense.objects.filter(hotel=self.hotel, date__range=[self.period_start, self.period_end])
        revenues = Revenue.objects.filter(hotel=self.hotel, date__range=[self.period_start, self.period_end])
        self.total_expenses = sum(expense.amount for expense in expenses)
        self.total_revenues = sum(revenue.amount for revenue in revenues)
        self.net_profit = self.total_revenues - self.total_expenses
        self.save()

    def __str__(self):
        return f"Financial Statement ({self.period_start} to {self.period_end}) for {self.hotel.name}"
