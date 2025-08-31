from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class KurdishUser(AbstractUser):
    """
    Extended user model for Kurdish students with additional fields
    """
    REGION_CHOICES = [
        ('rojhelat', _('Rojhelat')),  # Eastern Kurdistan
        ('bashur', _('Başûr')),      # Southern Kurdistan
        ('bakur', _('Bakûr')),       # Northern Kurdistan
        ('rojava', _('Rojava')),     # Western Kurdistan
        ('diaspora', _('Diaspora')), # Kurdish diaspora
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('phd', _('PhD')),
        ('professional', _('Professional Degree')),
    ]
    
    KURDISH_DIALECT_CHOICES = [
        ('sorani', _('Sorani (Central Kurdish)')),
        ('kurmanji', _('Kurmanji (Northern Kurdish)')),
        ('pehlewani', _('Pehlewani (Southern Kurdish)')),
        ('zazaki', _('Zazaki (Dimli)')),
        ('gorani', _('Gorani (Hawrami)')),
    ]
    
    # Personal information
    kurdish_name = models.CharField(max_length=100, verbose_name=_('Kurdish Name'), blank=True)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name=_('Kurdish Region'))
    kurdish_dialects = models.ManyToManyField('KurdishDialect', verbose_name=_('Kurdish Dialects Spoken'), blank=True)
    
    # Academic information
    current_education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name=_('Current Education Level'))
    university_name = models.CharField(max_length=200, verbose_name=_('Current/Previous University'), blank=True)
    field_of_study = models.CharField(max_length=200, verbose_name=_('Field of Study'))
    graduation_year = models.IntegerField(verbose_name=_('Graduation Year'), null=True, blank=True)
    
    # Contact and location
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'), blank=True)
    current_city = models.CharField(max_length=100, verbose_name=_('Current City'), blank=True)
    current_country = models.CharField(max_length=100, verbose_name=_('Current Country'), blank=True)
    
    # Application preferences
    preferred_study_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name=_('Preferred Study Level'))
    research_interests = models.TextField(verbose_name=_('Research Interests'), blank=True)
    
    # Profile completion
    profile_completed = models.BooleanField(default=False, verbose_name=_('Profile Completed'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.kurdish_name or self.username} ({self.get_region_display()})"
    
    class Meta:
        verbose_name = _('Kurdish User')
        verbose_name_plural = _('Kurdish Users')


class KurdishDialect(models.Model):
    """
    Model for Kurdish language dialects
    """
    name_sorani = models.CharField(max_length=100, verbose_name=_('Name (Sorani)'))
    name_kurmanji = models.CharField(max_length=100, verbose_name=_('Name (Kurmanji)'))
    name_english = models.CharField(max_length=100, verbose_name=_('Name (English)'))
    code = models.CharField(max_length=10, unique=True, verbose_name=_('Language Code'))
    
    def __str__(self):
        return self.name_english
    
    class Meta:
        verbose_name = _('Kurdish Dialect')
        verbose_name_plural = _('Kurdish Dialects')


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(KurdishUser, on_delete=models.CASCADE, related_name='profile')
    
    # Biography and motivation
    biography = models.TextField(verbose_name=_('Biography'), blank=True)
    motivation_letter = models.TextField(verbose_name=_('General Motivation Letter'), blank=True)
    
    # Academic achievements
    gpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('GPA'), null=True, blank=True)
    academic_awards = models.TextField(verbose_name=_('Academic Awards'), blank=True)
    publications = models.TextField(verbose_name=_('Publications'), blank=True)
    
    # Experience
    work_experience = models.TextField(verbose_name=_('Work Experience'), blank=True)
    volunteer_experience = models.TextField(verbose_name=_('Volunteer Experience'), blank=True)
    
    # Skills and languages
    technical_skills = models.TextField(verbose_name=_('Technical Skills'), blank=True)
    language_skills = models.TextField(verbose_name=_('Language Skills'), blank=True)
    
    # Documents
    cv_document = models.FileField(upload_to='cvs/', verbose_name=_('CV Document'), blank=True)
    transcripts = models.FileField(upload_to='transcripts/', verbose_name=_('Academic Transcripts'), blank=True)
    certificates = models.FileField(upload_to='certificates/', verbose_name=_('Certificates'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')