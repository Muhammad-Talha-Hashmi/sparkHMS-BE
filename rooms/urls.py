from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.ManageRooms.as_view()),
]
