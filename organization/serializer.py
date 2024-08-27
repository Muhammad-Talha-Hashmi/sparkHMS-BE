from rest_framework.serializers import (ModelSerializer, SerializerMethodField, CharField, Serializer,PrimaryKeyRelatedField)
from utils.enum import Types
from .models import Organization,Hotel

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
        fields = ['org_id', 'name', 'address', 'status', 'display_name']

class OrganizationDropDownSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class HotelCreateSerializer(ModelSerializer):
    name = CharField(max_length=120, required=True, allow_null=False)
    display_name = CharField(max_length=120, required=True, allow_null=False)
    address = CharField(max_length=60, required=False, allow_null=True)
    organization = PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'status','domain','contact_no','contact_email','website','organization', 'logo', 'display_name','created_by', 'modified_by']

class HotelDropDownSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name']
