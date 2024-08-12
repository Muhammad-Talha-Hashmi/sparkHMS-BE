
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from organization.models import Hotel

class RoomsSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    class Meta:
        model = Room
        fields = '__all__'
class AmenitiesSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    class Meta:
        model = RoomAmeneties
        fields = '__all__'

class ServicesSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    class Meta:
        model = RoomServices
        fields = '__all__'

class BedTypeSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    class Meta:
        model = BedType
        fields = '__all__'

class RoomsSerializerGetter(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    amenities = AmenitiesSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

class RoomsListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room']
        # Add other fields if there are any