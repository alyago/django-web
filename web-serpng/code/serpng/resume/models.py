import django.db.models.options as options
from django.db import models
from fields import BlobField

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

"""
Convenience function will return None as alternative to try/except
"""
def get_or_none(model, **kwargs):
    try:     
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    
"""
Get Resume, ignoring Resumes with NULL users - guest users
"""
def resume_get_or_none(**kwargs):
    #Don't return resumes for NULL users - guest users
    if 'user' in kwargs and not kwargs['user']:
        return None

    try:
        return get_or_none(Resume, **kwargs)
    except Resume.MultipleObjectsReturned:
        return Resume.objects.filter(**kwargs).order_by('-id')[:1][0]

"""
Get Resume, ignoring Resumes with NULL users - guest users
"""
def resume_get(**kwargs):
    #Don't return resumes for NULL users - guest users
    if 'user' in kwargs and not kwargs['user']:
        raise Resume.DoesNotExist
    return Resume.objects.get(**kwargs)
    
 
"""
Wrapper around select_related which will include associated tables needed for most operation:
     'summary', 'job', 'education', 'contact', 'contact__address' 
This query will exclude the 'content' table
"""
def resume_select_related(**kwargs):
    #prefetch_related() currently in development version will follow backward relations, eg. Job->Resume
    #Don't return resumes for NULL users - guest users
    if 'user' in kwargs and not kwargs['user']:
        raise Resume.DoesNotExist 
    return Resume.objects.select_related('summary', 'contact', 'contact__address', 'skill' ).get(**kwargs)

"""
Convenience function will return None as alternative to try/except
"""  
def resume_select_related_or_none(**kwargs):
    try:
        return resume_select_related(**kwargs)
    except Resume.DoesNotExist:
        return None
  
"""
This delete will cascade OneToOne relationships in the 'forward' direction
Django does not do this by default
"""
#TODO: Would removing the OneToOne relationships improve perf? Delete is not a common operation now
def resume_delete(resume_id):
    resume = resume_select_related(id=resume_id)
    
    if (resume.contact != None):
        if (resume.contact.address != None):
            resume.contact.address.delete()
        resume.contact.delete()
    if (resume.summary != None):
        resume.summary.delete()  
        
    resume.delete()       
         
# Generic Address - not resume specific
class Address(models.Model):
    street = models.CharField(blank=True, null=True, max_length=128, default = "")
    street2 = models.CharField(blank=True, null=True, max_length=128, default = "")
    city = models.CharField(blank=True, null=True, max_length=128, default = "")
    state = models.CharField(blank=True, null=True, max_length=128, default = "")
    postcode = models.CharField(blank=True, null=True, max_length=40, default = "")
    country = models.CharField(blank=True, null=True, max_length=128, default = "")
    #class Meta:
    #    verbose_name_plural = ('Addresses')
    class Meta:
        in_db = 'resume'

