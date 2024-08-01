
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = roomsTable
        fields = '__all__'
class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = amenitiesTable
        fields = '__all__'

class RoomsSerializerGetter(serializers.ModelSerializer):
    amenities = AmenitiesSerializer(many=True, read_only=True)
    class Meta:
        model = roomsTable
        fields = '__all__'

class RoomsListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = roomsTable
        fields = ['id', 'room']
        # Add other fields if there are any