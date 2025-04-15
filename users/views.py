from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm

from .forms import CustomUserChangeForm, ProfilePictureForm
from .models import CustomUser
from .signup_forms import CustomSignupForm

class CustomSignupView(SignupView):
    """View for user registration."""
    template_name = 'users/register.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomSignupForm()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, _('Registration successful. Welcome!'))
        return response

@login_required
def profile(request):
    """View for user profile."""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully.'))
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Class-based view for updating user profile."""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully.'))
        return super().form_valid(form)

@login_required
def change_avatar(request):
    """View for changing user's profile picture."""
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile picture updated successfully.'))
            return redirect('users:profile')
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'users/change_avatar.html', {'form': form})
