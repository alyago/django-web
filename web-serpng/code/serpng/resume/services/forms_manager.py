import logging

from django.db import transaction

import resume.models as models
import resume.cat_location as cat_location
from resume.forms import ContactForm, AddressForm, SummaryForm, SkillForm, JobFormSet, EducationFormSet, ResumeForm, AdditionalInformationForm
from resume import p13n

REQUIRED_FIELD_ERROR = 'This field is required'

class ResumeEditFormsManager(object):
    """
    Class to manage collection of forms on review and build page

    Forms and Formsets are created on construction. When handle_post() is called with the request,
    forms are populated and saved to the db based upon the submit input name.
    """

    def __init__(self, resume_instance):       
        if resume_instance == None:
            raise ValueError("resume instance can not be None")

        self.resume_instance = resume_instance
        self.has_errors = False

        self.resume_form = ResumeForm(instance=resume_instance)
        self.contact_form = ContactForm(instance = resume_instance.contact)    
        address_instance = None
        if resume_instance.contact and resume_instance.contact.address:
            address_instance = resume_instance.contact.address
        self.address_form = AddressForm(instance = address_instance)

        # These fields all have description columns, so assign prefixes.
        self.summary_form = SummaryForm(instance = resume_instance.summary, prefix='summary', label_suffix='')
        self.skill_form = SkillForm(instance=resume_instance.skill, prefix='skill', label_suffix='')
        if not hasattr(resume_instance, 'additional_info'):
            resume_instance.additional_info = None
        self.additional_info_form = AdditionalInformationForm(instance=resume_instance.additional_info, prefix='additional_info', label_suffix='')

        self.jobformset =  JobFormSet(instance=self.resume_instance, prefix='job')
        self.educationformset =  EducationFormSet(instance=self.resume_instance, prefix='education')

    def validate(self):
        # This case is if the contact form doesn't get parsed on upload.
        if self.contact_form.initial:
            if not self.contact_form.initial['email']:
                self.contact_form.errors['email'] = REQUIRED_FIELD_ERROR
            if not self.contact_form.initial['first_name']:
                self.contact_form.errors['first_name'] = REQUIRED_FIELD_ERROR
            if not self.contact_form.initial['last_name']:
                self.contact_form.errors['last_name'] = REQUIRED_FIELD_ERROR
        else:
            self.contact_form.errors['email'] = REQUIRED_FIELD_ERROR
            self.contact_form.errors['first_name'] = REQUIRED_FIELD_ERROR
            self.contact_form.errors['last_name'] = REQUIRED_FIELD_ERROR

        if self.jobformset.forms and not self.jobformset.forms[0].initial['title']:
            self.jobformset.forms[0].errors['title'] = REQUIRED_FIELD_ERROR

    # CAUTION: We are using the default REPEATABLE READ transaction isolation level - subsequent reads will always return the same results  
    @transaction.commit_on_success 
    def handle_post(self, form_data, user_id):
        if user_id and self.resume_instance.user != user_id:
            self.resume_instance.user = user_id

        # For existing users, create the row if it doesn't exist.
        # Otherwise it won't save any changes.
        if self.resume_instance.additional_info is None:
            additional_info = models.AdditionalInformation()
            additional_info.save()
            self.resume_instance.additional_info = additional_info

        if self.resume_instance.summary is None:
            summary = models.Summary()
            summary.save()
            self.resume_instance.summary = summary

        if self.resume_instance.skill is None:
            skill = models.Skill()
            skill.save()
            self.resume_instance.skill = skill

        address = None
        if self.resume_instance.contact != None:
            self.address_form = AddressForm(form_data, None, instance = self.resume_instance.contact.address)
            if self.address_form.is_valid() and not self.address_form.cleaned_data['cancel_form']:
                if self.address_form.has_changed():
                    location = cat_location.ZipsEnUs.objects.filter(zip_code=self.address_form.cleaned_data['postcode'], city_type='D')[:1]
                    if location:
                        location = location[0]
                        self.address_form.instance.city = location.city_name
                        self.address_form.instance.state = location.state_abbr
                    address = self.address_form.save()
            else:
                if any(self.address_form.errors):
                    self.has_errors = True

        self.contact_form = ContactForm(form_data, None, instance = self.resume_instance.contact)
        if self.contact_form.has_changed() and self.contact_form.is_valid():
            if not self.contact_form.cleaned_data['cancel_form']:
                # Note that the contact form doesn't have fields for city and state.
                contact = self.contact_form.save(commit = False)
                if address != None:
                    contact.address = address
                contact.save()
                if not self.resume_instance.contact:
                    self.resume_instance.contact = contact
        else:
            if any(self.contact_form.errors):
                self.has_errors = True

        self.summary_form = SummaryForm(form_data, None, instance = self.resume_instance.summary, prefix='summary', label_suffix='')
        if self.summary_form.has_changed() and self.summary_form.is_valid() and not self.summary_form.cleaned_data['cancel_form']:
            self.summary_form.save()
        else:
            if any(self.summary_form.errors):
                self.has_errors = True

        self.skill_form = SkillForm(form_data, None, instance=self.resume_instance.skill, prefix='skill', label_suffix='')
        if self.skill_form.has_changed() and self.skill_form.is_valid() and not self.skill_form.cleaned_data['cancel_form']:
            self.skill_form.save()
        else:
            if any(self.skill_form.errors):
                self.has_errors = True

        self.additional_info_form = AdditionalInformationForm(form_data, None, instance=self.resume_instance.additional_info, prefix='additional_info', label_suffix='')
        if not self.additional_info_form.is_valid() or any(self.additional_info_form.errors):
            self.has_errors = True
        elif self.additional_info_form.has_changed() and self.additional_info_form.is_valid() and not self.additional_info_form.cleaned_data['cancel_form']:
            self.additional_info_form.save()

        # We need to check to see if the latest job (the one we enforce a title for) isn't being deleted.
        self.jobformset = JobFormSet(form_data, None, instance=self.resume_instance, prefix='job')
        if self.jobformset.is_valid() and self.jobformset and len(self.jobformset.forms):
            for index, jobform in enumerate(self.jobformset.forms):
                if jobform in self.jobformset.deleted_forms:
                    continue

                if not 'title' in jobform.cleaned_data or not jobform.cleaned_data['title']:
                    self.jobformset.forms[index].errors['title'] = REQUIRED_FIELD_ERROR
                    self.has_errors = True
                    break

                # save job form set
                self.jobformset.save()

                # save p13n data
                try:
                    p13n.write_resume_job_title_data(user_id, self.jobformset)
                except Exception, e:
                    # todo: log error
                    logger = logging.getLogger('resume')
                    logger.exception("P13N Exception: %s" % e.message)

                break
        else:
            self.has_errors = True

        self.educationformset = EducationFormSet(form_data, None, instance=self.resume_instance, prefix='education')
        if (any([_.has_changed() for _ in self.educationformset.forms]) or self.educationformset.extra_forms) and self.educationformset.is_valid():
            self.educationformset.save()
        else:
            if any(self.educationformset.errors):
                self.has_errors = True

    def handle_employer_opt_in(self, form_data):
        self.resume_form = ResumeForm(form_data, None, instance=self.resume_instance)
        if self.resume_form.is_valid() and self.resume_form.has_changed():
            self.resume_form.save()
