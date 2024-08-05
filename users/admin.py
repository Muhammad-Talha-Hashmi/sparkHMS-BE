from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('User Credentials', {
            'fields': ('email', 'password', 'first_name', 'last_name', 'full_name', 'phone_number',)
        }),
        ('User Groups', {
            'fields': ('groups',)
        }),
        ('Basic', {
            'fields': ('unique_code', 'date_of_birth', 'hotel',
                       'user_image', 'type', 'is_staff', 'is_active', 'is_organization_admin', 'is_super_admin',
                       'is_first_time_login', 'last_login', 'date_joined', 'created_by', 'modified_by',
                       'modified_datetime', 'status',)
        }),
    )
    readonly_fields = ['date_joined']


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Session)
admin.site.register(UserPermissions)
