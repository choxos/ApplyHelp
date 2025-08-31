from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import EmailTemplate, ApplicationTracker, CommunicationTip, EmailLog, ApplicationDocument


class CommunicationsDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'communications/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'recent_applications': ApplicationTracker.objects.filter(user=user)[:5],
            'recent_emails': EmailLog.objects.filter(user=user)[:5],
            'pending_applications': ApplicationTracker.objects.filter(
                user=user, status__in=['preparing', 'submitted', 'under_review']
            ).count(),
            'communication_tips': CommunicationTip.objects.filter(is_active=True)[:3],
        })
        return context


class EmailTemplateListView(ListView):
    model = EmailTemplate
    template_name = 'communications/templates.html'
    context_object_name = 'templates'
    
    def get_queryset(self):
        return EmailTemplate.objects.filter(is_active=True).order_by('template_type', 'formality_level')


class EmailTemplateDetailView(DetailView):
    model = EmailTemplate
    template_name = 'communications/template_detail.html'
    context_object_name = 'template'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sample variables for preview
        context['sample_variables'] = {
            'name': self.request.user.get_full_name() if self.request.user.is_authenticated else 'Your Name',
            'university': 'Sample University',
            'professor': 'Professor Smith',
            'program': 'Master of Science',
            'field': 'Computer Science',
        }
        return context


class EmailComposeView(LoginRequiredMixin, TemplateView):
    template_name = 'communications/compose.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        template_id = self.request.GET.get('template')
        if template_id:
            try:
                template = EmailTemplate.objects.get(id=template_id, is_active=True)
                context['selected_template'] = template
            except EmailTemplate.DoesNotExist:
                pass
                
        context['templates'] = EmailTemplate.objects.filter(is_active=True)
        return context


class ApplicationTrackerListView(LoginRequiredMixin, ListView):
    model = ApplicationTracker
    template_name = 'communications/applications.html'
    context_object_name = 'applications'
    paginate_by = 10
    
    def get_queryset(self):
        return ApplicationTracker.objects.filter(user=self.request.user).order_by('-updated_at')


class ApplicationTrackerCreateView(LoginRequiredMixin, CreateView):
    model = ApplicationTracker
    template_name = 'communications/application_create.html'
    fields = ['university', 'program', 'application_title', 'priority', 'application_deadline',
             'supervisor_name', 'supervisor_email', 'research_area', 'notes']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, _('Application tracker created successfully!'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('communications:application_detail', kwargs={'pk': self.object.pk})


class ApplicationTrackerDetailView(LoginRequiredMixin, DetailView):
    model = ApplicationTracker
    template_name = 'communications/application_detail.html'
    context_object_name = 'application'
    
    def get_queryset(self):
        return ApplicationTracker.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = self.get_object()
        
        context.update({
            'documents': application.documents.all(),
            'emails': application.email_logs.all().order_by('-sent_date'),
        })
        return context


class ApplicationTrackerEditView(LoginRequiredMixin, UpdateView):
    model = ApplicationTracker
    template_name = 'communications/application_edit.html'
    fields = ['status', 'priority', 'application_deadline', 'submission_date', 'decision_date',
             'supervisor_name', 'supervisor_email', 'research_area', 'funding_status', 
             'application_fee', 'notes', 'progress_notes']
    
    def get_queryset(self):
        return ApplicationTracker.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, _('Application tracker updated successfully!'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('communications:application_detail', kwargs={'pk': self.object.pk})


class CommunicationTipsView(ListView):
    model = CommunicationTip
    template_name = 'communications/tips.html'
    context_object_name = 'tips'
    
    def get_queryset(self):
        return CommunicationTip.objects.filter(is_active=True).order_by('-priority', 'title')


class EmailLogView(LoginRequiredMixin, ListView):
    model = EmailLog
    template_name = 'communications/email_log.html'
    context_object_name = 'emails'
    paginate_by = 20
    
    def get_queryset(self):
        return EmailLog.objects.filter(user=self.request.user).order_by('-sent_date')