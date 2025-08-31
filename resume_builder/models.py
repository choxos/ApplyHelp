from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import KurdishUser


class CVTemplate(models.Model):
    """
    Model for different CV templates adapted for different countries/regions
    """
    TEMPLATE_TYPES = [
        ('academic', _('Academic CV')),
        ('professional', _('Professional Resume')),
        ('research', _('Research-Focused CV')),
        ('creative', _('Creative Portfolio')),
    ]
    
    COUNTRY_STYLES = [
        ('us', _('US Style')),
        ('uk', _('UK Style')),
        ('eu', _('European Style')),
        ('canada', _('Canadian Style')),
        ('australia', _('Australian Style')),
        ('international', _('International Style')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_('Template Name'))
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, verbose_name=_('Template Type'))
    country_style = models.CharField(max_length=20, choices=COUNTRY_STYLES, verbose_name=_('Country Style'))
    
    description = models.TextField(verbose_name=_('Description'))
    template_file = models.FileField(upload_to='cv_templates/', verbose_name=_('Template File'), blank=True)
    preview_image = models.ImageField(upload_to='cv_previews/', verbose_name=_('Preview Image'), blank=True)
    
    # Template structure
    sections_order = models.JSONField(default=list, verbose_name=_('Sections Order'))
    formatting_guidelines = models.TextField(verbose_name=_('Formatting Guidelines'), blank=True)
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_country_style_display()})"
    
    class Meta:
        verbose_name = _('CV Template')
        verbose_name_plural = _('CV Templates')


class Resume(models.Model):
    """
    Model for user's resume/CV
    """
    user = models.ForeignKey(KurdishUser, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(CVTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=200, verbose_name=_('Resume Title'))
    target_country = models.CharField(max_length=100, verbose_name=_('Target Country'), blank=True)
    target_field = models.CharField(max_length=200, verbose_name=_('Target Field'), blank=True)
    
    # Personal Information
    full_name = models.CharField(max_length=200, verbose_name=_('Full Name'))
    kurdish_name = models.CharField(max_length=200, verbose_name=_('Kurdish Name'), blank=True)
    email = models.EmailField(verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'), blank=True)
    address = models.TextField(verbose_name=_('Address'), blank=True)
    website = models.URLField(verbose_name=_('Website/Portfolio'), blank=True)
    linkedin = models.URLField(verbose_name=_('LinkedIn'), blank=True)
    
    # Professional Summary
    professional_summary = models.TextField(verbose_name=_('Professional Summary'), blank=True)
    objective = models.TextField(verbose_name=_('Career Objective'), blank=True)
    
    # Generated files
    pdf_file = models.FileField(upload_to='generated_cvs/', verbose_name=_('Generated PDF'), blank=True)
    doc_file = models.FileField(upload_to='generated_cvs/', verbose_name=_('Generated DOC'), blank=True)
    
    is_primary = models.BooleanField(default=False, verbose_name=_('Primary Resume'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    class Meta:
        verbose_name = _('Resume')
        verbose_name_plural = _('Resumes')


class Education(models.Model):
    """
    Model for education entries in resume
    """
    DEGREE_LEVELS = [
        ('high_school', _('High School')),
        ('diploma', _('Diploma')),
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('phd', _('PhD')),
        ('postdoc', _('Postdoctoral')),
        ('certificate', _('Certificate')),
    ]
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    
    degree_level = models.CharField(max_length=20, choices=DEGREE_LEVELS, verbose_name=_('Degree Level'))
    degree_title = models.CharField(max_length=200, verbose_name=_('Degree Title'))
    field_of_study = models.CharField(max_length=200, verbose_name=_('Field of Study'), blank=True)
    
    institution_name = models.CharField(max_length=200, verbose_name=_('Institution Name'))
    institution_city = models.CharField(max_length=100, verbose_name=_('City'), blank=True)
    institution_country = models.CharField(max_length=100, verbose_name=_('Country'), blank=True)
    
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'), null=True, blank=True)
    is_current = models.BooleanField(default=False, verbose_name=_('Currently Studying'))
    
    gpa = models.CharField(max_length=20, verbose_name=_('GPA/Grade'), blank=True)
    thesis_title = models.CharField(max_length=500, verbose_name=_('Thesis Title'), blank=True)
    supervisor = models.CharField(max_length=200, verbose_name=_('Supervisor'), blank=True)
    
    description = models.TextField(verbose_name=_('Description'), blank=True)
    achievements = models.TextField(verbose_name=_('Achievements/Honors'), blank=True)
    
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    
    def __str__(self):
        return f"{self.degree_title} at {self.institution_name}"
    
    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Education')
        ordering = ['-end_date', '-start_date']


class Experience(models.Model):
    """
    Model for work/research experience entries in resume
    """
    EXPERIENCE_TYPES = [
        ('work', _('Work Experience')),
        ('research', _('Research Experience')),
        ('internship', _('Internship')),
        ('volunteer', _('Volunteer Work')),
        ('teaching', _('Teaching Experience')),
        ('project', _('Project Experience')),
    ]
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES, verbose_name=_('Experience Type'))
    job_title = models.CharField(max_length=200, verbose_name=_('Job Title/Position'))
    company_name = models.CharField(max_length=200, verbose_name=_('Organization/Company'))
    company_city = models.CharField(max_length=100, verbose_name=_('City'), blank=True)
    company_country = models.CharField(max_length=100, verbose_name=_('Country'), blank=True)
    
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'), null=True, blank=True)
    is_current = models.BooleanField(default=False, verbose_name=_('Current Position'))
    
    description = models.TextField(verbose_name=_('Job Description'))
    achievements = models.TextField(verbose_name=_('Key Achievements'), blank=True)
    skills_used = models.TextField(verbose_name=_('Skills Used'), blank=True)
    
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    class Meta:
        verbose_name = _('Experience')
        verbose_name_plural = _('Experience')
        ordering = ['-end_date', '-start_date']


class Skill(models.Model):
    """
    Model for skills in resume
    """
    SKILL_CATEGORIES = [
        ('technical', _('Technical Skills')),
        ('language', _('Language Skills')),
        ('software', _('Software Skills')),
        ('research', _('Research Skills')),
        ('interpersonal', _('Interpersonal Skills')),
        ('other', _('Other Skills')),
    ]
    
    PROFICIENCY_LEVELS = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
        ('expert', _('Expert')),
        ('native', _('Native')),  # For languages
    ]
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, verbose_name=_('Skill Category'))
    name = models.CharField(max_length=100, verbose_name=_('Skill Name'))
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, verbose_name=_('Proficiency Level'))
    
    description = models.TextField(verbose_name=_('Description'), blank=True)
    years_of_experience = models.IntegerField(verbose_name=_('Years of Experience'), null=True, blank=True)
    
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    
    def __str__(self):
        return f"{self.name} ({self.get_proficiency_display()})"
    
    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['category', 'order']


