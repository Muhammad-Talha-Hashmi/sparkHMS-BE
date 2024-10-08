from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.ManageRooms.as_view()),
    path('manage/<int:id>/', views.ManageRooms.as_view()),
    path('listing/', views.ManageListingRooms.as_view()),
    path('listing/<int:id>/', views.ManageListingRooms.as_view()),
    path('amenities/', views.ManageAmenities.as_view()),
    path('amenities/<int:id>/', views.ManageAmenities.as_view()),
    path('services/', views.ManageSerices.as_view()),
    path('services/<int:id>/', views.ManageSerices.as_view()),
    path('bedtype/', views.ManageBedTypes.as_view()),
    path('bedtype/<int:id>/', views.ManageBedTypes.as_view()),
    path('booking/', views.ManageBooking.as_view()),
    path('booking/<int:id>/', views.ManageBooking.as_view()),
    path('available/', views.ManageAvailability.as_view()),
    path('available/<int:id>/', views.ManageAvailability.as_view()),
    path('bookingById/<int:id>/', views.BookingDetail.as_view()),
    path('invoiceById/<int:id>/', views.InvoiceDetail.as_view()),
    path('isCheckInOut/', views.CheckInOut.as_view()),
    path('orderKitchen/', views.KitchenOrderView.as_view()),
    path('orderKitchen/<int:id>/', views.KitchenOrderView.as_view()),
]
