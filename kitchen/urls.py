from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.ManageKitchen.as_view()),
    path('manage/<int:id>/', views.ManageKitchen.as_view()),
    path('inventory/', views.ManageKitchenInventory.as_view()),
    path('inventory/<int:id>/', views.ManageKitchenInventory.as_view()),
    path('restock/', views.ManageKitchenRestock.as_view()),
    path('expense/', views.ManageKitchenExpense.as_view()),
    path('expense/<int:id>/', views.ManageKitchenExpense.as_view()),
    path('revenue/', views.ManageKitchenRevenue.as_view()),
    path('revenue/<int:id>/', views.ManageKitchenRevenue.as_view()),
    path('financialStatement/', views.ManageKitchenFinancialStatement.as_view()),

]
