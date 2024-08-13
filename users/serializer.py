from rest_framework.authtoken.models import Token
from rest_framework.serializers import (ModelSerializer, DateField, ValidationError,
                                        SerializerMethodField, ImageField, CharField, EmailField, IntegerField,Serializer,PrimaryKeyRelatedField, BooleanField )
from .models import User
from utils.enum import Types
from organization.models import Hotel, Organization
from django.contrib.auth.models import Group
from organization.serializer import HotelDropDownSerializer

type_obj = Types()


class UserSerializer(ModelSerializer):
    username = CharField(max_length=120, required=True, allow_null=False)
    first_name = CharField(max_length=60, required=True, allow_null=False)
    last_name = CharField(max_length=60, required=True, allow_null=False)
    full_name = CharField(max_length=120, required=True, allow_null=False)
    email = EmailField(required=True, allow_null=False)
    date_of_birth = DateField(required=False, allow_null=True)
    user_image = ImageField(required=False, allow_null=True)
    created_by_id = IntegerField(required=False, allow_null=True)
    status = CharField(required=False, default=1)
    type = CharField(required=False, allow_null=True)
    is_organization_admin = BooleanField(required=False, allow_null=True)
    is_super_admin = BooleanField(required=False, allow_null=True)
    hotel = PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=False)

    def validate_type(self, value):
        type_value = type_obj.get_user_type(value)
        if type_value == 0:
            raise ValidationError("Invalid Type.")
        return type_value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        temp_type = validated_data.get('type', 5)
        type=type_obj.get_user_type(temp_type)
        instance = self.Meta.model(**validated_data)
        # Assign the user to the corresponding group
        if type:
            try:
                group = Group.objects.get(name=type)
                instance.save()  # Save the instance before adding to group
                instance.groups.add(group)
            except Group.DoesNotExist:
                raise ValidationError(f"Group '{type}' does not exist.")
        
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'unique_code', 'username', 'date_of_birth',
                  'user_image', 'password', 'created_by_id', 'type',
                  'status',"hotel",'is_super_admin','is_organization_admin']


class GetUserSerializer(ModelSerializer):
    user_image = SerializerMethodField('get_user_image', required=False)
    type = SerializerMethodField('get_type', required=False)
    status = SerializerMethodField('get_status', required=False)
    full_name = SerializerMethodField('get_name', required=False)
    api_token = SerializerMethodField('get_api_token', required=False)
    groups = SerializerMethodField('get_groups', required=False)
    hotel = HotelDropDownSerializer()

    def get_user_image(self, obj):
        try:
            photo_url = obj.user_image.url
            # print("PHOTO URL: ", photo_url)
            return self.context['request'].build_absolute_uri(photo_url)
        except Exception as e:
            # print(e)
            return None

    def get_type(self, obj):
        return type_obj.get_user_type(obj.type)

    def get_status(self, obj):
        return type_obj.get_status(status=obj.status)

    def get_name(self, obj):
        return str(obj.full_name)
    
    def get_groups(self, obj):
        groups = []
        for group in obj.groups.all():
            groups.append(group.name)
        return groups

    def get_api_token(self, obj):
        # Try to get an existing token for the user
        token, created = Token.objects.get_or_create(user=obj)

        return token.key

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth', 'user_image',
                  'type','api_token',
                  'created_by_id', 'status', 'date_joined', 'is_active', 'hotel', 'is_super_admin', 'groups']


class UpdateUserSerializer(ModelSerializer):
    os = CharField(max_length=10, required=True, allow_null=False)
    type = CharField(required=False, allow_null=False)
    status = CharField(required=False, allow_null=False)
    modified_by_id = IntegerField(required=True, allow_null=False)

    def validate_type(self, value):
        type_value = type_obj.get_user_type(user_type=value)
        if type_value == 0:
            raise ValidationError("Invalid Type.")
        return type_value

    def validate_status(self, value):
        status_value = type_obj.get_status(status=value)
        if status_value == 0:
            raise ValidationError("Invalid Status.")
        return status_value

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth',
                  'user_image', 'type', 'modified_by_id',
                  'modified_datetime', 'status', 'date_joined']


class FilterUserSerializer(ModelSerializer):
    type = CharField(required=False, allow_null=False)
    status = CharField(required=False, allow_null=False)

    def validate_type(self, value):
        type_value = type_obj.get_user_type(user_type=value)
        if type_value == 0:
            raise ValidationError("Invalid Type.")
        return type_value

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username', 'date_of_birth', 'user_image',
                  'type',
                  'modified_by_id',
                  'modified_datetime', 'status', 'date_joined']

class GetUserForExtensionSerializer(ModelSerializer):
    type = SerializerMethodField('get_type', required=False)
    status = SerializerMethodField('get_status', required=False)
    full_name = SerializerMethodField('get_name', required=False)
    hotel_name = SerializerMethodField('get_hotel_name', required=False)
    def get_type(self, obj):
        return type_obj.get_user_type(obj.type)

    def get_status(self, obj):
        return type_obj.get_status(status=obj.status)

    def get_name(self, obj):
        return str(obj.full_name)

    def get_hotel_name(self, obj):
        return str(obj.hotel.name)


    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'username',
                  'type', 'status', 'is_active', 'hotel_id','hotel_name']

