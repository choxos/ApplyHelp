from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """
    Model for destination countries with study opportunities
    """
    name = models.CharField(max_length=100, verbose_name=_('Country Name'))
    name_sorani = models.CharField(max_length=100, verbose_name=_('Name (Sorani)'), blank=True)
    name_kurmanji = models.CharField(max_length=100, verbose_name=_('Name (Kurmanji)'), blank=True)
    code = models.CharField(max_length=3, unique=True, verbose_name=_('Country Code'))
    
    # Basic information
    flag_image = models.ImageField(upload_to='flags/', verbose_name=_('Flag'), blank=True)
    description = models.TextField(verbose_name=_('Description'))
    official_language = models.CharField(max_length=100, verbose_name=_('Official Language'))
    currency = models.CharField(max_length=50, verbose_name=_('Currency'))
    
    # Study-related information
    academic_year_start = models.CharField(max_length=20, verbose_name=_('Academic Year Start'), blank=True)
    application_deadlines = models.TextField(verbose_name=_('General Application Deadlines'), blank=True)
    
    # Cost information
    avg_tuition_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Average Tuition (USD)'), null=True, blank=True)
    avg_living_cost_usd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Average Living Cost (USD)'), null=True, blank=True)
    
    # Visa and immigration
    student_visa_type = models.CharField(max_length=50, verbose_name=_('Student Visa Type'), blank=True)
    visa_processing_time = models.CharField(max_length=100, verbose_name=_('Visa Processing Time'), blank=True)
    work_permit_allowed = models.BooleanField(default=False, verbose_name=_('Work Permit Allowed for Students'))
    post_study_work_visa = models.BooleanField(default=False, verbose_name=_('Post-Study Work Visa Available'))
    
    # Kurdish community
    kurdish_population = models.TextField(verbose_name=_('Kurdish Community Information'), blank=True)
    kurdish_organizations = models.TextField(verbose_name=_('Kurdish Organizations'), blank=True)
    
    # Ratings and difficulty
    application_difficulty = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Application Difficulty (1-5)'), default=3)
    living_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Living Quality (1-5)'), default=3)
    study_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Study Quality (1-5)'), default=3)
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']


class University(models.Model):
    """
    Model for universities in destination countries
    """
    UNIVERSITY_TYPES = [
        ('public', _('Public University')),
        ('private', _('Private University')),
        ('research', _('Research Institution')),
        ('applied', _('University of Applied Sciences')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_('University Name'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='universities')
    city = models.CharField(max_length=100, verbose_name=_('City'))
    
    # Basic information
    website = models.URLField(verbose_name=_('Official Website'), blank=True)
    logo = models.ImageField(upload_to='university_logos/', verbose_name=_('Logo'), blank=True)
    university_type = models.CharField(max_length=20, choices=UNIVERSITY_TYPES, verbose_name=_('University Type'))
    established_year = models.IntegerField(verbose_name=_('Established Year'), null=True, blank=True)
    
    # Academic information
    world_ranking = models.IntegerField(verbose_name=_('World Ranking'), null=True, blank=True)
    national_ranking = models.IntegerField(verbose_name=_('National Ranking'), null=True, blank=True)
    student_population = models.IntegerField(verbose_name=_('Student Population'), null=True, blank=True)
    international_students = models.IntegerField(verbose_name=_('International Students'), null=True, blank=True)
    
    # Languages
    instruction_languages = models.CharField(max_length=200, verbose_name=_('Languages of Instruction'))
    
    # Contact and support
    international_office_email = models.EmailField(verbose_name=_('International Office Email'), blank=True)
    admission_email = models.EmailField(verbose_name=_('Admission Email'), blank=True)
    
    # Kurdish connections
    kurdish_students_info = models.TextField(verbose_name=_('Kurdish Students Information'), blank=True)
    kurdish_friendly_supervisors = models.TextField(verbose_name=_('Kurdish-Friendly Supervisors'), blank=True)
    
    # Ratings
    academic_reputation = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Academic Reputation (1-5)'), default=3)
    research_opportunities = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Research Opportunities (1-5)'), default=3)
    international_support = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('International Student Support (1-5)'), default=3)
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}, {self.city}, {self.country.name}"
    
    class Meta:
        verbose_name = _('University')
        verbose_name_plural = _('Universities')
        ordering = ['name']


