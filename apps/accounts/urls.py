from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Dashboard URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('maintenance/dashboard/', views.maintenance_dashboard, name='maintenance_dashboard'),
    path('housekeeping/dashboard/', views.housekeeping_dashboard, name='housekeeping_dashboard'),
    
    # User Management URLs
    path('users/', views.user_management, name='user_management'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/activate/', views.activate_user, name='activate_user'),
    path('users/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    
    # Profile URLs
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('api/dashboard/user-stats/', views.get_user_stats, name='user_stats'),
    path('api/dashboard/payment-status/', views.get_payment_status, name='payment_status'),
] 