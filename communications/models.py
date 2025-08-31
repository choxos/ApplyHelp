from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import KurdishUser
from destinations.models import University, StudyProgram


class EmailTemplate(models.Model):
    """
    Model for email templates for different communication scenarios
    """
    TEMPLATE_TYPES = [
        ('initial_inquiry', _('Initial Inquiry to Supervisor')),
        ('application_follow_up', _('Application Follow-up')),
        ('supervisor_introduction', _('Supervisor Introduction')),
        ('interview_request', _('Interview Request')),
        ('acceptance_response', _('Acceptance Response')),
        ('visa_inquiry', _('Visa Inquiry')),
        ('scholarship_inquiry', _('Scholarship Inquiry')),
        ('research_proposal', _('Research Proposal Email')),
        ('recommendation_request', _('Recommendation Letter Request')),
        ('general_inquiry', _('General Inquiry')),
    ]
    
    FORMALITY_LEVELS = [
        ('very_formal', _('Very Formal')),
        ('formal', _('Formal')),
        ('semi_formal', _('Semi-Formal')),
        ('informal', _('Informal')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_('Template Name'))
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, verbose_name=_('Template Type'))
    formality_level = models.CharField(max_length=20, choices=FORMALITY_LEVELS, verbose_name=_('Formality Level'))
    target_country = models.CharField(max_length=100, verbose_name=_('Target Country'), blank=True)
    
    # Email components
    subject_line = models.CharField(max_length=200, verbose_name=_('Subject Line Template'))
    greeting = models.TextField(verbose_name=_('Greeting Template'))
    body = models.TextField(verbose_name=_('Email Body Template'))
    closing = models.TextField(verbose_name=_('Closing Template'))
    signature = models.TextField(verbose_name=_('Signature Template'))
    
    # Metadata
    description = models.TextField(verbose_name=_('Description/Usage Notes'), blank=True)
    cultural_notes = models.TextField(verbose_name=_('Cultural Communication Notes'), blank=True)
    variables = models.JSONField(default=list, verbose_name=_('Template Variables'))  # List of variables like {name}, {university}
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    class Meta:
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')


