from resume.services.converters.resume_converter import ResumeConverter

"""
Import resume that was constructed by builder forms into the system.
The resume models will have already been saved to the database so to_model does nothing
"""
class BuilderConverter(ResumeConverter):
    
    """
    Does nothing.
    The resume models will have already been saved to the database.
    """
    def to_model(self, target_resume):
        return
    
