from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Field
from crispy_forms.bootstrap import InlineRadios

from .models import KurdishUser, UserProfile, KurdishDialect


class KurdishUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Email'))
    kurdish_name = forms.CharField(max_length=100, required=False, label=_('Kurdish Name'))
    region = forms.ChoiceField(choices=KurdishUser.REGION_CHOICES, label=_('Kurdish Region'))
    field_of_study = forms.CharField(max_length=200, label=_('Field of Study'))
    current_education_level = forms.ChoiceField(
        choices=KurdishUser.EDUCATION_LEVEL_CHOICES, 
        label=_('Current Education Level')
    )
    preferred_study_level = forms.ChoiceField(
        choices=KurdishUser.EDUCATION_LEVEL_CHOICES, 
        label=_('Preferred Study Level')
    )
    
    class Meta:
        model = KurdishUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                 'kurdish_name', 'region', 'field_of_study', 'current_education_level', 
                 'preferred_study_level', 'phone_number', 'current_city', 'current_country')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make email required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Add form helper for crispy forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3">' + str(_('Basic Information')) + '</h4>'),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            Row(
                Column('kurdish_name', css_class='form-group col-md-6'),
                Column('username', css_class='form-group col-md-6'),
            ),
            'email',
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
            ),
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Regional & Academic Information')) + '</h4>'),
            Row(
                Column('region', css_class='form-group col-md-6'),
                Column('field_of_study', css_class='form-group col-md-6'),
            ),
            Row(
                Column('current_education_level', css_class='form-group col-md-6'),
                Column('preferred_study_level', css_class='form-group col-md-6'),
            ),
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Contact Information')) + '</h4>'),
            Row(
                Column('phone_number', css_class='form-group col-md-6'),
                Column('current_city', css_class='form-group col-md-6'),
            ),
            'current_country',
            
            Submit('submit', _('Create Account'), css_class='btn btn-primary btn-lg mt-4')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['biography', 'motivation_letter', 'gpa', 'academic_awards', 'publications',
                 'work_experience', 'volunteer_experience', 'technical_skills', 'language_skills',
                 'cv_document', 'transcripts', 'certificates']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4}),
            'motivation_letter': forms.Textarea(attrs={'rows': 6}),
            'academic_awards': forms.Textarea(attrs={'rows': 3}),
            'publications': forms.Textarea(attrs={'rows': 4}),
            'work_experience': forms.Textarea(attrs={'rows': 5}),
            'volunteer_experience': forms.Textarea(attrs={'rows': 3}),
            'technical_skills': forms.Textarea(attrs={'rows': 3}),
            'language_skills': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3">' + str(_('Personal Information')) + '</h4>'),
            'biography',
            'motivation_letter',
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Academic Information')) + '</h4>'),
            Row(
                Column('gpa', css_class='form-group col-md-4'),
                Column('academic_awards', css_class='form-group col-md-8'),
            ),
            'publications',
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Experience')) + '</h4>'),
            'work_experience',
            'volunteer_experience',
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Skills')) + '</h4>'),
            Row(
                Column('technical_skills', css_class='form-group col-md-6'),
                Column('language_skills', css_class='form-group col-md-6'),
            ),
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Documents')) + '</h4>'),
            Row(
                Column('cv_document', css_class='form-group col-md-4'),
                Column('transcripts', css_class='form-group col-md-4'),
                Column('certificates', css_class='form-group col-md-4'),
            ),
            
            Submit('submit', _('Update Profile'), css_class='btn btn-primary btn-lg mt-4')
        )


class KurdishUserUpdateForm(forms.ModelForm):
    class Meta:
        model = KurdishUser
        fields = ['first_name', 'last_name', 'kurdish_name', 'email', 'phone_number',
                 'current_city', 'current_country', 'region', 'field_of_study',
                 'current_education_level', 'preferred_study_level', 'research_interests']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4 class="mb-3">' + str(_('Basic Information')) + '</h4>'),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
            ),
            Row(
                Column('kurdish_name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Contact Information')) + '</h4>'),
            Row(
                Column('phone_number', css_class='form-group col-md-6'),
                Column('current_city', css_class='form-group col-md-6'),
            ),
            'current_country',
            
            HTML('<h4 class="mb-3 mt-4">' + str(_('Academic Information')) + '</h4>'),
            'region',
            Row(
                Column('field_of_study', css_class='form-group col-md-6'),
                Column('current_education_level', css_class='form-group col-md-6'),
            ),
            'preferred_study_level',
            'research_interests',
            
            Submit('submit', _('Update Information'), css_class='btn btn-primary btn-lg mt-4')
        )