# one Contact -> one Resume
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(blank=True, null=True, max_length=255)  
    work_phone = models.CharField(blank=True, null=True, max_length=32)
    home_phone = models.CharField(blank=True, null=True, max_length=32)
    cell_phone = models.CharField(blank=True, null=True, max_length=32)
    email = models.CharField(blank=True, null=True, max_length=255)
    address = models.ForeignKey(Address, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    class Meta:
        in_db = 'resume'

# one Summary -> one Resume
class Summary(models.Model):
    headline = models.CharField(blank=True, null=True, max_length=1024)
    description = models.CharField(blank=True, null=True, max_length=4096)
    class Meta:
        in_db = 'resume'

#one Skill -> one Resume
class Skill(models.Model):
    description = models.CharField(blank=True, max_length=2048)
    class Meta:
        in_db = 'resume'

class AdditionalInformation(models.Model):
    description = models.CharField(blank=True, null=True, max_length=4096)
    class Meta:
        in_db = 'resume'

class Resume(models.Model):  
    add_date_time = models.DateTimeField()
    search_query = models.CharField(blank=True, null=True, max_length=2048)
    name = models.CharField(blank=True, null=True, max_length=255, default = "")
    source = models.CharField(blank=True, null=True, max_length=255, default = "")
    submitted = models.IntegerField(max_length = 1, default = 0)
    contact =  models.ForeignKey(Contact, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    summary = models.ForeignKey(Summary, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    skill = models.ForeignKey(Skill, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    additional_info = models.ForeignKey(AdditionalInformation, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    employer_opt_in = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    #User in Customer DB, UserMasterNew table
    user = models.IntegerField(blank=True, null=True, max_length=11) 
    class Meta:
        in_db = 'resume'

# Raw and parsed forms of resume, non-db representations
# one Content -> One Resume
class Content(models.Model): 
    raw_resume = BlobField(blank=True, null=True)
    file_name =  models.CharField(blank=True, null=True, max_length=512, default = "")
    parsed_resume = models.TextField(blank=True, null=True)
    pdf = BlobField(blank=True, null=True)
    resume = models.ForeignKey(Resume, blank=True, null=True, unique=True, on_delete=models.SET_NULL)
    class Meta:
        in_db = 'resume'
  
# many Job -> one Resume   
class Job(models.Model):
    title = models.CharField(blank=True, null=True, max_length=255)
    employer = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=128, default = "")
    state = models.CharField(blank=True, null=True, max_length=128, default = "")
    country = models.CharField(blank=True, null=True, max_length=128, default = "")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current =  models.BooleanField(blank=True)
    description = models.TextField(blank=True, null=True, max_length=4096)
    naics_code = models.IntegerField(blank=True, null=True, max_length=6)
    resume = models.ForeignKey(Resume)
    position = models.PositiveIntegerField(default=0)
    class Meta:
        # Sort jobs by end date here.
        # Fixes bug https://github.ksjc.sh.colo/apps-team/web-resumes/issues/75.
        ordering = ('-end_date',)
        in_db = 'resume'
    
# many Education -> one Resume    
class Education(models.Model):
    institution = models.CharField(blank=True, null=True, max_length=255)
    degree = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=128, default = "")
    state = models.CharField(blank=True, null=True, max_length=128, default = "")
    country = models.CharField(blank=True, null=True, max_length=128, default = "")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    current =  models.BooleanField(blank=True)
    resume = models.ForeignKey(Resume)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-end_date',)
        in_db = 'resume'
    
#many Publication -> one Resume  
#includes patents
#TODO: How does BurningGlass parse patents?
class Publication(models.Model):
    description = models.CharField(blank=True, max_length=1024)
    resume = models.ForeignKey(Resume)
    position = models.PositiveIntegerField(default=0)
    class Meta:
        in_db = 'resume'

#many Publication -> one Resume  
#TODO: How does BurningGlass parse certifications?
class Certifications(models.Model):
    description = models.CharField(blank=True, max_length=1024)
    resume = models.ForeignKey(Resume)
    position = models.PositiveIntegerField(default=0)
    class Meta:
        in_db = 'resume'

#many Award -> one Resume 
#Maps to Burning Glass Honors    
class Award(models.Model):
    description = models.CharField(blank=True, max_length=255)
    resume = models.ForeignKey(Resume)
    position = models.PositiveIntegerField(default=0)    
    class Meta:
        in_db = 'resume'

class ApplyTracking(models.Model):
    user_id = models.IntegerField(blank=True, null=True, max_length=11)
    user_email = models.CharField(blank=True, null=True, max_length=255)
    session = models.CharField(blank=True, null=True, max_length=50)
    apply_source = models.CharField(max_length=32)
    user_agent = models.CharField(max_length=255)
    resume_type = models.CharField(max_length=32)
    filename = models.CharField(blank=True, null=True, max_length=512, default='')
    advertiser_id = models.IntegerField(blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    refind_key = models.CharField(blank=True, null=True, max_length=40)
    job_title = models.CharField(blank=True, null=True, max_length=255)
    employer = models.CharField(blank=True, null=True, max_length=255)
    job_location = models.CharField(blank=True, null=True, max_length=255) # Zipcode.
    search_keyword = models.CharField(blank=True, null=True, max_length=255)
    search_location = models.CharField(blank=True, null=True, max_length=255)
    search_position = models.CharField(blank=True, null=True, max_length=20)
    cpc = models.CharField(blank=True, null=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    resume = models.ForeignKey(Resume, null=True)
    status = models.CharField(blank=True, null=True, max_length=32) # Mainly for self serve...
    class Meta:
        in_db = 'resume'

class OrganicSimplyApplySources(models.Model):
    robotid = models.IntegerField(blank=False, max_length=11)
    class Meta:
        in_db = 'resume'

#### BEGIN MOBOLT INTEGRATION ####

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class JobApplication(BaseModel):
    refind_key = models.CharField(max_length=40, primary_key=True)
    mobolt_id = models.CharField(max_length=10, unique=True)
    questions = models.CharField(max_length=10000)
    class Meta:
        in_db = 'resume'
        db_table = 'job_applications'

#### END MOBOLT INTEGRATION ####
