from rest_framework import serializers
from .models import *


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
