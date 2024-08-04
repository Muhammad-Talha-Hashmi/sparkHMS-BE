from rest_framework.authtoken.models import Token
from rest_framework.serializers import (ModelSerializer, DateField, ValidationError,
                                        SerializerMethodField, ImageField, CharField, EmailField, IntegerField,Serializer )
from .models import Organization
from utils.enum import Types

type_obj = Types()

class OrganizationCreateSerializer(ModelSerializer):
    name = CharField(max_length=120, required=True, allow_null=False)
    display_name = CharField(max_length=120, required=True, allow_null=False)
    address = CharField(max_length=60, required=False, allow_null=True)
    class Meta:
        model = Organization
        fields = ['org_id', 'name', 'address', 'use_saml', 'status', 'logo', 'display_name','created_by', 'modified_by']

class GetOrganizationSerializer(ModelSerializer):
    status = SerializerMethodField('get_status', required=False)

    def get_status(self, obj):
        return type_obj.get_status(status=obj.status)
    class Meta:
        model = Organization
        fields = ['org_id', 'name', 'address', 'use_saml', 'status', 'display_name', 'created_datetime', 'modified_datetime']
