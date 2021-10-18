from django.urls import path
from . import views


app_name = "bank"

urlpatterns = [
    path('', views.index, name='index'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('account_details/<int:pk>/', views.account_details, name='account_details'),
    path('transaction_details/<int:transaction>/', views.transaction_details, name='transaction_details'),
    path('make_transfer/', views.make_transfer, name='make_transfer'),
    path('make_loan/', views.make_loan, name='make_loan'),

    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_search_partial/', views.staff_search_partial, name='staff_search_partial'),
    path('staff_customer_details/<int:pk>/', views.staff_customer_details, name='staff_customer_details'),
    path('staff_account_list_partial/<int:pk>/', views.staff_account_list_partial, name='staff_account_list_partial'),
    path('staff_account_details/<int:pk>/', views.staff_account_details, name='staff_account_details'),
    path('staff_new_account_partial/<int:user>/', views.staff_new_account_partial, name='staff_new_account_partial'),
    path('staff_new_customer/', views.staff_new_customer, name='staff_new_customer'),
]
