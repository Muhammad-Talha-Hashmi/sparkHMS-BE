from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ManageOrganization.as_view()),
    path('dropdown/', views.OrganizationDropdown.as_view()),
    path('hotel/', views.ManageHotel.as_view()),
    path('hotel/dropdown/', views.HotelDropdown.as_view()),
]
