from django.urls import path
from . import views


app_name = "bank"

urlpatterns = [
    path('', views.index, name='index'),
    path('index_customer/', views.index_customer, name='index_customer'),
    path('index_teller/', views.index_teller, name='index_teller'),
]
