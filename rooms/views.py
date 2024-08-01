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
                    data = request.data
                    amenities = data['amenities']
                    amenities_ids_list = []
                    for name in amenities:
                        amenities_instance, _ = amenitiesTable.objects.get_or_create(name=name)
                        amenities_id = amenities_instance.id
                        amenities_ids_list.append(amenities_id)
                    
                    payload_dict = {}
                    for k,v in data.items():
                        payload_dict[k] = v
                    payload_dict['amenities'] = amenities_ids_list
                    
                    room_serializer = RoomsSerializer(data=payload_dict)
                    if room_serializer.is_valid():
                        room_serializer.save()
                        message = f"{room_serializer.validated_data.get('room')} created Successfully "
                    return created(message=message)

                except Exception as err:
                    print(traceback.format_exc())
                    return internal_server_error(message='Failed to create room')

    def get(self, request):
        try: 
            all_rooms = roomsTable.objects.order_by('-created_date')
            resultdata=[]
            if all_rooms.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_rooms, request)
                serializer = RoomsSerializerGetter(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get room list')

    def patch(self, request):
        try:
            data=request.data
            roomId= request.data.get('id',None)
            print(roomId)
            room = roomsTable.objects.get(id=roomId)
            amenities = data.get('amenities', [])
            if 'amenities' in data:
                data.pop('amenities') 
                amenities_ids_list = []
                for name in amenities:
                    amenities_instance, _ = amenitiesTable.objects.get_or_create(name=name)
                    amenities_id = amenities_instance.id
                    amenities_ids_list.append(amenities_id)
                    print(amenities_ids_list)
                payload_dict = {}
                for k,v in data.items():
                        payload_dict[k] = v
                payload_dict['amenities'] = amenities_ids_list
                
                print(data)
                serializer = RoomsSerializer(room, data=payload_dict, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    message = f"{serializer.validated_data.get('room')} updated successfully"
                    return ok(message= message)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update room')
    def delete(self, request):
        try: 
            roomId= request.GET.get('id', None)
            try:
                room = roomsTable.objects.filter(id=roomId).first()
            except roomsTable.DoesNotExist:
                # Handle the case where the object is not found
                messageData="Room not found with id : ".format(roomId)
                return bad_request(message=messageData)
            else:
                # Object was found, do something with it
                room.delete()
                return ok(message='Successfully deleted the room')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the room')
