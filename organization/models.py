from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from utils.enum import Types
from utils.methods import organization_key_generator
from core.settings import AUTH_USER_MODEL

type_obj = Types()
class Base(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True,
                                   related_name="created_by", on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(AUTH_USER_MODEL, blank=True, related_name="%(app_label)s_%(class)s_modified_by",
                                    null=True, on_delete=models.CASCADE)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=2, null=True, blank=True)

    class Meta:
        abstract = True

# Create your models here.
class Organization(models.Model):
    org_id = models.AutoField(primary_key=True)
    name = models.TextField()
    address = models.TextField(blank=True, null=True)
    org_key = models.TextField(default=organization_key_generator)
    status = models.PositiveSmallIntegerField(default=2)
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_date = models.DateField(auto_now=True, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    logo = models.ImageField(upload_to='assets/', default='assets/no_image.png', null=True, blank=True)
    display_name = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, blank=True,
                                   related_name="organization_created_by", on_delete=models.CASCADE)
    modified_by = models.ForeignKey(AUTH_USER_MODEL, blank=True, related_name="organization_modified_by",
                                    null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'

class Hotel (Base):
    name = models.TextField()
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='assets/', default='assets/no_image.png', null=True, blank=True)
    display_name = models.TextField(null=True, blank=True)
    domain = models.CharField(null=True, blank=True)
    contact_no = models.CharField(max_length=16,null=True, blank=True)
    contact_email = models.CharField(max_length=30,null=True, blank=True)
    website = models.CharField(max_length=60,null=True, blank=True)
    organization = models.ForeignKey(Organization, related_name='hotel_organization_fk', null=True, blank=True,
                                     on_delete=models.CASCADE)

