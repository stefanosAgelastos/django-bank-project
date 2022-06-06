from django.urls import path
from rest_framework.authtoken import views
from .api import AccountExists, Transfer


app_name = "bank_api"

urlpatterns = [
    path('account/<int:pk>', AccountExists.as_view()),
    path('transaction/<int:pk>', Transfer.as_view()),
    path('transaction', Transfer.as_view()),
    path('rest-auth/', views.obtain_auth_token),
]
