from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from utils.base_model import Base
from utils.enum import Types
from utils.methods import organization_key_generator
from core.settings import AUTH_USER_MODEL

type_obj = Types()


# Create your models here.
class Organization(Base):
    name = models.TextField()
    address = models.TextField(blank=True, null=True)
    org_key = models.TextField(default=organization_key_generator)
    logo = models.ImageField(upload_to='assets/', default='assets/no_image.png', null=True, blank=True)
    display_name = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True,
                                   related_name="organization_created_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'


class Hotel(Base):
    name = models.TextField()
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='assets/', default='assets/no_image.png', null=True, blank=True)
    display_name = models.TextField(null=True, blank=True)
    domain = models.CharField(null=True, blank=True)
    contact_no = models.CharField(max_length=16, null=True, blank=True)
    contact_email = models.CharField(max_length=30, null=True, blank=True)
    website = models.CharField(max_length=60, null=True, blank=True)
    organization = models.ForeignKey(Organization, related_name='hotel_organization_fk',
                                     on_delete=models.CASCADE)
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True,
                                   related_name="user_created_by", on_delete=models.CASCADE)
    modified_by = models.ForeignKey(AUTH_USER_MODEL, blank=True, related_name="user_modified_by",
                                    null=True, on_delete=models.CASCADE)



class HotelInventory(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item_name} ({self.hotel.name})"


class InventoryRestock(models.Model):
    inventory_item = models.ForeignKey(HotelInventory, on_delete=models.CASCADE, related_name='restocks')
    restock_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)
        self.inventory_item.quantity += self.quantity
        self.inventory_item.save()

    def __str__(self):
        return f"Restock of {self.inventory_item.item_name} ({self.quantity} units at {self.price_per_unit} each)"
