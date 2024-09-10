from rest_framework import serializers
from .models import *


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = '__all__'

class KitchenGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = ['id', 'name', 'location', 'description']

class KitchenInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenInventory
        fields = '__all__'

class KitchenInventoryGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenInventory
        fields = ['id', 'item_name', 'quantity', 'unit','restock_level', 'last_restock_date']

class KitchenRestockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restock
        fields = '__all__'

    def create(self, validated_data):
        inventory_item = validated_data['inventory_item']
        restock_quantity = validated_data['restock_quantity']
        
        # Update the inventory quantity
        inventory_item.quantity += restock_quantity
        inventory_item.restock_level += restock_quantity
        inventory_item.save()

        # Create the restock record
        return super().create(validated_data)

class KitchenExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenExpense
        fields = '__all__'

class KitchenExpenseGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenExpense
        fields = ['id', 'status', 'amount', 'description','category', 'date']


class KitchenRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenRevenue
        fields = '__all__'

class KitchenRevenueGetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenRevenue
        fields = ['id', 'status', 'amount', 'description','category', 'date']


class KitchenFinancialStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenFinancialStatement
        fields = '__all__'
