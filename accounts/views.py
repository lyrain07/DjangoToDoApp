from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def home(request):
    """Redirect to login or todo list based on authentication"""
    if request.user.is_authenticated:
        return redirect('todoapp:index')
    return redirect('accounts:login')

def register_view(request):
    """Handle user registration"""
    # If user is already logged in, redirect to todo list
    if request.user.is_authenticated:
        return redirect('todoapp:index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create new user
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            # Log the user in automatically after registration
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Account created successfully!')
            return redirect('todoapp:index')
        else:
            # Show errors if form is invalid
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Handle user login"""
    # If user is already logged in, redirect to todo list
    if request.user.is_authenticated:
        return redirect('todoapp:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Try to authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Login successful
                login(request, user)
                
                # Set session expiry based on remember_me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('todoapp:index')
            else:
                # Invalid credentials
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='accounts:login')
def logout_view(request):
    """Handle user logout"""
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye {username}! Logged out successfully!')
    return redirect('accounts:login')

