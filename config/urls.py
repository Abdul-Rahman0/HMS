"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('login/', views.login_view, name='login'),
    # path('signup/', views.signup_view, name='signup'),
    path('accounts/', include('apps.accounts.urls')),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    
    # Public password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # # Dashboard URLs
    # path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    # path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    # path('maintenance/dashboard/', views.maintenance_dashboard, name='maintenance_dashboard'),
    # path('housekeeping/dashboard/', views.housekeeping_dashboard, name='housekeeping_dashboard'),
    
    # User management URLs 
    path('users/', views.user_management, name='user_management'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/activate/', views.activate_user, name='activate_user'),
    path('users/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
