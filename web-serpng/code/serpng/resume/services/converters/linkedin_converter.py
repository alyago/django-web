from datetime import date
import resume.models as models
import xml.etree.ElementTree as xml
from resume.services.converters.resume_converter import ResumeConverter
                  
class LinkedInConverter(ResumeConverter):
    
    resume_xml_string = ''
    
    def __init__(self, linkedin_connection):
        self.resume_xml_string = linkedin_connection.get_profile_string()
        
        
    def to_parsed_string(self):
        return self.resume_xml_string
   
   
    def to_model(self, destination_resume):     
        person_element = xml.fromstring(self.resume_xml_string)    
        if (person_element == None):
            return
        
        location_element = person_element.find("location")
        if location_element != None:  
            address = LinkedInConverter.create_address_from_xml(location_element)
            address.save()        
        
        contact = LinkedInConverter.create_contact_from_xml(person_element) 
        contact.address = address
        contact.save()   
        destination_resume.contact = contact 
            
        experience_element = person_element.find("positions")     
        if experience_element != None: 
            for job_element in experience_element.findall("position"):             
                job = LinkedInConverter.create_job_from_xml(job_element)       
                destination_resume.job_set.add(job)
                
        education_element = person_element.find("educations")      
        if education_element != None:            
            for school_element in education_element.findall("education"):   
                school = LinkedInConverter.create_education_from_xml(school_element)  
                destination_resume.education_set.add(school)            
                
        summary = models.Summary()
        if person_element.find("summary") != None:
            summary.description = person_element.find("summary").text
        if person_element.find("headline") != None:
            summary.headline = person_element.find("headline").text
        summary.save()
        destination_resume.summary = summary      
           
        if person_element.find("specialties") != None:        
            if  person_element.find("specialties").text != None and  person_element.find("specialties").text != "":
                skill = models.Skill()
                skill.description = person_element.find("specialties").text
                skill.save()
                destination_resume.skill = skill 
                        
            
    @staticmethod
    def create_job_from_xml(job_element): 
        job = models.Job()
        if job_element.find("company/name") != None and job_element.find("company/name").text != None:
            job.employer = job_element.find("company/name").text
        if job_element.find("title") != None and job_element.find("title").text != None:
            job.title = job_element.find("title").text
        if job_element.find("summary") != None and  job_element.find("summary").text != None:
            job.description = job_element.find("summary").text
        if job_element.find("start-date") != None:
            if job_element.find("start-date/year") != None and job_element.find("start-date/year").text != None:
                job.start_date = date(int(job_element.find("start-date/year").text),1,2).isoformat()
                if job_element.find("start-date/month") != None:
                    job.start_date = date(int(job_element.find("start-date/year").text),int(job_element.find("start-date/month").text),1).isoformat()
                #default end date
                job.end_date = date.today()                   
        if job_element.find("end-date") != None:
            if job_element.find("end-date/year") != None and job_element.find("end-date/year").text != None:
                job.end_date = date(int(job_element.find("end-date/year").text),1,2).isoformat()
                if job_element.find("end-date/month") != None:
                    job.end_date = date(int(job_element.find("end-date/year").text),int(job_element.find("end-date/month").text),1).isoformat()
        if job_element.find("is-current") != None and job_element.find("is-current").text != None:
            job.current = 1 if (job_element.find("is-current").text.lower() == 'true') else 0 
            
        return job        
    
    
    @staticmethod
    def create_contact_from_xml(contact_element): 
        contact = models.Contact()
        if contact_element.find("first-name") != None:
            contact.first_name = contact_element.find("first-name").text
        if contact_element.find("last-name") != None:
            contact.last_name = contact_element.find("last-name").text
        #@todo: how to get mulitple phone numbers?
        if contact_element.find("phone") != None:
            contact.cell_phone = contact_element.find("phone").text[:20] # Automatically truncate strings?
        if contact_element.find("email") != None:
            contact.email = contact_element.find("email").text       
            
        return contact
    
    
    @staticmethod
    def create_education_from_xml(school_element): 
        school = models.Education()
        if school_element.find("school-name") is not None:
            school.institution = school_element.find("school-name").text
        if school_element.find("degree") is not None and school_element.find('degree').text:
            school.degree = school_element.find("degree").text
            if school_element.find("field-of-study") != None and school_element.find("field-of-study").text:
                school.degree = school.degree + ', ' + school_element.find("field-of-study").text
        
        if school_element.find("start-date") != None:
            if school_element.find("start-date/month") != None:
                school.start_date = date(int(school_element.find("start-date/year").text),int(school_element.find("start-date/month").text),1).isoformat()
            else: 
                school.start_date = date(int(school_element.find("start-date/year").text),1,2).isoformat()
        
        if school_element.find("end-date") != None:
            if school_element.find("end-date/month") != None:
                school.end_date = date(int(school_element.find("end-date/year").text),int(school_element.find("end-date/month").text),1).isoformat()
            else:
                school.end_date = date(int(school_element.find("end-date/year").text),1,2).isoformat()

        return school


    @staticmethod
    def create_address_from_xml(location_element): 
        address = models.Address()
        if location_element.find("country/code") != None:
            address.country = location_element.find("country/code").text
        if location_element.find("name") != None:
            address.city = location_element.find("name").text
        if location_element.find("postal-code") != None:
            address.postcode = location_element.find("postal-code").text
            
        return address 
    
    
    @staticmethod
    def get_experience_duration_years(experience_element):            
        experience_days = 0
    
        for position_element in experience_element.findall("position"): 
            end_date = date.today()
            if position_element.find("end-date") != None and position_element.find("end-date/year") != None:
                month = 1 
                year = int(position_element.find("end-date/year").text)
                if position_element.find("end-date/month") != None:
                    month = int(experience_element.find("position/end-date/month").text)
                end_date = date(year, month, 1)      
            if position_element.find("start-date") != None and position_element.find("start-date/year") != None:
                month = 1 
                year = int(position_element.find("start-date/year").text)
                if position_element.find("start-date/month") != None:
                    month = int(experience_element.find("position/start-date/month").text)
                start_date = date(year, month, 1)          
                experience_days += (end_date - start_date).days
        
        return (experience_days + 1)  / 365
