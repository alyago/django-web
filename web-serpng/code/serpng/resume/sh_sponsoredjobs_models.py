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

class AccountManagerClientMapping(models.Model):
    account_manager_user_id = models.IntegerField(primary_key=True)
    client_user_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'account_manager_client_mapping'
        in_db = 'sh_sponsoredjobs'

class Advertiser(models.Model):
    advertiser_id = models.IntegerField()
    advertiser_search_query = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'advertiser'
        in_db = 'sh_sponsoredjobs'

class CampaignJobCounts(models.Model):
    timestamp = models.DateTimeField()
    sponsorship_id = models.IntegerField(null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    advertiser_id = models.IntegerField(null=True, blank=True)
    job_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'campaign_job_counts'
        in_db = 'sh_sponsoredjobs'

class RaaClientMapping(models.Model):
    raa_user_id = models.IntegerField(primary_key=True)
    client_user_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'raa_client_mapping'
        in_db = 'sh_sponsoredjobs'

class Sponsorship(models.Model):
    id = models.IntegerField(primary_key=True)
    advertiser_id = models.IntegerField(null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=765, blank=True)
    job_title = models.CharField(max_length=600, blank=True)
    job_title_relation = models.CharField(max_length=30, blank=True)
    job_location = models.CharField(max_length=600, blank=True)
    job_location_radius = models.CharField(max_length=30, blank=True)
    job_company = models.CharField(max_length=600, blank=True)
    job_company_relation = models.CharField(max_length=30, blank=True)
    custom_search_query = models.TextField(blank=True)
    max_cpc = models.FloatField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    all_jobs = models.CharField(max_length=3, blank=True)
    tracking_param = models.CharField(max_length=150, blank=True)
    tracking_param_value = models.CharField(max_length=765, blank=True)
    tracking_url_append_string = models.CharField(max_length=765, blank=True)
    tracking_url_prepend_string = models.CharField(max_length=765, blank=True)
    tracking_prepend_urlencode = models.CharField(max_length=30, blank=True)
    tracking_regexp_pattern = models.CharField(max_length=600, blank=True)
    tracking_regexp_replacement = models.CharField(max_length=600, blank=True)
    enable_simply_apply_mobile = models.CharField(max_length=3, blank=True)
    enable_simply_apply_web = models.CharField(max_length=3, blank=True)
    simply_apply_receiver_email = models.CharField(max_length=765, blank=True)
    ctr = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'sponsorship'
        in_db = 'sh_sponsoredjobs'

class InclickUser(models.Model):

    class Meta:
        db_table = 'inclick_user'
        in_db = 'sh_sponsoredjobs'

class FeedsAdvertiser(models.Model):
    feed_id = models.IntegerField(primary_key=True)
    advertiser_id = models.IntegerField()
    class Meta:
        db_table = u'feeds_advertiser'
        in_db = 'sh_sponsoredjobs'

class JobPost(models.Model):
    """
    'status' values and their meanings:
      'active' - Paid for, has a campaign, is funded, account is verified, and is in rawjobs.
      'paused' - Manually paused campaign OR campaign ran out of money; job removed from RawJobs.
      'closed' - Campaign is closed manually/or some other condition; permanent, job removed from RawJobs.
      'pending' - One or more remaining steps (contact, pricing, account verification, and/or billing) has not been done yet.
    """

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    apply_email = models.EmailField(max_length=100)
    status = models.CharField(max_length=24, default='pending') # See above.
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    user = models.ForeignKey(InclickUser)
    #campaign = models.ForeignKey(InclickCampaigns, to_field='camp_id')

    class Meta:
        db_table = 'job_posts'
        in_db = 'sh_sponsoredjobs'
