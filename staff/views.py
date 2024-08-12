from django.shortcuts import render
from utils.responses import internal_server_error, bad_request, created, not_found, ok
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
import traceback
from .serializers import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ManageStaff(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        payload = request.data
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                message = f"{payload.get('name')} created Successfully "   
                return created(data=payload, message=message)                    
        return internal_server_error(message=serializer.errors)

    def get(self, request, id=None):
        try: 
            if id is not None:
                all_staffs = staffTable.objects.filter(hotel=id,is_active=True).order_by('-date_joined')
                resultdata=[]
                if all_staffs.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_staffs, request)
                    serializer = StaffSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)
            else:
                bad_request(message="Hotel id is missing")
            
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Staff')

    def patch(self, request):
        try:
            try:
                staffId= request.data.get('id',None)
                staff = staffTable.objects.get(id=staffId)
            except staffTable.DoesNotExist:
                return not_found(message="Staff not found")

            data = request.data

            serializer = StaffSerializer(staff, data=data, partial=True)
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
            staffId= request.GET.get('id', None)
            try:
                staff = staffTable.objects.filter(id=staffId).first()
            except staffTable.DoesNotExist:
                # Handle the case where the object is not found
                messageData="Staff not found with id : ".format(staffId)
                return bad_request(message=messageData)
            else:
                # Object was found, do something with it
                staff.delete()
                return ok(message='Successfully deleted the staff')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the staff')
