from rest_framework.serializers import (ModelSerializer, SerializerMethodField, CharField, Serializer)
from utils.enum import Types
from .models import Organization

type_obj = Types()



class OrganizationCreateSerializer(ModelSerializer):
    name = CharField(max_length=120, required=True, allow_null=False)
    display_name = CharField(max_length=120, required=True, allow_null=False)
    address = CharField(max_length=60, required=False, allow_null=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'address', 'status', 'logo', 'display_name','created_by', 'modified_by']

class GetOrganizationSerializer(ModelSerializer):
    status = SerializerMethodField('get_status', required=False)

    def get_status(self, obj):
        return type_obj.get_status(status=obj.status)
    class Meta:
        model = Organization
        fields = ['org_id', 'name', 'address', 'use_saml', 'status', 'display_name', 'created_datetime', 'modified_datetime']

class ChangePasswordSerializer(Serializer):
    password = CharField(required=True, write_only=True)