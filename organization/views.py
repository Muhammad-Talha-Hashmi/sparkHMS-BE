from django.shortcuts import render
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import traceback
from .serializer import *
from .models import *
from django.contrib.auth.models import User
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
# Create your views here.
class SignUp(APIView):
    def post(self, request):
        try: 
            payload = request.data
            print(payload)
            serializer = UserSerializer(data=payload)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return created(message='User Created successfully')                                   
          
        except ValidationError as err:
            error_message = err.get_full_details()
            print(traceback.format_exc())
            return internal_server_error(message=error_message)
class Login(APIView):
    def post(self, request):
        try:
            print(request.data)
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            user = authenticate(request=request, email=email, password=password)
            
            if not user:
                return bad_request(message='Invalid credentials')

            if not user.is_active:
                return bad_request(message='User account is disabled')

            refresh = RefreshToken.for_user(user)
            serializer = GetUserSerializer(user)

        
            return ok(data={'user': serializer.data, 'access_token': str(refresh.access_token), 'refresh_token': str(refresh)},message='Login successfully successfully')                                   
          
        except ValidationError as err:
            error_message = err.get_full_details()
            print(traceback.format_exc())
            return internal_server_error(message=error_message)

class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        print(email)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user_instance = User.objects.filter(email=email).first()
            if user_instance:
                print('call')
                user_instance.set_password(password)
                user_instance.is_first_time_login = False
                user_instance.reset_token = None
                user_instance.save()
                return ok(data='null', message='Password changed successfully')
            return bad_request(message='User does not exist')
        return internal_server_error(message=serializer.errors)

class GetUsers(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try: 
            all_users = User.objects.filter().order_by('-date_joined')
            resultdata=[]
            if all_users.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_users, request)
                serializer = GetUserSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
        
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get news')


class DeleteUser(APIView):
    def post(self, request):
        try:
            userId = request.data.get('userId')
            user=User.objects.filter(id=userId)
            if not user:
                return not_found(message='Invalid user')
            else:
                user.delete()
                return ok(message='User deleted successfully')                                   
          
        except ValidationError as err:
            error_message = err.get_full_details()
            print(traceback.format_exc())
            return internal_server_error(message=error_message)

class ManageOrganization(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = request.data
        serializer = OrganizationCreateSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                message = f"{serializer.validated_data.get('name')} created Successfully "   
                return created(data=serializer.validated_data, message=message)                    
        return internal_server_error(message=serializer.errors)

    def get(self, request):
        try: 
            all_Organization = Organization.objects.order_by('-created_date')
            resultdata=[]
            if all_Organization.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_Organization, request)
                serializer = OrganizationCreateSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Organizations')

    def patch(self, request):
        try:
            try:
                organizationId= request.data.get('org_id',None)
                organizationData = Organization.objects.get(org_id=organizationId)
            except OrganizationTable.DoesNotExist:
                return not_found(message="Organization not found")

            data = request.data

            serializer = OrganizationCreateSerializer(organizationData, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message = f"{serializer.validated_data.get('name')} updated successfully"
                return ok(message= message)
            else:
                return bad_request(serializer.errors)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update Staff')
    def delete(self, request):
        try: 
            organizationId= request.GET.get('id', None)
            try:
                organizationInstance = Organization.objects.filter(org_id=organizationId).first()
            except organizationInstance.DoesNotExist:
                # Handle the case where the object is not found
                messageData="Organization not found with id : ".format(organizationId)
                return bad_request(message=messageData)
            else:
                # Object was found, do something with it
                organizationInstance.delete()
                return ok(message='Successfully deleted the Organization')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the Organization')
