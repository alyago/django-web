import re
import urllib
from datetime import datetime

from django import forms

import resume.cat_location as cat_location
import resume.jbb_models as jbb
import resume.production_data_deployed_models as production_jobs
from resume.sh_sponsoredjobs_models import JobPost, FeedsAdvertiser

# Pattern from http://www.regular-expressions.info/email.html.
EMAIL_RE = re.compile('\\b([A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4})\\b', re.I)


class ProductionJob(object):

    def __init__(self, refindkey):
        # TODO: Cache the job/sponsorship info if possible.
        # These are the columns that are needed.
        columns = ['refindkey', 'location_city', 'location_state', 'title', 'company_name', 'source',
                   'contact_email', 'date_posted_timestamp', 'detail_page_url', 'lucene_operation',
                   'robotid', 'onet_code', 'location_zip']

        job = production_jobs.ProductionJobs.objects.filter(refindkey=refindkey)[:1].only(*columns)
        self.job = job[0] if job else None

        self.cparm = None
        self.sponsorship = None

    @property
    def location(self):
        city = ' '.join([i.capitalize() for i in self.job.location_city.split()]) if self.job.location_city else ''

        return ', '.join([l for l in [city, self.job.location_state] if l])

    @property
    def location_zip(self):
        return self.job.location_zip

    @property
    def key(self):
        """Returns the job key used for the GET parameter for the SimplyApply URL."""
        return self.job.refindkey if self.job else None

    @property
    def key_type(self):
        """Returns the key type to be used for the hidden input value."""
        return 'jobkey'

    @property
    def title(self):
        return self.job.title

    @property
    def company(self):
        return self.job.company_name

    @property
    def apply_email(self):
        # The apply email for sponsored jobs may be in the sponsorship table and no where else.
        if self.sponsorship:
            try:
                return forms.EmailField().clean(self.sponsorship.simply_apply_receiver_email)
            except forms.ValidationError:
                pass

        if self.job.contact_email:
            result = EMAIL_RE.search(self.job.contact_email)

            return result.groups()[0] if result else None

    @property
    def refindkey(self):
        return self.job.refindkey if self.job else None

    @property
    def source(self):
        return self.job.source

    @property
    def date_posted(self):
        return datetime.fromtimestamp(self.job.date_posted_timestamp)

    @property
    def detail_page_url(self):
        if self.sponsorship:
            self.job.detail_page_url = 'http://www.simplyhired.com/a/job-details/redirect/jobkey-%s/cparm-%s?from=simplyapply' % (urllib.quote(self.key), self.cparm)

        return self.job.detail_page_url

    @property
    def robot_id(self):
        return self.job.robotid

    @property
    def onet(self):
        return self.job.onet_code

    def is_valid(self):
        """Validates whether or not the job has a valid email address and is active."""
        if not self.job:
            return False

        apply_email = self.apply_email
        if self.job.lucene_operation == 'delete' or not apply_email:
            return False

        try:
            forms.EmailField().clean(apply_email)
        except forms.ValidationError:
            return False

        if self.sponsorship:
            if self.sponsorship.enable_simply_apply_web != 'y' and self.sponsorship.enable_simply_apply_mobile != 'y':
                return False

        return True

