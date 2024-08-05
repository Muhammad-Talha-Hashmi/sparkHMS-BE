from rest_framework import serializers
from .models import *

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'


class HotelFinancialStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelFinancialStatement
        fields = '__all__'

class KitchenExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenExpense
        fields = '__all__'

class KitchenRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenRevenue
        fields = '__all__'

class KitchenFinancialStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenFinancialStatement
        fields = '__all__'