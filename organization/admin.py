from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('User Credentials', {
            'fields': ('email', 'username', 'password', 'first_name', 'last_name', 'full_name', 'phone_number',)
        }),
        ('User Groups', {
            'fields': ('groups', 'user_permissions',)
        }),
        ('Basic', {
            'fields': ('unique_code', 'date_of_birth', 'organization',
                       'user_image', 'type', 'is_staff', 'is_active', 'is_organization_admin', 'is_super_admin',
                       'is_first_time_login', 'last_login', 'date_joined', 'created_by', 'modified_by',
                       'modified_datetime', 'status', 'google_access_token', 'google_refresh_token',
                       'google_token_expiry',)
        }),
    )
    readonly_fields = ['date_joined']


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Session)
admin.site.register(UserPermissions)
admin.site.register(Organization)
admin.site.register(OrganizationCredentials)