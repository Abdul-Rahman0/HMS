from django.urls import path
from . import views

urlpatterns = [
    path('api/monthly-fee-status/', views.monthly_fee_status, name='monthly_fee_status'),
] 