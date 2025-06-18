from django.urls import path
from . import views

urlpatterns = [
  
    path('api/dashboard/maintenance-stats/', views.maintenance_dashboard_stats, name='maintenance_dashboard_stats'),
    
] 