from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Country, University, StudyProgram, Scholarship


class DestinationsView(TemplateView):
    template_name = 'destinations/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'countries': Country.objects.filter(is_active=True)[:8],
            'featured_universities': University.objects.filter(is_active=True)[:6],
            'recent_programs': StudyProgram.objects.filter(is_active=True)[:8],
            'scholarships': Scholarship.objects.filter(is_active=True)[:4],
        })
        return context


class CountryListView(ListView):
    model = Country
    template_name = 'destinations/countries.html'
    context_object_name = 'countries'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Country.objects.filter(is_active=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by region (if applicable)
        region = self.request.GET.get('region')
        if region:
            # Add region filtering logic if needed
            pass
            
        return queryset.order_by('name')


class CountryDetailView(DetailView):
    model = Country
    template_name = 'destinations/country_detail.html'
    context_object_name = 'country'
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.get_object()
        
        context.update({
            'universities': country.universities.filter(is_active=True)[:10],
            'scholarships': country.scholarships.filter(is_active=True)[:5],
            'programs': StudyProgram.objects.filter(
                university__country=country, is_active=True
            )[:10],
        })
        return context


class UniversityListView(ListView):
    model = University
    template_name = 'destinations/universities.html'
    context_object_name = 'universities'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = University.objects.filter(is_active=True).select_related('country')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(country__name__icontains=search_query)
            )
        
        # Filter by country
        country_code = self.request.GET.get('country')
        if country_code:
            queryset = queryset.filter(country__code=country_code)
            
        # Filter by type
        university_type = self.request.GET.get('type')
        if university_type:
            queryset = queryset.filter(university_type=university_type)
            
        return queryset.order_by('name')


class UniversityDetailView(DetailView):
    model = University
    template_name = 'destinations/university_detail.html'
    context_object_name = 'university'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        university = self.get_object()
        
        context.update({
            'programs': university.programs.filter(is_active=True),
            'scholarships': university.scholarships.filter(is_active=True),
        })
        return context


class ProgramListView(ListView):
    model = StudyProgram
    template_name = 'destinations/programs.html'
    context_object_name = 'programs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = StudyProgram.objects.filter(is_active=True).select_related('university', 'university__country')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(field_of_study__icontains=search_query) |
                Q(university__name__icontains=search_query)
            )
        
        # Filter by level
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
            
        # Filter by field
        field = self.request.GET.get('field')
        if field:
            queryset = queryset.filter(field_of_study__icontains=field)
            
        return queryset.order_by('university__name', 'name')


class ProgramDetailView(DetailView):
    model = StudyProgram
    template_name = 'destinations/program_detail.html'
    context_object_name = 'program'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.get_object()
        
        # Find similar programs
        similar_programs = StudyProgram.objects.filter(
            field_of_study__icontains=program.field_of_study.split()[0],
            level=program.level,
            is_active=True
        ).exclude(pk=program.pk)[:5]
        
        context['similar_programs'] = similar_programs
        return context


class ScholarshipListView(ListView):
    model = Scholarship
    template_name = 'destinations/scholarships.html'
    context_object_name = 'scholarships'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Scholarship.objects.filter(is_active=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(provider__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by type
        scholarship_type = self.request.GET.get('type')
        if scholarship_type:
            queryset = queryset.filter(scholarship_type=scholarship_type)
            
        # Filter Kurdish-specific scholarships
        kurdish_only = self.request.GET.get('kurdish')
        if kurdish_only:
            queryset = queryset.filter(kurdish_specific=True)
            
        return queryset.order_by('-application_deadline', 'name')


class DestinationCompareView(LoginRequiredMixin, TemplateView):
    template_name = 'destinations/compare.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get country IDs from request
        country_ids = self.request.GET.getlist('countries')
        university_ids = self.request.GET.getlist('universities')
        
        if country_ids:
            context['countries'] = Country.objects.filter(id__in=country_ids, is_active=True)
        
        if university_ids:
            context['universities'] = University.objects.filter(id__in=university_ids, is_active=True)
            
        return context


class DestinationQuizView(TemplateView):
    template_name = 'destinations/quiz.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Quiz questions and logic would be implemented here
        context['quiz_questions'] = [
            {
                'question': _('What is your current education level?'),
                'options': [
                    {'value': 'bachelor', 'text': _("Bachelor's Degree")},
                    {'value': 'master', 'text': _("Master's Degree")},
                    {'value': 'phd', 'text': _("PhD")},
                ]
            },
            {
                'question': _('What is your preferred study level?'),
                'options': [
                    {'value': 'master', 'text': _("Master's Degree")},
                    {'value': 'phd', 'text': _("PhD")},
                    {'value': 'postdoc', 'text': _("Postdoctoral")},
                ]
            },
            {
                'question': _('What is your field of study?'),
                'type': 'text'
            },
            {
                'question': _('Which region are you from?'),
                'options': [
                    {'value': 'rojhelat', 'text': _('Rojhelat')},
                    {'value': 'bashur', 'text': _('Başûr')},
                    {'value': 'bakur', 'text': _('Bakûr')},
                    {'value': 'rojava', 'text': _('Rojava')},
                    {'value': 'diaspora', 'text': _('Diaspora')},
                ]
            },
        ]
        
        return context