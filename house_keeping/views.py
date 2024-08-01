from django.shortcuts import render,get_object_or_404
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import traceback
from .serilizer import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from staff.models import staffTable
from rooms.models import roomsTable
# Create your views here.
class ManageHouseKeeping(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = request.data
        staffId = payload.get('staff', 0)
        roomId = payload.get('room', 0)
        if staffId:
            staff = staffTable.objects.get(pk=staffId)
            payload.pop('staff') 
            payload['staff']=staff
        else:
             return bad_request("Staff not exist")
        if roomId:
            room = roomsTable.objects.get(pk=roomId)
            payload.pop('room') 
            payload['room']=room
        else:
             return bad_request("Room not exist")
        scheulder=houseKeepingTable.objects.create(
            chores=request.data['chores'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            time=request.data['time'],
            status=request.data['status'],
            staff=staff,
            room=room
            )
        scheulder.save()
        if scheulder:
            message = "Cleaning schedule created successfully "   
            return created(message=message)                    
        return internal_server_error(message=serializer.errors)

    def get(self, request):
        try: 

            resultdata=[]
            if all_schedules.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10

                serializer = HouseKeepingSerializerGettter(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return ok(data=resultdata)
            
        except Exception as err:

            return internal_server_error(message='Failed to get schedule list')

    def patch(self, request):
        try:
            payload = request.data
            scheduler_id = payload.get('id', 0)
            staff_id = payload.get('staff', 0)
            room_id = payload.get('room', 0)
            
            # Get the schedule object or return a bad request if not found
            schedule = get_object_or_404(houseKeepingTable, pk=scheduler_id)
            
            # Handle staff
            if staff_id:
                staff = get_object_or_404(staffTable, pk=staff_id)
                schedule.staff = staff
            else:
                return JsonResponse({'error': 'Staff does not exist'}, status=400)
            
            # Handle room
            if room_id:
                room = get_object_or_404(roomsTable, pk=room_id)
                schedule.room = room
            else:
                return JsonResponse({'error': 'Room does not exist'}, status=400)
            
            # Update the fields
            schedule.chores = payload.get('chores', schedule.chores)
            schedule.start_date = payload.get('start_date', schedule.start_date)
            schedule.end_date = payload.get('end_date', schedule.end_date)
            schedule.time = payload.get('time', schedule.time)
            schedule.status = payload.get('status', schedule.status)
            
            # Save the updated schedule
            schedule.save()
            
            message = "Cleaning schedule updated successfully"
            return ok(message= message)
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update schedule')

    def delete(self, request):
        try: 
            scheduleId= request.GET.get('id', None)
            try:
                schedule = houseKeepingTable.objects.filter(id=scheduleId).first()
            except houseKeepingTable.DoesNotExist:
                # Handle the case where the object is not found
                messageData="Schedule not found with id : ".format(scheduleId)
                return bad_request(message=messageData)
            else:
                # Object was found, do something with it
                schedule.delete()
                return ok(message='Successfully deleted the Schedule')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the Schedule')
