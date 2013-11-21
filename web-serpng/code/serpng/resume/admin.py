from resume.models import Resume 
from resume.models import Address 
from resume.models import Contact 
from resume.models import Job 
from resume.models import Education 
from resume.models import Skill 
from resume.models import Publication 
from resume.models import Award 
from resume.models import Summary
from django.contrib import admin




#class AddressInline (admin.StackedInline):
#    model = Address
    
class AddressInline (admin.StackedInline):
    model = Address    

class ContactInline (admin.StackedInline):
    model = Contact

class ContactAddressAdmin(admin.ModelAdmin):
    model = Address
    fieldsets = [
    (None, {'fields':['street']}),
    (None, {'fields':['street2']}),
    (None, {'fields':['city']}),
    (None, {'fields':['state']}),
    (None, {'fields':['postcode']}),
    (None, {'fields':['country']}),
]
    inlines = [ContactInline]

    


class SummaryInline (admin.StackedInline):
    model = Summary
    extra = 1
class ContactAdmin (admin.ModelAdmin):
    fieldsets = [
    (None, {'fields':['first_name']}),
    (None, {'fields':['last_name']}),
    (None, {'fields':['middle_name']}),
    (None, {'fields':['work_phone']}),
    (None, {'fields':['home_phone']}),
    (None, {'fields':['cell_phone']}),
    (None, {'fields':['email']}),
    (None, {'fields':['resume']}),

    ]
    inlines = [AddressInline]
    

class JobInline(admin.StackedInline):
    model = Job
    extra = 1
    
class JobAdmin (admin.ModelAdmin):
    inlines = [AddressInline]
    
class EducationInline(admin.StackedInline):
    model = Education
    extra = 0
    
class EducationAdmin (admin.ModelAdmin):
    inlines = [EducationInline]
    
class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1
class AwardInline(admin.StackedInline):
    model = Award
    extra = 0
    
class PublicationInline(admin.StackedInline):
    model = Publication 
    extra = 0

class ResumeAdmin(admin.ModelAdmin): 
    fieldsets = [
    (None, {'fields':['user']}),
    (None, {'fields':['add_date_time']}),
    ]
    
    inlines = [ContactInline, SummaryInline, JobInline, EducationInline, SkillInline, AwardInline, PublicationInline]  

admin.site.register(Resume, ResumeAdmin)
admin.site.register(Address)
admin.site.register(Job)
admin.site.register(Education)








#admin.site.register(Address)
#admin.site.register(Contact)
#admin.site.register(Job)
#admin.site.register(Education)
#admin.site.register(Skill)
#admin.site.register(Publication)
#admin.site.register(Award)
#admin.site.register(Summary)



