from django.urls import path
from . import views

urlpatterns = [
    path('organization/', views.ManageOrganization.as_view()),
]
