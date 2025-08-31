from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Guide, ResourceCategory


class ResourcesHomeView(TemplateView):
    template_name = 'resources/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'featured_guides': Guide.objects.filter(is_featured=True, is_published=True)[:6],
            'recent_guides': Guide.objects.filter(is_published=True).order_by('-created_at')[:8],
            'categories': ResourceCategory.objects.filter(is_active=True, parent=None).order_by('order'),
        })
        return context


class GuideListView(ListView):
    model = Guide
    template_name = 'resources/guides.html'
    context_object_name = 'guides'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Guide.objects.filter(is_published=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(keywords__icontains=search_query)
            )
        
        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by guide type
        guide_type = self.request.GET.get('type')
        if guide_type:
            queryset = queryset.filter(guide_type=guide_type)
        
        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Filter by country
        country_id = self.request.GET.get('country')
        if country_id:
            queryset = queryset.filter(country_id=country_id)
            
        return queryset.order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'categories': ResourceCategory.objects.filter(is_active=True),
            'guide_types': Guide.GUIDE_TYPES,
            'difficulty_levels': Guide.DIFFICULTY_LEVELS,
        })
        return context


class GuideDetailView(DetailView):
    model = Guide
    template_name = 'resources/guide_detail.html'
    context_object_name = 'guide'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Guide.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        guide = super().get_object(queryset)
        
        # Increment views count
        guide.views += 1
        guide.save(update_fields=['views'])
        
        return guide
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guide = self.get_object()
        
        # Get related guides
        related_guides = Guide.objects.filter(
            is_published=True,
            guide_type=guide.guide_type
        ).exclude(pk=guide.pk)[:4]
        
        if guide.category:
            related_guides = related_guides.filter(category=guide.category)
        
        context['related_guides'] = related_guides
        return context


class GuidesByCategoryView(ListView):
    model = Guide
    template_name = 'resources/guides_by_category.html'
    context_object_name = 'guides'
    paginate_by = 15
    
    def get_queryset(self):
        self.category = get_object_or_404(ResourceCategory, id=self.kwargs['category_id'], is_active=True)
        return Guide.objects.filter(category=self.category, is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context