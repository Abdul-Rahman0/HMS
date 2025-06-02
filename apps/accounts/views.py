from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import User, Role
from django.contrib.auth.hashers import make_password
import re

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return render(request, 'home.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Redirect based on user role
            if user.role.name == 'student':
                return redirect('student_dashboard')
            elif user.role.name == 'receptionist':
                return redirect('receptionist_dashboard')
            elif user.role.name == 'maintenance':
                return redirect('maintenance_dashboard')
            elif user.role.name == 'housekeeping':
                return redirect('housekeeping_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role_name = request.POST.get('role')
        
        # Validate password
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'auth/signup.html')
        
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return render(request, 'auth/signup.html')
        
        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
            return render(request, 'auth/signup.html')
        
        if not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain at least one number.')
            return render(request, 'auth/signup.html')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request, 'auth/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'auth/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'auth/signup.html')
        
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            messages.error(request, 'Invalid role selected.')
            return render(request, 'auth/signup.html')
        
        # Create user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    
    return render(request, 'auth/signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def debug_home(request):
    return HttpResponse("DEBUG: Home page is working!")

@login_required
def user_management(request):
    # Get filter parameters
    role = request.GET.get('role')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    # Start with all users
    users = User.objects.all()
    
    # Apply filters
    if role:
        users = users.filter(role=role)
    if status:
        users = users.filter(is_active=status == 'active')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'auth/user_management.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('user_management')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('user_management')
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        
        messages.success(request, f'User {username} created successfully.')
        return redirect('user_management')
    
    return redirect('user_management')

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == '1'
        
        # Check if username or email already exists (excluding current user)
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, 'Username already exists.')
            return redirect('user_management')
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, 'Email already exists.')
            return redirect('user_management')
        
        # Update user
        user.username = username
        user.email = email
        user.role = role
        user.is_active = is_active
        user.save()
        
        messages.success(request, f'User {username} updated successfully.')
        return redirect('user_management')
    
    return redirect('user_management')

@login_required
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} activated successfully.')
    return redirect('user_management')

@login_required
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} deactivated successfully.')
    return redirect('user_management')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('edit_profile')
    
    return render(request, 'auth/edit_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Verify current password
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')
        
        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')
        
        # Update password
        user.set_password(new_password)
        user.save()
        
        # Re-authenticate user
        login(request, user)
        messages.success(request, 'Password changed successfully.')
        return redirect('change_password')
    
    return render(request, 'auth/change_password.html')

@login_required
def student_dashboard(request):
    if request.user.role.name != 'student':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return render(request, 'student/dashboard.html')

@login_required
def receptionist_dashboard(request):
    if request.user.role.name != 'receptionist':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return render(request, 'receptionist/dashboard.html')

@login_required
def maintenance_dashboard(request):
    if request.user.role.name != 'maintenance':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return render(request, 'maintenance/dashboard.html')

@login_required
def housekeeping_dashboard(request):
    if request.user.role.name != 'housekeeping':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return render(request, 'housekeeping/dashboard.html')
