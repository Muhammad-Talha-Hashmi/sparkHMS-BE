import traceback
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from organization.models import Organization
from organization.serializer import OrganizationCreateSerializer
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from .models import *
from .serializer import *

User = get_user_model()

# Create your views here.
class SignUp(APIView):
    def post(self, request):
        try: 
            payload = request.data
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
        password = request.data.get('password')

        if not email or not password:
            return Response({'message': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.filter(email=email).first()
        if user_instance:
            user_instance.set_password(password)
            user_instance.is_first_time_login = False
            user_instance.reset_token = None
            user_instance.save()
            return Response({'data': 'null', 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

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
            except Organization.DoesNotExist:
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
            except Organization.DoesNotExist:
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


class ManageUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            groups = request.user.groups.all()
            # Create a list of group names
            group_names = [group.name for group in groups]
            type= request.data.get('type')
            if 'Super Admin' in group_names or 'Hotel Admin' in group_names or 'Organization Admin' in group_names:
                payload = request.data
                serializer = UserSerializer(data=payload)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return created(message='User Created successfully')  
                else:             
                    return internal_server_error(message=serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create user')

    def get(self, request, id=None):
        try: 
            print(id)
            if id is not None:
                all_users = User.objects.filter(is_organization_admin=False,is_super_admin=False,hotel=id).order_by('-date_joined')
                resultdata=[]
                if all_users.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_users, request)
                    serializer = GetUserSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)
            else:
                bad_request(message="Hotel id is missing")
           
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Organizations')

    def patch(self, request):
        try:
            try:
                organizationId= request.data.get('org_id',None)
                organizationData = Organization.objects.get(org_id=organizationId)
            except Organization.DoesNotExist:
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
            except Organization.DoesNotExist:
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
