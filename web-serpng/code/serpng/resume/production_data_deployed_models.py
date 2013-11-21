# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

import django.db.models.options as options
from django.db import models

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

"""
class Deletedjobs(models.Model):
    job_id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765, blank=True)
    job_board_name = models.CharField(max_length=765, blank=True)
    company_name = models.CharField(max_length=765, blank=True)
    subsidiary_name = models.CharField(max_length=765, blank=True)
    division = models.CharField(max_length=765, blank=True)
    department = models.CharField(max_length=765, blank=True)
    category_or_function = models.CharField(max_length=765, blank=True)
    location_all = models.TextField(blank=True)
    location_address = models.CharField(max_length=765, blank=True)
    location_city = models.CharField(max_length=765, blank=True)
    location_state = models.CharField(max_length=765, blank=True)
    location_zip = models.CharField(max_length=765, blank=True)
    location_country = models.CharField(max_length=765, blank=True)
    description_all = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    skills_required = models.TextField(blank=True)
    skills_preferred = models.TextField(blank=True)
    company_description = models.TextField(blank=True)
    experience_level_required = models.CharField(max_length=765, blank=True)
    education_level_required = models.CharField(max_length=765, blank=True)
    employment_type_all = models.TextField(blank=True)
    employment_term = models.CharField(max_length=765, blank=True)
    employment_hours = models.CharField(max_length=765, blank=True)
    shifts = models.CharField(max_length=765, blank=True)
    manages_others = models.CharField(max_length=765, blank=True)
    travel_required = models.CharField(max_length=765, blank=True)
    telecommute = models.CharField(max_length=765, blank=True)
    contact_info_all = models.TextField(blank=True)
    contact_name = models.CharField(max_length=765, blank=True)
    contact_email = models.CharField(max_length=765, blank=True)
    contact_phone_number = models.CharField(max_length=765, blank=True)
    contact_fax = models.CharField(max_length=765, blank=True)
    contact_address = models.CharField(max_length=765, blank=True)
    date_posted = models.CharField(max_length=765, blank=True)
    date_posted_norm = models.IntegerField(null=True, blank=True)
    date_posted_timestamp = models.IntegerField(null=True, blank=True)
    date_updated = models.CharField(max_length=765, blank=True)
    closing_date = models.CharField(max_length=765, blank=True)
    compensation_all = models.TextField(blank=True)
    compensation_pay = models.CharField(max_length=765, blank=True)
    compensation_other = models.CharField(max_length=765, blank=True)
    benefits_text = models.TextField(blank=True)
    security_clearance = models.CharField(max_length=765, blank=True)
    keywords = models.CharField(max_length=765, blank=True)
    number_of_positions = models.CharField(max_length=765, blank=True)
    job_board_url = models.TextField(blank=True)
    company_url = models.TextField(blank=True)
    apply_url = models.TextField(blank=True)
    apply_url_cookie_session_req = models.CharField(max_length=3, blank=True)
    apply_url_non_portable = models.CharField(max_length=3, blank=True)
    apply_url_login_req = models.CharField(max_length=3, blank=True)
    detail_page_url = models.TextField(blank=True)
    detail_page_url_cookie_session_req = models.CharField(max_length=3, blank=True)
    detail_page_url_non_portable = models.CharField(max_length=3, blank=True)
    detail_page_login_req = models.CharField(max_length=3, blank=True)
    careers_page_url = models.TextField(blank=True)
    careers_page_url_cookie_session_req = models.CharField(max_length=3, blank=True)
    careers_page_url_non_portable = models.CharField(max_length=3, blank=True)
    careers_page_url_login_req = models.CharField(max_length=3, blank=True)
    robot_engineer = models.CharField(max_length=765, blank=True)
    robotid = models.IntegerField(null=True, db_column='robotId', blank=True) # Field name made lowercase.
    robotrunid = models.IntegerField(null=True, db_column='robotRunId', blank=True) # Field name made lowercase.
    refindkey = models.CharField(unique=True, max_length=120, db_column='refindKey', blank=True) # Field name made lowercase.
    firstextractiondate = models.DateTimeField(null=True, db_column='firstExtractionDate', blank=True) # Field name made lowercase.
    latestextractiondate = models.DateTimeField(null=True, db_column='latestExtractionDate', blank=True) # Field name made lowercase.
    extractedinlatestrun = models.CharField(max_length=3, db_column='extractedInLatestRun', blank=True) # Field name made lowercase.
    latitude = models.CharField(max_length=30, blank=True)
    longitude = models.CharField(max_length=30, blank=True)
    data_source = models.CharField(max_length=300)
    lucene_operation = models.CharField(max_length=30, blank=True)
    normalized_company_name = models.CharField(max_length=765, blank=True)
    source = models.CharField(max_length=450, blank=True)
    hasduplicates = models.CharField(max_length=3, db_column='HasDuplicates', blank=True) # Field name made lowercase.
    masterjobkey = models.CharField(max_length=120, db_column='MasterJobKey', blank=True) # Field name made lowercase.
    dedupe_company = models.CharField(max_length=765, blank=True)
    job_attributes = models.CharField(max_length=765, blank=True)
    company_ranked_list = models.CharField(max_length=765, blank=True)
    intra_source_hash = models.CharField(max_length=96, blank=True)
    inter_source_hash = models.CharField(max_length=96, blank=True)
    lasttouchtimestamp = models.DateTimeField(db_column='lastTouchTimestamp') # Field name made lowercase.
    company_key = models.CharField(max_length=120, blank=True)
    onet_code = models.CharField(max_length=765, blank=True)
    job_metadata = models.CharField(max_length=765, blank=True)
    permalinkkey = models.CharField(max_length=30, db_column='permalinkKey', blank=True) # Field name made lowercase.
    employer_type = models.CharField(max_length=765, blank=True)
    source_type = models.CharField(max_length=765, blank=True)
    segmentation_value = models.TextField(blank=True)
    publisher_id = models.IntegerField(null=True, blank=True)
    region = models.CharField(max_length=765, blank=True)
    region_id = models.CharField(max_length=765, blank=True)
    category_string = models.CharField(max_length=765, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    user_field_1 = models.IntegerField(null=True, blank=True)
    user_field_2 = models.IntegerField(null=True, blank=True)
    user_field_3 = models.CharField(max_length=765, blank=True)
    user_field_4 = models.CharField(max_length=765, blank=True)
    user_field_5 = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'DeletedJobs'
"""

