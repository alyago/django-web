# -*- coding: utf-8 -*-
import resume.models as models
import datetime
import xml.etree.cElementTree as xml
from resume.services.converters.resume_converter import ResumeConverter
from resume.exceptions.resume_parse_error import ResumeParseError
import logging
logger = logging.getLogger('resume')
import time

"""
Parse Resume into models
"""
class BurningGlassConverter(ResumeConverter):
    
    resume_xml_string = ''
    file_name = ''
    resume_bytes = None
    

    def __init__(self, burning_glass_connection, resume_file):
        
        from django.conf import settings
        
        resume_bytes = resume_file.read()            
        if ( len(resume_bytes)  > settings.MAX_RESUME_FILE_SIZE_MB * 1024 * 1024):
            raise ValueError("The resume file: " +  resume_file.name + " is too large, It must be less than " + str(settings.MAX_RESUME_FILE_SIZE_MB) + "MB.") 

        self.resume_bytes = resume_bytes
        self.file_name = resume_file.name
        
        time_start = time.time()
        self.resume_xml_string =  burning_glass_connection.get_tagged_resume_string(resume_bytes) 
        logger.debug("Burning Glass Tagging time for file %s is %s" % (self.file_name, str(time.time() - time_start)))
          
    def to_parsed_string(self):
        return self.resume_xml_string

    def to_raw_string(self):
        return self.resume_bytes
        
    def get_file_name(self):
        return self.file_name
                  
    """    
    Implementation of abstract method.

    Parser destination_resume_xml_string into destination_resume object. 
    """
    def to_model(self, destination_resume):    
        try: 
            res_doc_element = xml.fromstring(self.resume_xml_string)   
        except:
            raise ResumeParseError("Can not parse Burning Glass Response as xml, filename %s, contents %s"  % (self.file_name, self.resume_xml_string[:256]))
            
        resume_element = res_doc_element.find("resume")    
        if (resume_element == None):
            return 
        
        #TODO: Optimize using bulk inserts??
        
        contact_element = resume_element.find("contact")
        if contact_element != None:
            contact = BurningGlassConverter.create_contact_from_xml(contact_element) 
            contact.save()
            destination_resume.contact = contact             
     
        # If summary/summary does not exist, use summary/objective for summary
        summary_element = resume_element.find("summary")
        if summary_element != None:
            summary = None
            if summary_element.find("summary") != None and summary_element.find("summary").text != None:
                summary = models.Summary(description = BurningGlassConverter.replace_bullets(summary_element.find("summary").text))      
            elif summary_element.find("objective") != None and summary_element.find("objective").text != None:
                summary = models.Summary(description = summary_element.find("objective").text)
            if summary != None:
                summary.save()
                destination_resume.summary = summary          
                     
        experience_element = resume_element.find("experience")      
        if experience_element != None: 
            for job_element in experience_element.findall("job"):             
                job = BurningGlassConverter.create_job_from_xml(job_element)       
                destination_resume.job_set.add(job)
                
        education_element = resume_element.find("education")      
        if education_element != None:            
            for school_element in education_element.findall("school"):   
                school = BurningGlassConverter.create_education_from_xml(school_element)             
                destination_resume.education_set.add(school)
        
        #for honors_element in resume_element.findall(".//honors"):
        #    if honors_element.text != None:
        #        destination_resume.award_set.create(description = honors_element.text)
        
        for publications_element in resume_element.findall(".//publications"):
            if publications_element.text != None:
                destination_resume.publication_set.create(description = publications_element.text[:1024])

        #TODO: Narrow these skills? Use 'skills' section for resumes that have one?
        skill_rollup_element = res_doc_element.find("skillrollup")
        skill_list = []
        for skill_element in skill_rollup_element.findall("canonskill"):
            if skill_element.get('name') != None:
                skill_list.append(skill_element.get('name'))       
        if len(skill_list) > 0:
            skills = models.Skill()
            skills.description = ', '.join(skill_list)
            skills.save()
            destination_resume.skill = skills
             
    """
    """
    @staticmethod
    def create_job_from_xml(job_element): 
        job = models.Job()
        if job_element.find("employer") != None:
            job.employer = job_element.find("employer").text
        if job_element.find("title") != None:
            job.title = job_element.find("title").text
        if job_element.find("description") != None:
            job.description = BurningGlassConverter.replace_bullets(job_element.find("description").text)
        if job_element.find("daterange") != None and job_element.find("daterange/start") != None and job_element.find("daterange/end") != None:
            #date formatting, present for today?
            job.start_date = job_element.find("daterange/start").get("iso8601")
            if job.start_date:
                if job.start_date.endswith('-01-01'):
                    if job_element.find("daterange/start").text and ('jan' not in job_element.find("daterange/start").text.lower() or
                                                                     '01' not in job_element.find("daterange/start").text.lower()):
                        job.start_date = job.start_date.split('-')[0] + '-01-02'
                if job_element.find('daterange/end').text:
                    if 'present' in job_element.find('daterange/end').text.lower() or 'current' in job_element.find('daterange/end').text.lower():
                        job.current = True
                job.end_date = job_element.find("daterange/end").get("iso8601")  
                if job.end_date: 
                    if job.end_date.endswith('-01-01'):
                        if job_element.find("daterange/end").text and ('jan' not in job_element.find("daterange/end").text.lower() or
                                                                       '01' not in job_element.find("daterange/end").text.lower()):
                            job.end_date = job.end_date.split('-')[0] + '-01-02'
                else:
                    # No explicit end date. Set the end date to that year.
                    job.end_date = job.start_date.split('-')[0] + '-01-02'

        if job_element.find("address") != None:    
            address = BurningGlassConverter.create_address_from_xml(job_element.findall("address"))
            job.city = address.city
            job.state = address.state
            job.country = address.country
            
        return job      
         
         
    """
    """
    @staticmethod
    def create_contact_from_xml(contact_element): 
        contact = models.Contact()
        given_name_elements = contact_element.findall("name/givenname") 
        if given_name_elements and len(given_name_elements) > 0:
            contact.first_name = given_name_elements[0].text
            if len(given_name_elements) > 1:
                contact.middle_name = given_name_elements[1].text
        if contact_element.find("name/surname") != None:
            contact.last_name = contact_element.find("name/surname").text
        #@todo: how to get mulitple phone numbers?
        if contact_element.find("phone") != None:
            contact.cell_phone = contact_element.find("phone").text[:20] # Automatically truncate strings?
        if contact_element.find("email") != None:
            contact.email = contact_element.find("email").text       
        if contact_element.find("address") != None:    
            address_elements = contact_element.findall("address")
            address = BurningGlassConverter.create_address_from_xml(address_elements)
            address.save()
            contact.address = address
            
        return contact   
    
    
    """
    """
    @staticmethod
    def create_education_from_xml(school_element): 
        school = models.Education()
        if school_element.find("institution") != None:
            school.institution = school_element.find("institution").text
        if school_element.find("degree") != None:
            school.degree = school_element.find("degree").text
            if school_element.find("major") != None and school_element.find("major").text != None:
                school.degree = school.degree + ', ' + school_element.find("major").text
       
        end_date_text = None
        start_date_text = None
        if school_element.find("daterange") != None and school_element.find("daterange/start") != None and school_element.find("daterange/end") != None:
            school.start_date = school_element.find("daterange/start").get("iso8601")
            school.end_date = school_element.find("daterange/end").get("iso8601")
            start_date_text = school_element.find("daterange/start").text      
            end_date_text = school_element.find("daterange/end").text
            if end_date_text and ('present' in end_date_text.lower() or 'current' in end_date_text.lower()):
                school.current = True                                       
        elif school_element.find('completiondate') != None:
            school.end_date = school_element.find('completiondate').get('iso8601')
           
        #Hack for year only dates, use YYYY-01-02 to denote year only date
        if school.start_date and school.start_date.endswith('-01-01') and (not start_date_text or ('jan' not in start_date_text.lower())):
            school.start_date = school.start_date.split('-')[0] + '-01-02'    
        if school.end_date and school.end_date.endswith('-01-01') and (not end_date_text or ('jan' not in end_date_text.lower())): 
            school.end_date = school.end_date.split('-')[0] + '-01-02'
            
        if school_element.find("address") != None:    
            address = BurningGlassConverter.create_address_from_xml(school_element.findall("address"))
            school.city = address.city
            school.state = address.state
            school.country = address.country
            
        return school
    
    
    """
    A burning glass document can have multiple addresses
    """
    @staticmethod
    def create_address_from_xml(address_elements): 
        address = models.Address()
        for address_element in address_elements:
            if address_element.find("street") != None:
                address.street = address_element.find("street").text
            if address_element.find("city") != None:
                address.city = address_element.find("city").text
            if address_element.find("state") != None:
                address.state = address_element.find("state").get('abbrev') or address_element.find("state").text
            if address_element.find("country") != None:
                address.country = address_element.find("country").text
            if address_element.find("postalcode") != None:
                address.postcode = address_element.find("postalcode").text
                
        return address   
    
    
    @staticmethod    
    def get_experience_duration_years(experience_element):                
        experience_days = 0
 
        for job_element in experience_element.findall("job"): 
            if job_element.find("daterange") != None:   
                start_date_string = job_element.find("daterange/start").get("iso8601")
                end_date_string = job_element.find("daterange/end").get("iso8601")    
                if (start_date_string != None and end_date_string != None):              
                    # Date format is 'yyyy-mm-dd'
                    year,month,day = start_date_string.split('-')   
                    start_date =  datetime.date(int(year),int(month),int(day))
                    year,month,day = end_date_string.split('-')   
                    end_date =  datetime.date(int(year),int(month),int(day))
                    experience_days += (end_date - start_date).days
                
        return (experience_days + 1)  / 365 

    @staticmethod
    def replace_bullets(text):
        return text.replace(u'Â', '')


        