class StudyProgram(models.Model):
    """
    Model for specific study programs offered by universities
    """
    PROGRAM_LEVELS = [
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('phd', _('PhD')),
        ('postdoc', _('Postdoctoral')),
        ('professional', _('Professional Program')),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200, verbose_name=_('Program Name'))
    level = models.CharField(max_length=20, choices=PROGRAM_LEVELS, verbose_name=_('Program Level'))
    
    # Academic details
    field_of_study = models.CharField(max_length=200, verbose_name=_('Field of Study'))
    duration_months = models.IntegerField(verbose_name=_('Duration (months)'))
    credits = models.IntegerField(verbose_name=_('Total Credits'), null=True, blank=True)
    language_of_instruction = models.CharField(max_length=100, verbose_name=_('Language of Instruction'))
    
    # Application requirements
    min_gpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Minimum GPA'), null=True, blank=True)
    language_requirements = models.TextField(verbose_name=_('Language Requirements'), blank=True)
    other_requirements = models.TextField(verbose_name=_('Other Requirements'), blank=True)
    
    # Dates and deadlines
    application_deadline = models.DateField(verbose_name=_('Application Deadline'), null=True, blank=True)
    start_date = models.DateField(verbose_name=_('Program Start Date'), null=True, blank=True)
    
    # Financial information
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Tuition Fee'), null=True, blank=True)
    currency = models.CharField(max_length=10, verbose_name=_('Currency'), default='USD')
    scholarships_available = models.BooleanField(default=False, verbose_name=_('Scholarships Available'))
    
    # Additional information
    description = models.TextField(verbose_name=_('Program Description'), blank=True)
    career_prospects = models.TextField(verbose_name=_('Career Prospects'), blank=True)
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.level}) - {self.university.name}"
    
    class Meta:
        verbose_name = _('Study Program')
        verbose_name_plural = _('Study Programs')
        ordering = ['university__name', 'level', 'name']


class Scholarship(models.Model):
    """
    Model for scholarships and funding opportunities
    """
    SCHOLARSHIP_TYPES = [
        ('full', _('Full Scholarship')),
        ('partial', _('Partial Scholarship')),
        ('tuition', _('Tuition Only')),
        ('living', _('Living Expenses Only')),
        ('research', _('Research Grant')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_('Scholarship Name'))
    provider = models.CharField(max_length=200, verbose_name=_('Provider/Organization'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='scholarships', null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='scholarships', null=True, blank=True)
    
    scholarship_type = models.CharField(max_length=20, choices=SCHOLARSHIP_TYPES, verbose_name=_('Scholarship Type'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'), null=True, blank=True)
    currency = models.CharField(max_length=10, verbose_name=_('Currency'), default='USD')
    
    # Eligibility
    eligible_programs = models.ManyToManyField(StudyProgram, blank=True, verbose_name=_('Eligible Programs'))
    eligibility_criteria = models.TextField(verbose_name=_('Eligibility Criteria'))
    kurdish_specific = models.BooleanField(default=False, verbose_name=_('Kurdish-Specific Scholarship'))
    
    # Application details
    application_deadline = models.DateField(verbose_name=_('Application Deadline'), null=True, blank=True)
    application_process = models.TextField(verbose_name=_('Application Process'), blank=True)
    required_documents = models.TextField(verbose_name=_('Required Documents'), blank=True)
    
    # Contact information
    website = models.URLField(verbose_name=_('Website'), blank=True)
    contact_email = models.EmailField(verbose_name=_('Contact Email'), blank=True)
    
    description = models.TextField(verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider}"
    
    class Meta:
        verbose_name = _('Scholarship')
        verbose_name_plural = _('Scholarships')
        ordering = ['-application_deadline', 'name']