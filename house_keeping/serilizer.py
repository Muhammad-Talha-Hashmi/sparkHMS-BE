
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from staff.serializers import StaffListingSerializer
from rooms.serilizer import RoomsListingSerializer

class HouseKeepingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseKeeping
        fields = '__all__'


class HouseKeepingSerializerGettter(serializers.ModelSerializer):
    room = RoomsListingSerializer()
    staff = StaffListingSerializer()
    class Meta:
        model = HouseKeeping
        fields = '__all__'