class ApplicationTracker(models.Model):
    """
    Model for tracking applications to different universities/programs
    """
    APPLICATION_STATUS = [
        ('planning', _('Planning to Apply')),
        ('preparing', _('Preparing Application')),
        ('submitted', _('Application Submitted')),
        ('under_review', _('Under Review')),
        ('interview', _('Interview Stage')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('waitlisted', _('Waitlisted')),
        ('deferred', _('Deferred')),
        ('withdrawn', _('Withdrawn')),
    ]
    
    PRIORITY_LEVELS = [
        ('low', _('Low Priority')),
        ('medium', _('Medium Priority')),
        ('high', _('High Priority')),
        ('very_high', _('Very High Priority')),
    ]
    
    user = models.ForeignKey(KurdishUser, on_delete=models.CASCADE, related_name='applications')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE, null=True, blank=True)
    
    # Application details
    application_title = models.CharField(max_length=300, verbose_name=_('Application Title'))
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, verbose_name=_('Application Status'), default='planning')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, verbose_name=_('Priority Level'), default='medium')
    
    # Important dates
    application_deadline = models.DateField(verbose_name=_('Application Deadline'), null=True, blank=True)
    submission_date = models.DateField(verbose_name=_('Submission Date'), null=True, blank=True)
    decision_date = models.DateField(verbose_name=_('Decision Date'), null=True, blank=True)
    
    # Contact information
    supervisor_name = models.CharField(max_length=200, verbose_name=_('Supervisor Name'), blank=True)
    supervisor_email = models.EmailField(verbose_name=_('Supervisor Email'), blank=True)
    admission_contact = models.CharField(max_length=200, verbose_name=_('Admission Contact'), blank=True)
    admission_email = models.EmailField(verbose_name=_('Admission Email'), blank=True)
    
    # Application specifics
    research_area = models.CharField(max_length=300, verbose_name=_('Research Area'), blank=True)
    funding_status = models.CharField(max_length=200, verbose_name=_('Funding Status'), blank=True)
    application_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Application Fee'), null=True, blank=True)
    
    # Notes and tracking
    notes = models.TextField(verbose_name=_('Notes'), blank=True)
    progress_notes = models.TextField(verbose_name=_('Progress Notes'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.application_title} - {self.university.name}"
    
    class Meta:
        verbose_name = _('Application Tracker')
        verbose_name_plural = _('Application Trackers')
        ordering = ['-priority', 'application_deadline']


class ApplicationDocument(models.Model):
    """
    Model for documents related to applications
    """
    DOCUMENT_TYPES = [
        ('cv', _('CV/Resume')),
        ('cover_letter', _('Cover Letter')),
        ('motivation_letter', _('Motivation Letter')),
        ('research_proposal', _('Research Proposal')),
        ('transcript', _('Academic Transcript')),
        ('diploma', _('Diploma/Certificate')),
        ('recommendation', _('Recommendation Letter')),
        ('language_certificate', _('Language Certificate')),
        ('passport', _('Passport Copy')),
        ('portfolio', _('Portfolio')),
        ('writing_sample', _('Writing Sample')),
        ('test_scores', _('Test Scores')),
        ('other', _('Other Document')),
    ]
    
    DOCUMENT_STATUS = [
        ('draft', _('Draft')),
        ('ready', _('Ready')),
        ('submitted', _('Submitted')),
        ('needs_update', _('Needs Update')),
    ]
    
    application = models.ForeignKey(ApplicationTracker, on_delete=models.CASCADE, related_name='documents')
    
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES, verbose_name=_('Document Type'))
    title = models.CharField(max_length=200, verbose_name=_('Document Title'))
    file = models.FileField(upload_to='application_documents/', verbose_name=_('Document File'), blank=True)
    
    status = models.CharField(max_length=15, choices=DOCUMENT_STATUS, verbose_name=_('Status'), default='draft')
    version = models.IntegerField(default=1, verbose_name=_('Version'))
    
    # Metadata
    description = models.TextField(verbose_name=_('Description'), blank=True)
    deadline = models.DateField(verbose_name=_('Deadline'), null=True, blank=True)
    is_required = models.BooleanField(default=True, verbose_name=_('Required Document'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"
    
    class Meta:
        verbose_name = _('Application Document')
        verbose_name_plural = _('Application Documents')


class EmailLog(models.Model):
    """
    Model for logging sent emails and communication history
    """
    EMAIL_TYPES = [
        ('inquiry', _('Initial Inquiry')),
        ('follow_up', _('Follow-up')),
        ('application', _('Application Related')),
        ('interview', _('Interview Related')),
        ('acceptance', _('Acceptance Related')),
        ('visa', _('Visa Related')),
        ('other', _('Other')),
    ]
    
    user = models.ForeignKey(KurdishUser, on_delete=models.CASCADE, related_name='email_logs')
    application = models.ForeignKey(ApplicationTracker, on_delete=models.CASCADE, related_name='email_logs', null=True, blank=True)
    
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES, verbose_name=_('Email Type'))
    template_used = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Email details
    recipient_email = models.EmailField(verbose_name=_('Recipient Email'))
    recipient_name = models.CharField(max_length=200, verbose_name=_('Recipient Name'), blank=True)
    subject = models.CharField(max_length=300, verbose_name=_('Subject'))
    body = models.TextField(verbose_name=_('Email Body'))
    
    # Tracking
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Sent Date'))
    response_received = models.BooleanField(default=False, verbose_name=_('Response Received'))
    response_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Response Date'))
    
    notes = models.TextField(verbose_name=_('Notes'), blank=True)
    
    def __str__(self):
        return f"Email to {self.recipient_email} - {self.subject[:50]}"
    
    class Meta:
        verbose_name = _('Email Log')
        verbose_name_plural = _('Email Logs')
        ordering = ['-sent_date']


class CommunicationTip(models.Model):
    """
    Model for communication tips and cultural guidance
    """
    COMMUNICATION_CONTEXTS = [
        ('email', _('Email Communication')),
        ('interview', _('Interview')),
        ('meeting', _('Meeting/Presentation')),
        ('phone', _('Phone Call')),
        ('networking', _('Networking Event')),
        ('application', _('Application Process')),
        ('visa', _('Visa Interview')),
        ('general', _('General Communication')),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Tip Title'))
    context = models.CharField(max_length=20, choices=COMMUNICATION_CONTEXTS, verbose_name=_('Communication Context'))
    country = models.CharField(max_length=100, verbose_name=_('Country/Region'), blank=True)
    
    content = models.TextField(verbose_name=_('Tip Content'))
    example = models.TextField(verbose_name=_('Example'), blank=True)
    
    # Kurdish-specific considerations
    kurdish_context = models.TextField(verbose_name=_('Kurdish Context Notes'), blank=True)
    common_mistakes = models.TextField(verbose_name=_('Common Mistakes to Avoid'), blank=True)
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    priority = models.IntegerField(default=1, verbose_name=_('Display Priority'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_context_display()})"
    
    class Meta:
        verbose_name = _('Communication Tip')
        verbose_name_plural = _('Communication Tips')
        ordering = ['-priority', 'title']