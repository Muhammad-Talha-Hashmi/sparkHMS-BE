
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from organization.models import Hotel

class StaffSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)

    class Meta:
        model = staffTable
        fields = '__all__'

class StaffListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = staffTable
        fields = ['id', 'name']