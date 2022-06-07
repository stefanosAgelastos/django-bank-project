from django.urls import path
from rest_framework.authtoken import views
from .api import AccountExists, Transfer, TransferStatus
from rest_framework.schemas import get_schema_view
from . import views as app_views


app_name = "transfers"

urlpatterns = [

    # REST API
    path('account/<int:pk>', AccountExists.as_view()),
    path('transaction/<int:reference>', TransferStatus.as_view()),
    path('transaction', Transfer.as_view()),
    path('rest-auth/', views.obtain_auth_token),

    # HTML SNIPPETS
    path('make_transfer/', app_views.make_transfer, name='make_transfer'),
    path('transfer_status/<int:transfer_uid>/',
         app_views.transfer_status, name='transfer_status'),
    path('transfer_details/<int:transfer_uid>/',
         app_views.transfer_details, name='transfer_details'),


    # OPENAPI SPECS
    path('openapi', get_schema_view(
        title="The Bank",
        description="How to",
        version="1.0.0"
    ), name='openapi-schema'),
]
