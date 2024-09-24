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
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.utils import timezone




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
             status = request.GET.get('status', None)
             if id is not None:
                if status == 'booked':
                    all_rooms = Room.objects.filter(hotel=id, status=True).order_by('-created_datetime')
                    resultdata=[]
                    if all_rooms.exists():
                        paginator = PageNumberPagination()
                        paginator.page_size = 10
                        result_page = paginator.paginate_queryset(all_rooms, request)
                        serializer = RoomGetterSerializer(result_page, context={'request': request}, many=True)
                        return paginator.get_paginated_response(serializer.data)
                    else:
                        return ok(data=resultdata)
                elif status == 'available':
                    all_rooms = Room.objects.filter(hotel=id, status=False).order_by('-created_datetime')
                    resultdata=[]
                    if all_rooms.exists():
                        paginator = PageNumberPagination()
                        paginator.page_size = 10
                        result_page = paginator.paginate_queryset(all_rooms, request)
                        serializer = RoomGetterSerializer(result_page, context={'request': request}, many=True)
                        return paginator.get_paginated_response(serializer.data)
                    else:
                        return ok(data=resultdata)
                else:
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
class ManageListingRooms(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
             status = request.GET.get('status', None)
             if id is not None:
                    all_rooms = Room.objects.filter(hotel=id).order_by('-created_datetime')
                    resultdata=[]
                    if all_rooms.exists():
                        paginator = PageNumberPagination()
                        paginator.page_size = 10
                        result_page = paginator.paginate_queryset(all_rooms, request)
                        serializer = RoomGetSerializer(result_page, context={'request': request}, many=True)
                        return paginator.get_paginated_response(serializer.data)
                    else:
                        return ok(data=resultdata)

                

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get room list')

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


# Create your views here.
class ManageBooking(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            payload_dict = request.data
            room_id= request.data.get('room',None)
            if  room_id is not None:
                room = get_object_or_404(Room, id=room_id)
                booking_serializer = BookingSerializer(data=payload_dict)
                if booking_serializer.is_valid():
                    booking = booking_serializer.save()
                    room.status = True
                    room.save()
                    total_amount = room.price
                    # Create an invoice
                    invoice = Invoice.objects.create(
                        booking=booking,
                        amount=total_amount  # Assuming total_amount is in the payload
                    )
                    
                    # Update invoice_number after the first save
                    invoice.invoice_number = f"INV-{invoice.id}"
                    invoice.save()
                    message = f"{booking_serializer.validated_data.get('guest_name')} booking created Successfully "
                    return created(message=message)
                else:
                    return bad_request(message=booking_serializer.errors)
            else:
                 return bad_request(message="Room Id is missing")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to create booking')

    def get(self, request, id=None):
        try:
            if id is not None:
                all_types = RoomBooking.objects.filter(hotel=id).order_by('-created_datetime')
                resultdata=[]
                if all_types.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(all_types, request)
                    serializer = BookingListingSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get booking list')

    def patch(self, request):
        try:
            payload_dict = request.data
            id = request.data.get('id', None)
            type = RoomBooking.objects.get(id=id)
            serializer = BookingSerializer(type, data=payload_dict, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"{serializer.validated_data.get('name')} updated successfully"
                return ok(message=message)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update booking')

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            try:
                booking = RoomBooking.objects.filter(id=id).first()
                serializer = BookingSerializer(booking)
                room_id= serializer.data.get('room',None)
                if  room_id is not None:
                    room = get_object_or_404(Room, id=room_id)
        
            except RoomBooking.DoesNotExist:
                # Handle the case where the object is not found
                message_data = "Type not found with id : ".format(room_id)
                return bad_request(message=message_data)
            else:
                # Object was found, do something with it
                booking.delete()
                room.status = False
                room.save()
                return ok(message='Successfully deleted the booking')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the booking')

# Create your views here.
class ManageAvailability(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            nop = request.GET.get('nop', None)
            startDate = request.GET.get('startDate', None)
            endDate = request.GET.get('endDate', None)
            if startDate:
                startDate = parse_datetime(startDate)
                if startDate is not None:
                    startDate = timezone.make_aware(startDate)
            
            if endDate:
                endDate = parse_datetime(endDate)
                if endDate is not None:
                    endDate = timezone.make_aware(endDate)
            if id is not None:
                # Base queryset for available rooms in the specified hotel
                rooms = Room.objects.filter(hotel=id)
                print(rooms)
                # Filter by room capacity if 'nop' is provided
                if nop:
                    rooms = rooms.filter(capacity__gte=int(nop))
                print(rooms)
                # Filter by availability based on booking dates if startDate and endDate are provided
                if startDate and endDate:
                    rooms = rooms.exclude(
                        Q(bookings__check_in__lt=endDate) & Q(bookings__check_out__gt=startDate)
                    )

                rooms = rooms.order_by('-created_date')
                
                resultdata = []
                if rooms.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(rooms, request)
                    serializer = RoomGetterSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get room list')

# Create your views here.
class BookingDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
             if id is not None:
                booking = RoomBooking.objects.filter(id=id).first()
                resultdata=[]
                serializer = BookingDetailSerializer(booking)
                return ok(data=serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Booking details')

# Create your views here.
class InvoiceDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
             if id is not None:
                invoice_instance = Invoice.objects.filter(booking=id).first()
                resultdata=[]
                serializer = InvoiceDetailSerializer(invoice_instance)
                return ok(data=serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Invoice details')

# Create your views here.
class CheckInOut(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            booking_id= request.data.get('id',None)
            print(booking_id)
            check_in_status= request.data.get('checkIn',None)
            booking = get_object_or_404(RoomBooking, id=booking_id)

            if check_in_status:
                booking.update_check_in_status(True)
                return ok(message="Successfully check in ")
            else:
                booking.update_check_out_status(True)
                return ok(message="Successfully check out ")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Booking details')

# Create your views here.
class KitchenOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get order data
            order_data = request.data.get('order')
            # Get order items data
            order_items_data = request.data.get('order_items')

            # Serialize the order data
            order_serializer = OrderSerializer(data=order_data)
            
            if order_serializer.is_valid():
                order = order_serializer.save()  # Save the order

                # Process and save each order item
                for item_data in order_items_data:
                    item_data['order'] = order.id  # Set the order foreign key
                    order_item_serializer = OrderItemSerializer(data=item_data)
                    
                    if order_item_serializer.is_valid():
                        order_item_serializer.save()  # Save the order item
                    else:
                        return Response(order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return created(message="Order started")
            return bad_request(message=order_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Booking details')

    def get(self, request, id=None):
        try:
            if id is not None:
                queryset = Order.objects.all().prefetch_related('order_items')  # Prefetch related data
                queryset = queryset.filter(booking_id=id)  # Filter by booking ID
                resultdata=[]
                if queryset.exists():
                    paginator = PageNumberPagination()
                    paginator.page_size = 10
                    result_page = paginator.paginate_queryset(queryset, request)
                    serializer = OrderGetterSerializer(result_page, context={'request': request}, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    return ok(data=resultdata)

        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to get Order list')

    def patch(self, request):
        try:
            payload_dict = request.data
            id = request.data.get('id', None)
            type = RoomBooking.objects.get(id=id)
            serializer = BookingSerializer(type, data=payload_dict, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"{serializer.validated_data.get('name')} updated successfully"
                return ok(message=message)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to update booking')

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            try:
                booking = RoomBooking.objects.filter(id=id).first()
                serializer = BookingSerializer(booking)
                room_id= serializer.data.get('room',None)
                if  room_id is not None:
                    room = get_object_or_404(Room, id=room_id)
        
            except RoomBooking.DoesNotExist:
                # Handle the case where the object is not found
                message_data = "Type not found with id : ".format(room_id)
                return bad_request(message=message_data)
            else:
                # Object was found, do something with it
                booking.delete()
                room.status = False
                room.save()
                return ok(message='Successfully deleted the booking')
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message='Failed to delete the booking')
