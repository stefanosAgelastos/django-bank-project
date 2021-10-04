from django.urls import path
from . import views


app_name = "bank"

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
