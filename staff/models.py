from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _


# Create your models here.
class staffTable(models.Model):
    position = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=60, blank=True)
    contact = models.CharField(max_length=60, blank=True)
    emergency_contact = models.CharField(max_length=120, blank=True)
    email = models.EmailField(unique=True)
    nationlaity = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    responsibilities = models.CharField(max_length=120, blank=True)