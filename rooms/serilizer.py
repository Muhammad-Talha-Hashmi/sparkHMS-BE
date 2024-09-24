
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from organization.models import Hotel
from organization.serializer import HotelDropDownSerializer, HotelCreateSerializer

class RoomsSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    bed_type = serializers.PrimaryKeyRelatedField(queryset=BedType.objects.all(), required=False, allow_null=True)
    amenities = serializers.PrimaryKeyRelatedField(queryset=RoomAmeneties.objects.all(), many=True, required=False, allow_null=True)
    services = serializers.PrimaryKeyRelatedField(queryset=RoomServices.objects.all(), many=True, required=False, allow_null=True)
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

class AmenetiesListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmeneties
        fields = ['id', 'name']

class ServicesListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomServices
        fields = ['id', 'name']

class BedTypeListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedType
        fields = ['id', 'name', 'number_of_person']

class RoomGetterSerializer(serializers.ModelSerializer):
    hotel = HotelDropDownSerializer()  # Use nested serializer for detailed representation
    bed_type = BedTypeListingSerializer()  # Use nested serializer for detailed representation
    amenities = AmenetiesListingSerializer(many=True)  # Use nested serializer for many-to-many fields
    services = ServicesListingSerializer(many=True)  # Use nested serializer for many-to-many fields

    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=True)

    class Meta:
        model = RoomBooking
        fields = '__all__'
        


class RoomGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room']

class BookingListingSerializer(serializers.ModelSerializer):
    hotel = HotelDropDownSerializer()
    room = RoomGetSerializer()

    class Meta:
        model = RoomBooking
        fields = '__all__'


class BookingDetailSerializer(serializers.ModelSerializer):
    room = RoomGetterSerializer()

    class Meta:
        model = RoomBooking
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderGetterSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Include related order items

    class Meta:
        model = Order
        fields = ['id', 'booking', 'kitchen', 'order_date', 'total_amount', 'is_paid', 'order_items']
