from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .models import KurdishUser, UserProfile
from .forms import KurdishUserCreationForm, UserProfileForm


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_content'] = {
            'guides_count': 0,  # TODO: Get actual counts
            'success_stories_count': 0,
            'universities_count': 0,
            'countries_count': 0,
        }
        return context


class RegisterView(CreateView):
    model = KurdishUser
    form_class = KurdishUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, _('Welcome! Your account has been created successfully.'))
        return response


class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, _('Welcome back!'))
        return super().form_valid(form)


class LogoutView(BaseLogoutView):
    next_page = 'accounts:home'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, _('You have been logged out successfully.'))
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'recent_applications': [],  # TODO: Get user's recent applications
            'profile_completion': self.calculate_profile_completion(user),
            'recent_activities': [],  # TODO: Get recent activities
            'recommendations': [],  # TODO: Get personalized recommendations
        })
        return context
    
    def calculate_profile_completion(self, user):
        # Simple profile completion calculation
        completion = 0
        total_fields = 10  # Total important fields
        
        if user.kurdish_name:
            completion += 1
        if user.region:
            completion += 1
        if user.field_of_study:
            completion += 1
        if user.phone_number:
            completion += 1
        if user.current_city:
            completion += 1
        if hasattr(user, 'profile'):
            profile = user.profile
            if profile.biography:
                completion += 1
            if profile.cv_document:
                completion += 1
            if profile.work_experience:
                completion += 1
            if profile.technical_skills:
                completion += 1
            if profile.language_skills:
                completion += 1
        
        return int((completion / total_fields) * 100)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        context['profile'] = profile
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, _('Your profile has been updated successfully.'))
        return super().form_valid(form)