class FormattedDescriptions(models.Model):
    id = models.IntegerField(primary_key=True)
    refindkey = models.CharField(unique=True, max_length=120, db_column='refindKey', blank=True) # Field name made lowercase.
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'FormattedDescriptions'
        in_db = 'jobs_latin1'

class ProductionJobs(models.Model):
    job_id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765, blank=True)
    job_board_name = models.CharField(max_length=765, blank=True)
    company_name = models.CharField(max_length=765, blank=True)
    subsidiary_name = models.CharField(max_length=765, blank=True)
    division = models.CharField(max_length=765, blank=True)
    department = models.CharField(max_length=765, blank=True)
    category_or_function = models.CharField(max_length=765, blank=True)
    location_all = models.TextField(blank=True)
    location_address = models.CharField(max_length=765, blank=True)
    location_city = models.CharField(max_length=765, blank=True)
    location_state = models.CharField(max_length=765, blank=True)
    location_zip = models.CharField(max_length=765, blank=True)
    location_country = models.CharField(max_length=765, blank=True)
    description_all = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    skills_required = models.TextField(blank=True)
    skills_preferred = models.TextField(blank=True)
    company_description = models.TextField(blank=True)
    experience_level_required = models.CharField(max_length=765, blank=True)
    education_level_required = models.CharField(max_length=765, blank=True)
    employment_type_all = models.TextField(blank=True)
    employment_term = models.CharField(max_length=765, blank=True)
    employment_hours = models.CharField(max_length=765, blank=True)
    shifts = models.CharField(max_length=765, blank=True)
    manages_others = models.CharField(max_length=765, blank=True)
    travel_required = models.CharField(max_length=765, blank=True)
    telecommute = models.CharField(max_length=765, blank=True)
    contact_info_all = models.TextField(blank=True)
    contact_name = models.CharField(max_length=765, blank=True)
    contact_email = models.CharField(max_length=765, blank=True)
    contact_phone_number = models.CharField(max_length=765, blank=True)
    contact_fax = models.CharField(max_length=765, blank=True)
    contact_address = models.CharField(max_length=765, blank=True)
    date_posted = models.CharField(max_length=765, blank=True)
    date_posted_norm = models.IntegerField(null=True, blank=True)
    date_posted_timestamp = models.IntegerField(null=True, blank=True)
    date_updated = models.CharField(max_length=765, blank=True)
    closing_date = models.CharField(max_length=765, blank=True)
    compensation_all = models.TextField(blank=True)
    compensation_pay = models.CharField(max_length=765, blank=True)
    compensation_other = models.CharField(max_length=765, blank=True)
    benefits_text = models.TextField(blank=True)
    security_clearance = models.CharField(max_length=765, blank=True)
    keywords = models.CharField(max_length=765, blank=True)
    number_of_positions = models.CharField(max_length=765, blank=True)
    job_board_url = models.TextField(blank=True)
    company_url = models.TextField(blank=True)
    apply_url = models.TextField(blank=True)
    apply_url_cookie_session_req = models.CharField(max_length=3, blank=True)
    apply_url_non_portable = models.CharField(max_length=3, blank=True)
    apply_url_login_req = models.CharField(max_length=3, blank=True)
    detail_page_url = models.TextField(blank=True)
    detail_page_url_cookie_session_req = models.CharField(max_length=3, blank=True)
    detail_page_url_non_portable = models.CharField(max_length=3, blank=True)
    detail_page_login_req = models.CharField(max_length=3, blank=True)
    careers_page_url = models.TextField(blank=True)
    careers_page_url_cookie_session_req = models.CharField(max_length=3, blank=True)
    careers_page_url_non_portable = models.CharField(max_length=3, blank=True)
    careers_page_url_login_req = models.CharField(max_length=3, blank=True)
    robot_engineer = models.CharField(max_length=765, blank=True)
    robotid = models.IntegerField(null=True, db_column='robotId', blank=True) # Field name made lowercase.
    robotrunid = models.IntegerField(null=True, db_column='robotRunId', blank=True) # Field name made lowercase.
    refindkey = models.CharField(max_length=120, db_column='refindKey', blank=True) # Field name made lowercase.
    firstextractiondate = models.DateTimeField(null=True, db_column='firstExtractionDate', blank=True) # Field name made lowercase.
    latestextractiondate = models.DateTimeField(null=True, db_column='latestExtractionDate', blank=True) # Field name made lowercase.
    extractedinlatestrun = models.CharField(max_length=3, db_column='extractedInLatestRun', blank=True) # Field name made lowercase.
    latitude = models.CharField(max_length=30, blank=True)
    longitude = models.CharField(max_length=30, blank=True)
    data_source = models.CharField(max_length=300)
    lucene_operation = models.CharField(max_length=30, blank=True)
    normalized_company_name = models.CharField(max_length=765, blank=True)
    source = models.CharField(max_length=450, blank=True)
    hasduplicates = models.CharField(max_length=3, db_column='HasDuplicates', blank=True) # Field name made lowercase.
    masterjobkey = models.CharField(max_length=120, db_column='MasterJobKey', blank=True) # Field name made lowercase.
    dedupe_company = models.CharField(max_length=765, blank=True)
    job_attributes = models.CharField(max_length=765, blank=True)
    company_ranked_list = models.CharField(max_length=765, blank=True)
    intra_source_hash = models.CharField(max_length=96, blank=True)
    inter_source_hash = models.CharField(max_length=96, blank=True)
    lasttouchtimestamp = models.DateTimeField(db_column='lastTouchTimestamp') # Field name made lowercase.
    company_key = models.CharField(max_length=120, blank=True)
    onet_code = models.CharField(max_length=765, blank=True)
    job_metadata = models.CharField(max_length=765, blank=True)
    permalinkkey = models.CharField(max_length=30, db_column='permalinkKey', blank=True) # Field name made lowercase.
    employer_type = models.CharField(max_length=765, blank=True)
    source_type = models.CharField(max_length=765, blank=True)
    segmentation_value = models.TextField(blank=True)
    publisher_id = models.IntegerField(null=True, blank=True)
    region = models.CharField(max_length=765, blank=True)
    region_id = models.IntegerField(null=True, blank=True)
    category_string = models.CharField(max_length=765, blank=True)
    category_id = models.CharField(max_length=765, blank=True)
    user_field_1 = models.IntegerField(null=True, blank=True)
    user_field_2 = models.IntegerField(null=True, blank=True)
    user_field_3 = models.CharField(max_length=765, blank=True)
    user_field_4 = models.CharField(max_length=765, blank=True)
    user_field_5 = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'ProductionJobs'
        in_db = 'jobs'

"""
class Productionjobsaux(models.Model):
    id = models.IntegerField(primary_key=True)
    refindkey = models.CharField(unique=True, max_length=120, db_column='refindKey') # Field name made lowercase.
    score = models.FloatField(null=True, blank=True)
    robotid = models.IntegerField(db_column='robotId') # Field name made lowercase.
    matched_rules = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'ProductionJobsAux'

class Checkpoint(models.Model):
    workflow_id = models.CharField(max_length=60, primary_key=True)
    last_processed_timestamp = models.CharField(max_length=150)
    last_processed_refindkey = models.CharField(max_length=765, db_column='last_processed_refindKey', blank=True) # Field name made lowercase.
    last_modified = models.DateTimeField()
    class Meta:
        db_table = u'checkpoint'

class DedupeTransactions(models.Model):
    inter_source_hash = models.CharField(max_length=96, primary_key=True)
    lock_time = models.DateTimeField()
    pid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'dedupe_transactions'

"""
