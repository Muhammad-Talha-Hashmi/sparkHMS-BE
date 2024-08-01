from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.ManageStaff.as_view()),
]
