from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.ManageStaff.as_view()),
    path('manage/<int:id>/', views.ManageStaff.as_view()),
]
