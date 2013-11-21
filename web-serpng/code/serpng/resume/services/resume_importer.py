import resume.models as models
from resume.services.converters.resume_converter_factory import ResumeConverterFactory
from resume.services.searcher import Searcher
from datetime import datetime
from django.db import transaction
import logging

logger = logging.getLogger('resume')


"""
Import resume to simply hired database
"""
class ResumeImporter(object):
    
    FILE_UPLOAD_IMPORT_SOURCE = 'File Upload'
    LINKEDIN_IMPORT_SOURCE = 'Linkedin'
    BUILD_FORM_SOURCE = 'Builder'
    
    import_source_to_resume_converter = {
        FILE_UPLOAD_IMPORT_SOURCE: ResumeConverterFactory.BURNINGGLASS_CONVERTER,
        LINKEDIN_IMPORT_SOURCE : ResumeConverterFactory.LINKEDIN_CONVERTER,
        BUILD_FORM_SOURCE : ResumeConverterFactory.BUILDER_CONVERTER
    }
    
    """
    Create resume without data, will not be saved to db.
    """
    @staticmethod
    def create_resume (request, user_id):
        
        existing_resume = None
        if user_id and user_id != 'null':
            existing_resume = models.get_or_none(models.Resume, user = user_id, is_active = 1)
        
        # There was a previous resume, deactivate the old  resume
        if existing_resume != None:
            existing_resume.is_active = 0
            existing_resume.save()
            
        new_resume = models.Resume(user = user_id, add_date_time = datetime.now())

        # If these fields are None, the user won't be able to save these fields.
        contact = models.Contact()
        contact.save()
        skill = models.Skill()
        skill.save()
        summary = models.Summary()
        summary.save()
        additional_info = models.AdditionalInformation()
        additional_info.save()
        content = models.Content()
        content.save()
        logger.info('Created content with Id: ' + str(content.id))

        new_resume.contact = contact
        new_resume.summary = summary
        new_resume.skill = skill
        new_resume.additional_info = additional_info
        new_resume.content = content

        logger.debug ('Created resume for user:' + str(user_id) + ' with resume Id: ' + str(new_resume.id))
        
        return new_resume
    
    """
    Create converter to convert imported resume from import source to SH DB models
    No DB operations should be performed here, but time-intensive operations should
    be performed in this non-transactional method if possible, eg. fetching data 
    in the Converter constructor from an external server.
    """
    @staticmethod
    def create_converter (request, import_source): 
        converter_type = ResumeImporter.import_source_to_resume_converter[import_source]
        resume_converter = ResumeConverterFactory.create(request, converter_type) 
        logger.debug ('Importing resume from source:' + import_source + '. Creating converter of type: ' + converter_type)
        return resume_converter
        
    """
    Import resume to simply hired database.
    If a resume and its dependent models have already been saved to the database, it will be passed in as 'existing_resume'
    
    All database activity should be performed here, in this transactional method
    """
    @staticmethod
    # CAUTION: We are using the default REPEATABLE READ transaction isolation level - subsequent reads will always return the same results

    @transaction.commit_on_success
    def import_resume (request, import_source, existing_resume = None, user_id=None):
        resume_converter = ResumeImporter.create_converter(request, import_source)             
        if not user_id:
            user_id = request.resume_user.user_id
        
        if (existing_resume == None):
            imported_resume = ResumeImporter.create_resume(request, user_id)
            imported_resume.save()
            logger.info('(1) Created new Resume with Id: ' + str(imported_resume.id))
            resume_converter.to_model(imported_resume)
        else:
            imported_resume = existing_resume
            logger.info('(1) Importing existing Resume with Id: ' + str(imported_resume.id))
        
        imported_resume.source = import_source
        imported_resume.search_query = Searcher.construct_search_query(imported_resume)        
        logger.debug ('Created search query: ' + imported_resume.search_query + ' for resume' + str(imported_resume.id))
        logger.info('(2) Created search query for Resume with Id: ' + str(imported_resume.id))

        imported_resume.content.raw_resume = resume_converter.to_raw_string().decode('latin-1').encode('utf-8')
        imported_resume.content.parsed_resume =  resume_converter.to_parsed_string()
        imported_resume.content.file_name = resume_converter.get_file_name()
        imported_resume.content.resume = imported_resume
        imported_resume.content.save()
        logger.info('(3) Saved Content for Resume with Id: ' + str(imported_resume.id) + ' Content id: ' + str(imported_resume.content.id))
        #logger.debug("Parsed resume from:" +  import_source + ": " + content.parsed_resume)    
        
        imported_resume.save()
        logger.info('(4) Saved Resume with Id: ' + str(imported_resume.id))

        return imported_resume
