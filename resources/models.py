from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import KurdishUser
from destinations.models import Country, University


class ResourceCategory(models.Model):
    """
    Model for organizing different types of resources
    """
    name = models.CharField(max_length=100, verbose_name=_('Category Name'))
    name_sorani = models.CharField(max_length=100, verbose_name=_('Name (Sorani)'), blank=True)
    name_kurmanji = models.CharField(max_length=100, verbose_name=_('Name (Kurmanji)'), blank=True)
    
    description = models.TextField(verbose_name=_('Description'), blank=True)
    icon = models.CharField(max_length=50, verbose_name=_('Icon Class'), blank=True)
    color = models.CharField(max_length=7, verbose_name=_('Category Color'), default='#007bff')
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Parent Category'))
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Resource Category')
        verbose_name_plural = _('Resource Categories')
        ordering = ['order', 'name']


class Guide(models.Model):
    """
    Model for comprehensive guides
    """
    GUIDE_TYPES = [
        ('country', _('Country Guide')),
        ('university', _('University Guide')),
        ('process', _('Process Guide')),
        ('visa', _('Visa Guide')),
        ('scholarship', _('Scholarship Guide')),
        ('career', _('Career Guide')),
        ('language', _('Language Guide')),
        ('cultural', _('Cultural Guide')),
        ('general', _('General Guide')),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    ]
    
    title = models.CharField(max_length=300, verbose_name=_('Guide Title'))
    guide_type = models.CharField(max_length=20, choices=GUIDE_TYPES, verbose_name=_('Guide Type'))
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Target Country'))
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Target University'))
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, verbose_name=_('Difficulty Level'), default='beginner')
    
    summary = models.TextField(verbose_name=_('Summary'), blank=True)
    content = models.TextField(verbose_name=_('Content'))
    steps = models.JSONField(default=list, verbose_name=_('Steps'), blank=True)
    
    author = models.ForeignKey(KurdishUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Author'))
    estimated_reading_time = models.IntegerField(verbose_name=_('Estimated Reading Time (minutes)'), default=10)
    last_updated = models.DateField(verbose_name=_('Last Updated'), auto_now=True)
    
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    helpful_votes = models.IntegerField(default=0, verbose_name=_('Helpful Votes'))
    
    slug = models.SlugField(unique=True, verbose_name=_('URL Slug'))
    meta_description = models.CharField(max_length=160, verbose_name=_('Meta Description'), blank=True)
    keywords = models.CharField(max_length=300, verbose_name=_('Keywords'), blank=True)
    
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured Guide'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Guide')
        verbose_name_plural = _('Guides')
        ordering = ['-is_featured', '-created_at']