from django.urls import path
from rest_framework.authtoken import views
from .api import AccountExists, Transfer, TransferStatus


app_name = "transfers"

urlpatterns = [
    path('account/<int:pk>', AccountExists.as_view()),
    path('transaction/<int:reference>', TransferStatus.as_view()),
    path('transaction', Transfer.as_view()),
    path('rest-auth/', views.obtain_auth_token),
]
