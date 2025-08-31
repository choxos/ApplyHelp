from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponse

from .models import Resume, CVTemplate, Education, Experience, Skill, Publication, Award


class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume_builder/list.html'
    context_object_name = 'resumes'
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).order_by('-updated_at')


class ResumeDetailView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'resume_builder/detail.html'
    context_object_name = 'resume'
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    template_name = 'resume_builder/create.html'
    fields = ['title', 'target_country', 'target_field', 'template']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.full_name = f"{self.request.user.first_name} {self.request.user.last_name}"
        form.instance.email = self.request.user.email
        form.instance.kurdish_name = self.request.user.kurdish_name
        messages.success(self.request, _('Resume created successfully!'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('resume_builder:detail', kwargs={'pk': self.object.pk})


class ResumeEditView(LoginRequiredMixin, UpdateView):
    model = Resume
    template_name = 'resume_builder/edit.html'
    fields = ['title', 'target_country', 'target_field', 'template', 'professional_summary', 'objective']
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, _('Resume updated successfully!'))
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('resume_builder:detail', kwargs={'pk': self.object.pk})


class ResumeDeleteView(LoginRequiredMixin, DeleteView):
    model = Resume
    template_name = 'resume_builder/delete.html'
    success_url = reverse_lazy('resume_builder:list')
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Resume deleted successfully!'))
        return super().delete(request, *args, **kwargs)


class ResumeBuilderView(LoginRequiredMixin, TemplateView):
    template_name = 'resume_builder/builder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        resume_id = self.request.GET.get('resume')
        if resume_id:
            try:
                resume = Resume.objects.get(id=resume_id, user=self.request.user)
                context['resume'] = resume
            except Resume.DoesNotExist:
                pass
                
        context['templates'] = CVTemplate.objects.filter(is_active=True)
        return context


class TemplateListView(ListView):
    model = CVTemplate
    template_name = 'resume_builder/templates.html'
    context_object_name = 'templates'
    
    def get_queryset(self):
        return CVTemplate.objects.filter(is_active=True).order_by('country_style', 'template_type')


class ResumeDownloadPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        # TODO: Implement PDF generation
        messages.info(request, _('PDF generation feature coming soon!'))
        return redirect('resume_builder:detail', pk=pk)


class ResumeDownloadDocView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        
        # TODO: Implement DOC generation
        messages.info(request, _('DOC generation feature coming soon!'))
        return redirect('resume_builder:detail', pk=pk)