class Publication(models.Model):
    """
    Model for publications/research outputs in resume
    """
    PUBLICATION_TYPES = [
        ('journal', _('Journal Article')),
        ('conference', _('Conference Paper')),
        ('book', _('Book')),
        ('chapter', _('Book Chapter')),
        ('thesis', _('Thesis')),
        ('report', _('Technical Report')),
        ('patent', _('Patent')),
        ('other', _('Other')),
    ]
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='publications')
    
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES, verbose_name=_('Publication Type'))
    title = models.CharField(max_length=500, verbose_name=_('Title'))
    authors = models.CharField(max_length=500, verbose_name=_('Authors'))
    publication_venue = models.CharField(max_length=300, verbose_name=_('Journal/Conference/Publisher'), blank=True)
    
    publication_date = models.DateField(verbose_name=_('Publication Date'), null=True, blank=True)
    volume = models.CharField(max_length=20, verbose_name=_('Volume'), blank=True)
    issue = models.CharField(max_length=20, verbose_name=_('Issue'), blank=True)
    pages = models.CharField(max_length=20, verbose_name=_('Pages'), blank=True)
    
    doi = models.CharField(max_length=200, verbose_name=_('DOI'), blank=True)
    url = models.URLField(verbose_name=_('URL'), blank=True)
    
    abstract = models.TextField(verbose_name=_('Abstract'), blank=True)
    keywords = models.CharField(max_length=500, verbose_name=_('Keywords'), blank=True)
    
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    
    def __str__(self):
        return f"{self.title} ({self.publication_date.year if self.publication_date else 'N/A'})"
    
    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
        ordering = ['-publication_date', 'order']


class Award(models.Model):
    """
    Model for awards and achievements in resume
    """
    AWARD_TYPES = [
        ('academic', _('Academic Award')),
        ('research', _('Research Award')),
        ('professional', _('Professional Award')),
        ('scholarship', _('Scholarship')),
        ('competition', _('Competition Award')),
        ('honor', _('Honor/Recognition')),
        ('certificate', _('Certificate')),
        ('other', _('Other')),
    ]
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='awards')
    
    award_type = models.CharField(max_length=20, choices=AWARD_TYPES, verbose_name=_('Award Type'))
    title = models.CharField(max_length=200, verbose_name=_('Award Title'))
    issuing_organization = models.CharField(max_length=200, verbose_name=_('Issuing Organization'))
    
    date_received = models.DateField(verbose_name=_('Date Received'))
    description = models.TextField(verbose_name=_('Description'), blank=True)
    
    order = models.IntegerField(default=0, verbose_name=_('Display Order'))
    
    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"
    
    class Meta:
        verbose_name = _('Award')
        verbose_name_plural = _('Awards')
        ordering = ['-date_received', 'order']