class JBBJob(object):

    def __init__(self, jobpostid):
        self._jobpost = jbb.JobPosts.objects.get(jobpostid=jobpostid)
        self.job = self._jobpost.jobid

        # Production job info; info used for event logging.
        columns = ['robotid', 'onet_code']
        production_job = production_jobs.ProductionJobs.objects.filter(refindkey=self.refindkey)[:1].only(*columns)
        self._production_job = production_job[0] if production_job else None

        # Sponsorship for SMB jobs.
        self.sponsorship = None
        self.cparm = None

    @property
    def location(self):
        """Returns a human readable location format."""
        location = self.job.job_zip
        location_lookup = cat_location.ZipsEnUs.objects.filter(zip_code=self.job.job_zip, city_type='D')[:1]
        if location_lookup:
            location_lookup = location_lookup[0]
            location = location_lookup.city_name + ', ' + location_lookup.state_abbr

        return location

    @property
    def location_zip(self):
        return self.job.job_zip

    @property
    def key(self):
        """Returns the job key used for the GET parameter for the SimplyApply URL."""
        return self._jobpost.jobpostid

    @property
    def key_type(self):
        """Returns the key type to be used for the hidden input value."""
        return 'job_post_id'

    @property
    def title(self):
        return self.job.job_title

    @property
    def company(self):
        return self.job.job_company

    @property
    def apply_email(self):
        return self.job.job_apply_email

    @property
    def refindkey(self):
        # TODO: Some JBB jobs aren't from the JBB feed.
        return '6256.{0}'.format(self.job.jobid)

    @property
    def source(self):
        # Check to see if this is a SMB job.
        if self._jobpost.post_siteid.orgid.accountid in [754734555, 246268234, 321631812]:
            return 'Simply Hired via Simply Apply'

        # The site name of where the job is posted (i.e. Mashable).
        if self._jobpost.post_siteid and self._jobpost.post_siteid.orgname:
            return 'Simply Hired via ' + self._jobpost.post_siteid.orgname

        return 'Simply Hired via ' + self._jobpost.orgid.orgname

    @property
    def date_posted(self):
        return self._jobpost.created

    @property
    def detail_page_url(self):
        return 'http://' + self._jobpost.post_siteid.default_domainid.domain_name + '/a/jbb/job-details/' + str(self._jobpost.jobpostid)

    @property
    def robot_id(self):
        return self._production_job.robotid if self._production_job else None

    @property
    def onet(self):
        return self._production_job.onet_code if self._production_job else None

    def is_valid(self):
        if not self.job or not self._jobpost:
            return False

        if not self.job.job_apply_email:
            return False

        # See if the job has expired.
        if self._jobpost.post_enddate < datetime.now():
            return False

        jobapproval = jbb.JobPostApproval.objects.filter(jobpostid=self._jobpost.jobpostid)[:1]
        if not jobapproval or not jobapproval[0].approval:
            return False

        return True

class SelfServeJob(ProductionJob):

    def __init__(self, refindkey):
        self.feed_id = ''
        self.job_id = ''

        if refindkey.find('.') > -1:
            self.feed_id, self.job_id = refindkey.split('.', 1)


        self.job = None

        if self.feed_id.isdigit() and self.job_id.isdigit():
            try:
                self.job = JobPost.objects.get(id=self.job_id)
            except JobPost.DoesNotExist:
                self.job = None

    @property
    def location(self):
        return self.job.location

    @property
    def location_zip(self):
        return ''

    @property
    def key(self):
        return '%s.%s' % (self.feed_id, self.job_id)

    @property
    def refindkey(self):
        return '%s.%s' % (self.feed_id, self.job_id)

    @property
    def company(self):
        return self.job.company

    @property
    def apply_email(self):
        return self.job.apply_email

    @property
    def date_posted(self):
        return self.job.posted

    @property
    def detail_page_url(self):
        return 'http://www.simplyhired.com/job-post/' % self.job_id

    @property
    def robot_id(self):
        return self.feed_id

    @property
    def onet_code(self):
        return ''

    def is_valid(self):
        if self.job is None:
            return False

        if not FeedsAdvertiser.objects.filter(advertiser_id=self.job.user.id, feed_id=self.feed_id).exists():
            return False

        return self.job.status == 'active'

def get_job(refindkey=None, jobpostid=None, self_serve=None):
    if refindkey:
        job = ProductionJob(refindkey)
    elif jobpostid:
        job = JBBJob(jobpostid)

    # This handles the case where the self serve job isn't in ProductionJobs yet but is 'active'.
    if self_serve and not job.is_valid():
        job = SelfServeJob(refindkey)

    return job
