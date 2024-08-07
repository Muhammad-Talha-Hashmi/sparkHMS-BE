from django.shortcuts import render
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import traceback
from .serializer import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model


# Create your views here.
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
            all_Organization = Organization.objects.all()
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
                organizationId= request.data.get('id',None)
                organizationData = Organization.objects.get(id=organizationId)
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
                organizationInstance = Organization.objects.filter(id=organizationId).first()
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


class OrganizationDropdown(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try: 
            all_Organization = Organization.objects.all()
            if all_Organization.exists():
                serializer = OrganizationDropDownSerializer(all_Organization, many=True)
                return ok(data=serializer.data)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Organizations')

class ManageHotel(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = request.data
        serializer = HotelCreateSerializer(data=payload)
        if serializer.is_valid():
                serializer.save()
                message = f"{serializer.validated_data.get('name')} created Successfully "   
                return created( message=message)                    
        return internal_server_error(message=serializer.errors)

    def get(self, request):
        try: 
            all_hotels = Hotel.objects.all()
            resultdata=[]
            if all_hotels.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_hotels, request)
                serializer = HotelCreateSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Hotels')

    def patch(self, request):
        try:
            try:
                hotelId= request.data.get('id',None)
                hotelData = Hotel.objects.get(id=hotelId)
            except Hotel.DoesNotExist:
                return not_found(message="Hotel not found")

            data = request.data

            serializer = HotelCreateSerializer(hotelData, data=data, partial=True)
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
            hotelId= request.GET.get('id', None)
            try:
                hotelInstance = Hotel.objects.filter(id=hotelId).first()
            except Hotel.DoesNotExist:
                # Handle the case where the object is not found
                messageData="Organization not found with id : ".format(hotelId)
                return bad_request(message=messageData)
            else:
                # Object was found, do something with it
                hotelInstance.delete()
                return ok(message='Successfully deleted the Hotel')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the Hotel')

class HotelDropdown(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try: 
            all_hotel = Hotel.objects.all()
            if all_hotel.exists():
                serializer = HotelDropDownSerializer(all_hotel, many=True)
                return ok(data=serializer.data)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Hotel')