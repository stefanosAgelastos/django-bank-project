from django.urls import path
from . import views


app_name = "bank"

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.index_customer, name='dashboard'),
    path('staff_dashboard/', views.index_teller, name='staff_dashboard'),
]
