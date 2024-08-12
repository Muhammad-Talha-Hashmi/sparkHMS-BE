from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.ManageRooms.as_view()),
    path('amenities/', views.ManageAmenities.as_view()),
    path('services/', views.ManageSerices.as_view()),
    path('bedtype/', views.ManageBedTypes.as_view()),
]
