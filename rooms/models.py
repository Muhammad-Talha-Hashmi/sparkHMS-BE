from django.db import models

from organization.models import Hotel
from kitchen.models import MenuItem,Kitchen
from utils.base_model import Base
from django.utils import timezone





class RoomAmeneties(Base):
    name = models.CharField(max_length=120, null=False, blank=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_amentities_fk')


class RoomServices(Base):
    name = models.CharField(max_length=120, null=False, blank=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_services_fk')


class BedType(Base):
    name = models.CharField(max_length=120, null=False, blank=False)
    number_of_person =models.IntegerField(default=1)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_bedtype_fk')

class Room(Base):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_rooms_fk')
    room = models.CharField(max_length=120, null=True, blank=True)
    room_type = models.CharField(max_length=60, null=True, blank=True)
    number_of_bed =models.IntegerField(default=1)
    bed_type = models.ForeignKey(BedType, null=True, blank=True, on_delete=models.CASCADE,)
    capacity = models.IntegerField(default=1)
    price = models.CharField(max_length=120, null=True, blank=True)
    amenities = models.ManyToManyField(RoomAmeneties, blank=True)
    services = models.ManyToManyField(RoomServices, blank=True)
    status = models.BooleanField(default=False)
    is_house_keeping = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=120, null=True, blank=True)

class RoomBooking(Base):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_booking_fk')
    guest_name = models.CharField(max_length=255)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    is_check_in = models.BooleanField(default=False)
    is_check_out = models.BooleanField(default=False)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    
    def update_check_in_status(self, is_check_in_status):
        self.is_check_in = is_check_in_status
        self.check_in = timezone.now() if is_check_in_status else self.check_in
        self.save()

    def update_check_out_status(self, is_check_out_status):
        self.is_check_out = is_check_out_status
        self.check_out = timezone.now() if is_check_out_status else self.check_out
        self.save()
    def __str__(self):
        return f"{self.guest_name} - {self.room.name} ({self.check_in} to {self.check_out})"


class Invoice(Base):
    booking = models.OneToOneField(RoomBooking, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:  # Only set the invoice number if it hasn't been set yet
            self.invoice_number = f"INV-{self.id}"
        super().save(*args, **kwargs)
        if not self.invoice_number:  # Update invoice number after saving if it depends on the id
            self.invoice_number = f"INV-{self.id}"
            self.save()  # Save again to persist the updated invoice number
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.booking.guest_name}"


class Order(Base):
    booking = models.ForeignKey(RoomBooking, on_delete=models.CASCADE, related_name='orders')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_order')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.booking.guest_name}"


class OrderItem(Base):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    kitchen_item = models.ForeignKey(MenuItem, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        item_name = self.inventory_item.item_name if self.inventory_item else self.kitchen_item.item_name
        return f"{item_name} (x{self.quantity})"