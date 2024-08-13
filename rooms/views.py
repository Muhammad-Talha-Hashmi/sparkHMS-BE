from django.shortcuts import render
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import traceback
from .serilizer import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class ManageRooms(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            payload_dict = request.data
            room_serializer = RoomsSerializer(data=payload_dict)
            if room_serializer.is_valid():
                room_serializer.save()
                message = f"{room_serializer.validated_data.get('room')} created Successfully "
                return created(message=message)
            else:
                return bad_request(message=room_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create room')

    def get(self, request, id=None):
        try:
             if id is not None:
                all_rooms = Room.objects.filter(hotel=id).order_by('-created_datetime')
                resultdata=[]
                if all_rooms.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_rooms, request)
                    serializer = RoomGetterSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get room list')

    def patch(self, request):
        try:
            payload_dict = request.data
            room_id = request.data.get('id', None)
            print(room_id)
            room = Room.objects.get(id=room_id)
            serializer = RoomsSerializer(room, data=payload_dict, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"{serializer.validated_data.get('room')} updated successfully"
                return ok(message=message)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update room')

    def delete(self, request):
        try:
            room_id = request.GET.get('id', None)
            try:
                room = Room.objects.filter(id=room_id).first()
            except Room.DoesNotExist:
                # Handle the case where the object is not found
                message_data = "Room not found with id : ".format(room_id)
                return bad_request(message=message_data)
            else:
                # Object was found, do something with it
                room.delete()
                return ok(message='Successfully deleted the room')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the room')

# Create your views here.
class ManageAmenities(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            amenities_serializer = AmenitiesSerializer(data=data)
            if amenities_serializer.is_valid():
                amenities_serializer.save()
                message = f"{amenities_serializer.validated_data.get('name')} created Successfully "
                return created(message=message)
            else:
                return bad_request(message=amenities_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create room')

    def get(self, request, id=None):
        try:
            if id is not None:
                all_amenities = RoomAmeneties.objects.filter(hotel=id).order_by('-created_datetime')
                resultdata=[]
                if all_amenities.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_amenities, request)
                    serializer = AmenetiesListingSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)
            else:
                bad_request(message="Hotel id is missing")
            

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get amenities list')

    def patch(self, request):
        try:
            payload_dict = request.data
            id = request.data.get('id', None)
            print(id)
            amenity = RoomAmeneties.objects.get(id=id)
            serializer = AmenetiesListingSerializer(amenity, data=payload_dict, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"{serializer.validated_data.get('name')} updated successfully"
                return ok(message=message)
        except Exception as err:
                print(traceback.format_exc())
                return internal_server_error(message='Failed to update amenity')

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            try:
                amenity = RoomAmeneties.objects.filter(id=id).first()
            except RoomAmeneties.DoesNotExist:
                # Handle the case where the object is not found
                message_data = "Room not found with id : ".format(room_id)
                return bad_request(message=message_data)
            else:
                # Object was found, do something with it
                amenity.delete()
                return ok(message='Successfully deleted the amenity')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the amenity')

# Create your views here.
class ManageSerices(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            payload_dict = request.data
            service_serializer = ServicesSerializer(data=payload_dict)
            if service_serializer.is_valid():
                service_serializer.save()
                message = f"{service_serializer.validated_data.get('name')} created Successfully "
                return created(message=message)
            else:
                return bad_request(message=service_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create service')

    def get(self, request, id=None):
        try:
             if id is not None:
                all_amenities = RoomServices.objects.filter(hotel=id).order_by('-created_datetime')
                resultdata=[]
                if all_amenities.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_amenities, request)
                    serializer = ServicesListingSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get service list')

    def patch(self, request):
        try:
            payload_dict = request.data
            id = request.data.get('id', None)
            print(payload_dict)
            service = RoomServices.objects.get(id=id)
            serializer = ServicesSerializer(service, data=payload_dict, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"{serializer.validated_data.get('name')} updated successfully"
                return ok(message=message)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update service')

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            try:
                service = RoomServices.objects.filter(id=id).first()
            except RoomServices.DoesNotExist:
                # Handle the case where the object is not found
                message_data = "Room not found with id : ".format(room_id)
                return bad_request(message=message_data)
            else:
                # Object was found, do something with it
                service.delete()
                return ok(message='Successfully deleted the service')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the service')

# Create your views here.
class ManageBedTypes(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            payload_dict = request.data

            bed_serializer = BedTypeSerializer(data=payload_dict)
            if bed_serializer.is_valid():
                bed_serializer.save()
                message = f"{bed_serializer.validated_data.get('name')} created Successfully "
                return created(message=message)
            else:
                return bad_request(message=bed_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create room')

    def get(self, request, id=None):
        try:
            if id is not None:
                all_types = BedType.objects.filter(hotel=id).order_by('-created_datetime')
                resultdata=[]
                if all_types.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_types, request)
                    serializer = BedTypeListingSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get type list')

    def patch(self, request):
        try:
            payload_dict = request.data
            id = request.data.get('id', None)
            type = BedType.objects.get(id=id)
            serializer = BedTypeSerializer(type, data=payload_dict, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"{serializer.validated_data.get('name')} updated successfully"
                return ok(message=message)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update type')

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            try:
                type = BedType.objects.filter(id=id).first()
            except Room.DoesNotExist:
                # Handle the case where the object is not found
                message_data = "Type not found with id : ".format(room_id)
                return bad_request(message=message_data)
            else:
                # Object was found, do something with it
                type.delete()
                return ok(message='Successfully deleted the type')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the type')
