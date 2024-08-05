from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ManageOrganization.as_view()),
]
