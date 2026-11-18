
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserChangeForm
from django import forms

from .models import CustomUser
from .forms import CustomUserCreationForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account was created successfully. Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.role == CustomUser.Role.ADMIN:
            return '/admin-dashboard/'
        return '/user-dashboard/'


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')
        return redirect('login')
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    if request.user.is_superuser or request.user.role == CustomUser.Role.ADMIN:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')


@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.role == CustomUser.Role.ADMIN):
        messages.error(request, 'You are not authorized to access that page.')
        return redirect('user_dashboard')
    return render(request, 'accounts/admin_dashboard.html')


@login_required
def user_dashboard(request):
    if request.user.role != CustomUser.Role.USER:
        return redirect('admin_dashboard')
    return render(request, 'accounts/user_dashboard.html')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'contact_number']


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
