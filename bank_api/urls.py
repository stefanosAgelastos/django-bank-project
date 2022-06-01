from django.urls import path, include
from .api import AccountExists, Transfer


app_name = "bank_api"

urlpatterns = [
    path('account/<int:pk>', AccountExists.as_view()),
    path('transaction/<int:pk>', Transfer.as_view()),
    path('transaction', Transfer.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
]
