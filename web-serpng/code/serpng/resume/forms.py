from django import forms
from django.forms import ModelForm
import models
from django.forms.models import inlineformset_factory
from django_localflavor_us.forms import USStateField
from django_localflavor_us.us_states import STATE_CHOICES
import datetime
from django.core.validators import validate_email
from widgets import MonthYearWidget # Custom widget.

EDUCATION_FORM_START_YEAR = 1940
JOB_FORM_START_YEAR = 1940
# Add a blank choice, otherwise empty locations default to Alabama.
STATE_CHOICES = (('', '',),) + STATE_CHOICES

this_year = datetime.datetime.now().year
# Add blank years.
JOB_YEARS = [''] + range(JOB_FORM_START_YEAR, this_year+1)[::-1]
EDUCATION_YEARS = [''] + range(EDUCATION_FORM_START_YEAR, this_year+1)[::-1]


class UploadForm(forms.Form):
    #resume_file_name = forms.CharField(max_length=512,min_length=1)
    resume_file = forms.FileField()
    

class ResumeForm(ModelForm):

    class Meta:

        model = models.Resume
        fields = ('employer_opt_in',)

    employer_opt_in = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox inline'}), label='Share resume with employers', required=False)
    
class ContactForm(ModelForm):
    class Meta:
        model = models.Contact
        exclude = ('address')
    error_css_class = 'error'
           
    first_name = forms.CharField(widget=forms.TextInput(attrs={'size':'31', 'placeholder': 'First', 'class': 'input-small'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'size':'31', 'placeholder': 'Middle', 'class': 'input-mini'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'size':'103', 'placeholder': 'Last', 'class': 'input-small'}))
    work_phone = forms.CharField(widget=forms.TextInput(attrs={'size':'31'}), required=False)
    home_phone = forms.CharField(widget=forms.TextInput(attrs={'maxlength':'14', 'placeholder': 'Home', 'class': 'input-medium'}), required=False)
    cell_phone = forms.CharField(widget=forms.TextInput(attrs={'maxlength':'14', 'placeholder': 'Mobile', 'class': 'input-medium'}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'size':'31'}), validators=[validate_email], error_messages={'invalid': 'Please enter a valid email.'})
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False)
    
    
class AddressForm(ModelForm):
    
    class Meta:
        model = models.Address  
    error_css_class = 'error'
    
    street = forms.CharField(widget=forms.TextInput(attrs={'size':'103', 'placeholder': 'Address Line 1'}), required=False)
    street2 = forms.CharField(widget=forms.TextInput(attrs={'size':'103', 'placeholder': 'Address Line 2'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'size':'31', 'placeholder': 'City'}), required=False)
    postcode = forms.CharField(widget=forms.TextInput(attrs={'size':'5', 'class': 'input-mini', 'placeholder': 'Zipcode'}), label='Zipcode', required=False)
    country = forms.CharField(widget=forms.HiddenInput(attrs={'size':'31', 'class': 'input-mini'}), required=False)
    state = USStateField(widget=forms.Select(choices=STATE_CHOICES), required=False)
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False) # Is this needed?
 
class SummaryForm(ModelForm):
    class Meta:
        model = models.Summary
        exclude = ('resume',)
    error_css_class = 'error'
    
    headline = forms.CharField(widget=forms.TextInput(attrs={'size':'103', 'placeholder': 'Short sentence describing who you are', 'class': 'input-xlarge'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'style': 'display:block', 'placeholder': 'Brief summary of your work experience and objective', 'class': 'input-xxlarge', 'maxlength': '4096'}), required=False)
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False)


class JobForm(ModelForm):
    class Meta:
        model = models.Job
        exclude = ('resume', 'position', 'naics_code', 'address', )
    error_css_class = 'error'

    title = forms.CharField(widget=forms.TextInput(attrs={'size':'103'}), required=False)
    employer = forms.CharField(widget=forms.TextInput(attrs={'size':'103'}), label='Company', required=False)
    start_date = forms.DateField(widget=MonthYearWidget(attrs={'class': 'span1'}, years=JOB_YEARS), label='Duration', required=False)
    end_date = forms.DateField(widget=MonthYearWidget(attrs={'class': 'span1'}, years=JOB_YEARS), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input-xxlarge'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'size':'31', 'placeholder': 'City'}), label='Location', required=False)
    state = USStateField(widget=forms.Select(choices=STATE_CHOICES, attrs={'placeholder': 'State'}), required=False)
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False)
    current = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox inline'}), label='I still work here', required=False)

JobFormSet = inlineformset_factory(models.Resume, models.Job, form = JobForm, extra=0, can_delete=True)
    
    
class EducationForm(ModelForm):
    class Meta:
        model = models.Education
        exclude = ('resume', 'address', 'position')
    error_css_class = 'error'

    degree = forms.CharField(widget=forms.TextInput(attrs={'size':'103'}), required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={'size':'103'}), required=False)
    start_date = forms.DateField(widget=MonthYearWidget(attrs={'class': 'span1'}, years=EDUCATION_YEARS), label='Duration', required=False)
    end_date = forms.DateField(widget=MonthYearWidget(attrs={'class': 'span1'}, years=EDUCATION_YEARS), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'size':'31'}), required=False)
    state = USStateField(widget=forms.Select(choices=STATE_CHOICES), required=False)
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False)
    current = forms.BooleanField(widget=forms.CheckboxInput(), label='Ongoing', required=False)

EducationFormSet = inlineformset_factory(models.Resume, models.Education, form = EducationForm, extra=0, can_delete=True)


class PublicationForm(ModelForm):
    class Meta:
        model = models.Publication
        exclude = ('resume',' position')
    error_css_class = 'error'
    description = forms.CharField(widget=forms.TextInput(attrs={'size':'103', 'class':'award'}), label="Publication", required=False)
    position = forms.IntegerField(widget=forms.HiddenInput, initial=0, required=False)
    
PublicationFormSet = inlineformset_factory(models.Resume, models.Publication, form=PublicationForm, extra=1, exclude=('position'))


"""
#TODO: Does BurningGlass parse certifications?
class CertificationsForm(ModelForm):
    class Meta:
        model = models.Certifications
        exclude = ('resume',)
    error_css_class = 'error'
    description = forms.CharField()
    position = forms.IntegerField(widget=forms.HiddenInput, initial=0)

CertificationsFormSet = formset_factory(CertificationsForm, extra=0)
"""


class SkillForm(ModelForm):
    class Meta:
        model = models.Skill
        exclude = ('resume',)
        
    error_css_class = 'error'

    description = forms.CharField(widget=forms.Textarea(attrs={'class':'input-xxlarge', 'maxlength': '2048'}), label="Skills", required=False)
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False)


#Maps to Burning Glass Honors    
class AwardForm(ModelForm):
    class Meta:
        model = models.Award
        exclude = ('resume','position')
        
    error_css_class = 'error'
    description = forms.CharField(widget=forms.TextInput(attrs={'size':'103', 'class':'award'}), label="Award", required=False)
    position = forms.IntegerField(widget=forms.HiddenInput, initial=0, required=False)
    
AwardFormSet = inlineformset_factory(models.Resume, models.Award, form=AwardForm, extra=1, exclude=('position'))


class AdditionalInformationForm(ModelForm):
    class Meta:
        model = models.AdditionalInformation
        exclude = ('resume',)

    error_css_class = 'error'

    description = forms.CharField(widget=forms.Textarea(attrs={'class':'input-xxlarge', 'maxlength': '4096'}), label="Additional Information", required=False)
    cancel_form = forms.BooleanField(widget=forms.HiddenInput(attrs={'id': 'cancel'}), required=False)
