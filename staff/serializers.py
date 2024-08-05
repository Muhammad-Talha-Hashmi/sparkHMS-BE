
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = staffTable
        fields = '__all__'

class StaffListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = staffTable
        fields = ['id', 'name']