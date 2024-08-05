from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view()),
    path('login/', views.Login.as_view()),
    path('change_password/', views.ChangePassword.as_view()),
    path('delete_user/', views.DeleteUser.as_view()),
    path('user_list/', views.GetUsers.as_view()),
    path('manage/', views.ManageUsers.as_view()),
    path('manage/<int:id>/', views.ManageUsers.as_view()),
    # path('refreshToken/', views.RefreshTokenView.as_view()),
]
