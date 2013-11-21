# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

# TODO: Add primary_key for the rest of the models.

import django.db.models.options as options
from django.db import models

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

class Accounts(models.Model):
    accountid = models.IntegerField(primary_key=True, db_column='accountId') # Field name made lowercase.
    type = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'accounts'
        in_db = 'jbb'

class OrgAccounts(models.Model):
    orgactid = models.IntegerField(primary_key=True, db_column='orgactId') # Field name made lowercase.
    orgid = models.ForeignKey('Organizations', db_column='orgId') # Field name made lowercase.
    accountid = models.ForeignKey(Accounts, db_column='accountId') # Field name made lowercase.
    orderno = models.IntegerField()
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_accounts'
        in_db = 'jbb'

class OrgDomains(models.Model):
    domainid = models.IntegerField(primary_key=True, db_column='domainId') # Field name made lowercase.
    orgid = models.ForeignKey(Accounts, db_column='orgId') # Field name made lowercase.
    domain_type = models.IntegerField()
    domain_name = models.CharField(max_length=384)
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_domains'
        in_db = 'jbb'

class Organizations(models.Model):
    orgid = models.ForeignKey(Accounts, primary_key=True, db_column='orgId') # Field name made lowercase.
    orgname = models.CharField(max_length=144, db_column='orgName') # Field name made lowercase.
    default_domainid = models.ForeignKey(OrgDomains, null=True, db_column='default_domainId', blank=True) # Field name made lowercase.
    default_hostid = models.ForeignKey(OrgDomains, null=True, db_column='default_hostId', blank=True) # Field name made lowercase.
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    main_site_url = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'organizations'
        in_db = 'jbb'

class Jobs(models.Model):
    jobid = models.IntegerField(primary_key=True, db_column='jobId') # Field name made lowercase.
    cat_orgid = models.ForeignKey(Organizations, null=True, db_column='cat_orgId', blank=True) # Field name made lowercase.
    cat_type = models.IntegerField()
    cat_loc_country = models.CharField(max_length=6)
    cat_loc_state = models.IntegerField()
    cat_loc_county = models.IntegerField()
    cat_loc_city = models.IntegerField()
    cat_occ_top = models.IntegerField()
    cat_occ_sub = models.CharField(max_length=21)
    cat_industry = models.CharField(max_length=18)
    job_title = models.CharField(max_length=192)
    job_company = models.CharField(max_length=144)
    job_company_url = models.CharField(max_length=384)
    job_street = models.CharField(max_length=192)
    job_intl_location = models.CharField(max_length=384)
    job_zip = models.CharField(max_length=48)
    job_salary = models.CharField(max_length=72)
    job_apply_email = models.CharField(max_length=384)
    job_apply_web = models.TextField()
    job_description = models.TextField()
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    job_url = models.CharField(max_length=384)
    class Meta:
        db_table = u'jobs'
        in_db = 'jbb'

class Packages(models.Model):
    packageid = models.IntegerField(primary_key=True, db_column='packageId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    type = models.IntegerField()
    currency_code = models.CharField(max_length=9)
    price = models.DecimalField(max_digits=17, decimal_places=5)
    name = models.CharField(max_length=192)
    description = models.CharField(max_length=765)
    createdid = models.ForeignKey(OrgAccounts, db_column='createdId') # Field name made lowercase.
    created = models.DateTimeField()
    created_by = models.CharField(max_length=192)
    code = models.CharField(max_length=192)
    expiration_date = models.DateTimeField()
    reach_type = models.CharField(max_length=765)
    discount_type = models.CharField(max_length=192)
    post_limit = models.IntegerField()
    class Meta:
        db_table = u'packages'
        in_db = 'jbb'

class Invoices(models.Model):
    invoiceid = models.IntegerField(primary_key=True, db_column='invoiceId') # Field name made lowercase.
    accountid = models.ForeignKey(Accounts, db_column='accountId') # Field name made lowercase.
    account_proxy_id = models.IntegerField()
    packageid = models.ForeignKey(Packages, db_column='packageId') # Field name made lowercase.
    pkg_jobpost_id = models.IntegerField()
    payment_method = models.IntegerField()
    payment_code = models.CharField(max_length=9)
    payment_amount = models.DecimalField(max_digits=17, decimal_places=5)
    payment_usdrate = models.DecimalField(max_digits=12, decimal_places=4)
    startedid = models.ForeignKey(OrgAccounts, db_column='startedId') # Field name made lowercase.
    started = models.DateTimeField()
    class Meta:
        db_table = u'invoices'
        in_db = 'jbb'

class AccountContacts(models.Model):
    contactid = models.IntegerField(primary_key=True, db_column='contactId') # Field name made lowercase.
    ownerid = models.ForeignKey(Accounts, db_column='ownerId') # Field name made lowercase.
    companyname = models.CharField(max_length=144, db_column='companyName') # Field name made lowercase.
    companytitle = models.CharField(max_length=144, db_column='companyTitle') # Field name made lowercase.
    firstname = models.CharField(max_length=144, db_column='firstName') # Field name made lowercase.
    lastname = models.CharField(max_length=144, db_column='lastName') # Field name made lowercase.
    description = models.CharField(max_length=765)
    email = models.CharField(max_length=384)
    phone = models.CharField(max_length=72)
    locationname = models.CharField(max_length=144, db_column='locationName') # Field name made lowercase.
    street = models.CharField(max_length=192)
    city = models.CharField(max_length=192)
    state = models.CharField(max_length=192)
    zip = models.CharField(max_length=48)
    country = models.CharField(max_length=192)
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'account_contacts'
        in_db = 'jbb'

class AccountFiles(models.Model):
    fileid = models.IntegerField(primary_key=True, db_column='fileId') # Field name made lowercase.
    ownerid = models.IntegerField(db_column='ownerId') # Field name made lowercase.
    status = models.IntegerField()
    size = models.IntegerField()
    name = models.CharField(max_length=384)
    type = models.CharField(max_length=192)
    data = models.TextField(blank=True)
    uploaded = models.DateTimeField()
    class Meta:
        db_table = u'account_files'
        in_db = 'jbb'

class AccountStatus(models.Model):
    accountid = models.ForeignKey(Accounts, db_column='accountId') # Field name made lowercase.
    status = models.IntegerField()
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'account_status'
        in_db = 'jbb'

class CatLocationsEnUs(models.Model):
    country_code = models.CharField(unique=True, max_length=6)
    state_code = models.IntegerField(unique=True)
    county_code = models.IntegerField(unique=True)
    city_code = models.IntegerField(unique=True)
    country_name = models.CharField(max_length=192)
    country_abbr = models.CharField(max_length=48)
    state_name = models.CharField(max_length=192)
    state_abbr = models.CharField(max_length=6)
    county_name = models.CharField(max_length=192)
    city_name = models.CharField(max_length=192)
    class Meta:
        db_table = u'cat_locations_en_us'
        in_db = 'jbb'

class CatOccupationsEnUs(models.Model):
    occupationid = models.IntegerField(primary_key=True, db_column='occupationId') # Field name made lowercase.
    name = models.CharField(unique=True, max_length=192)
    abbr = models.CharField(max_length=48)
    description = models.CharField(max_length=765)
    class Meta:
        db_table = u'cat_occupations_en_us'
        in_db = 'jbb'

class CatRegionsEnUs(models.Model):
    regionid = models.IntegerField(primary_key=True, db_column='regionId') # Field name made lowercase.
    name = models.CharField(max_length=192)
    abbr = models.CharField(max_length=48)
    description = models.CharField(max_length=765)
    class Meta:
        db_table = u'cat_regions_en_us'
        in_db = 'jbb'

class CatRegionsGeocoded(models.Model):
    region_id = models.IntegerField()
    state = models.CharField(max_length=192, blank=True)
    min_latitude = models.DecimalField(max_digits=13, decimal_places=6)
    max_latitude = models.DecimalField(max_digits=13, decimal_places=6)
    min_longitude = models.DecimalField(max_digits=13, decimal_places=6)
    max_longitude = models.DecimalField(max_digits=13, decimal_places=6)
    class Meta:
        db_table = u'cat_regions_geocoded'
        in_db = 'jbb'

class CatRegionsGeocodedCities(models.Model):
    region_id = models.IntegerField()
    city = models.CharField(max_length=192, blank=True)
    state = models.CharField(max_length=192, blank=True)
    class Meta:
        db_table = u'cat_regions_geocoded_cities'
        in_db = 'jbb'

class CatRegionsHierarchy(models.Model):
    regionid = models.ForeignKey(CatRegionsEnUs, db_column='regionId') # Field name made lowercase.
    parentid = models.ForeignKey(CatRegionsEnUs, null=True, db_column='parentId', blank=True) # Field name made lowercase.
    lft = models.IntegerField()
    rgt = models.IntegerField()
    class Meta:
        db_table = u'cat_regions_hierarchy'
        in_db = 'jbb'

class Feedburner(models.Model):
    orgid = models.IntegerField(primary_key=True, db_column='orgId') # Field name made lowercase.
    feedid = models.IntegerField(null=True, db_column='feedId', blank=True) # Field name made lowercase.
    feeduri = models.CharField(max_length=765, db_column='feedUri', blank=True) # Field name made lowercase.
    feedtitle = models.CharField(max_length=765, db_column='feedTitle', blank=True) # Field name made lowercase.
    feedurl = models.CharField(max_length=765, db_column='feedUrl', blank=True) # Field name made lowercase.
    feedburnerurl = models.CharField(max_length=765, db_column='feedburnerUrl', blank=True) # Field name made lowercase.
    updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'feedburner'
        in_db = 'jbb'

class FipsCountriesEnUs(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    short_display = models.CharField(max_length=384)
    long_display = models.CharField(max_length=384)
    class Meta:
        db_table = u'fips_countries_en_us'
        in_db = 'jbb'

class InvoiceReceiptsSecure(models.Model):
    invoiceid = models.IntegerField(primary_key=True, db_column='invoiceId') # Field name made lowercase.
    jobpostid = models.IntegerField(db_column='jobpostId') # Field name made lowercase.
    job_post_date = models.DateTimeField()
    job_title = models.CharField(max_length=192)
    job_company = models.CharField(max_length=144)
    job_location = models.CharField(max_length=765)
    post_enddate = models.DateTimeField()
    token = models.CharField(max_length=60)
    job_board_id = models.IntegerField()
    job_board_name = models.CharField(max_length=765)
    transaction_id = models.CharField(max_length=384)
    poster_org_id = models.IntegerField()
    poster_first_name = models.CharField(max_length=765)
    poster_last_name = models.CharField(max_length=765)
    poster_email = models.CharField(max_length=384)
    poster_phone = models.CharField(max_length=72)
    billing_first_name = models.CharField(max_length=765)
    billing_last_name = models.CharField(max_length=765)
    billing_address1 = models.CharField(max_length=765)
    billing_address2 = models.CharField(max_length=765)
    billing_city = models.CharField(max_length=765)
    billing_state = models.CharField(max_length=765)
    billing_zip = models.CharField(max_length=765)
    billing_phone = models.CharField(max_length=765)
    billing_card_type = models.CharField(max_length=60, blank=True)
    billing_card_last_4_digits = models.CharField(max_length=12, blank=True)
    transaction_type = models.IntegerField()
    original_post_price = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    discount_id = models.IntegerField(null=True, blank=True)
    discount_name = models.CharField(max_length=192, blank=True)
    discount_code = models.CharField(max_length=192, blank=True)
    discount_amount = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    package_id = models.IntegerField(null=True, blank=True)
    package_name = models.CharField(max_length=192, blank=True)
    package_code = models.CharField(max_length=192, blank=True)
    package_price = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    package_job_number = models.IntegerField(null=True, blank=True)
    package_job_total = models.IntegerField(null=True, blank=True)
    final_price = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    currency_code = models.CharField(max_length=9)
    payment_test_mode = models.IntegerField()
    receipt_recipient_email = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'invoice_receipts_secure'
        in_db = 'jbb'

class InvoiceState(models.Model):
    invoiceid = models.ForeignKey(Invoices, db_column='invoiceId') # Field name made lowercase.
    state = models.IntegerField()
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'invoice_state'
        in_db = 'jbb'

class JbbUserSmbAccount(models.Model):
    jbbusersmbaccount_id = models.IntegerField(primary_key=True)
    user_email = models.CharField(max_length=762)
    has_smb_account = models.IntegerField(null=True, blank=True)
    has_smb_career_site = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    class Meta:
        db_table = u'jbb_user_smb_account'
        in_db = 'jbb'

class JobAcls(models.Model):
    token = models.CharField(max_length=60, primary_key=True)
    accountid = models.ForeignKey(Accounts, db_column='accountId') # Field name made lowercase.
    jobid = models.ForeignKey(Jobs, db_column='jobId') # Field name made lowercase.
    access = models.IntegerField()
    modifiedid = models.ForeignKey(OrgAccounts, db_column='modifiedId') # Field name made lowercase.
    modified = models.DateTimeField()
    class Meta:
        db_table = u'job_acls'
        in_db = 'jbb'

class PkgJobposts(models.Model):
    pkg_jobpost_id = models.IntegerField(primary_key=True)
    packageid = models.ForeignKey(Packages, db_column='packageId') # Field name made lowercase.
    post_price = models.DecimalField(max_digits=17, decimal_places=5)
    post_currency_code = models.CharField(max_length=9)
    post_quantity = models.IntegerField()
    post_duration = models.IntegerField()
    post_siteid = models.ForeignKey(Organizations, db_column='post_siteId') # Field name made lowercase.
    post_network = models.IntegerField()
    class Meta:
        db_table = u'pkg_jobposts'
        in_db = 'jbb'

class JobPosts(models.Model):
    jobpostid = models.IntegerField(primary_key=True, db_column='jobpostId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    jobid = models.ForeignKey(Jobs, db_column='jobId') # Field name made lowercase.
    packageid = models.ForeignKey(PkgJobposts, db_column='packageId') # Field name made lowercase.
    contactid = models.ForeignKey(AccountContacts, null=True, db_column='contactId', blank=True) # Field name made lowercase.
    post_siteid = models.ForeignKey(Organizations, null=True, db_column='post_siteId', blank=True) # Field name made lowercase.
    post_network = models.IntegerField()
    post_state = models.IntegerField()
    post_enddate = models.DateTimeField()
    custom_catlocid = models.ForeignKey(CatRegionsEnUs, null=True, db_column='custom_catlocId', blank=True) # Field name made lowercase.
    custom_catoccid = models.ForeignKey(CatOccupationsEnUs, null=True, db_column='custom_catoccId', blank=True) # Field name made lowercase.
    revisedid = models.ForeignKey(OrgAccounts, db_column='revisedId') # Field name made lowercase.
    revised = models.DateTimeField()
    createdid = models.ForeignKey(OrgAccounts, db_column='createdId') # Field name made lowercase.
    created = models.DateTimeField()
    class Meta:
        db_table = u'job_posts'
        in_db = 'jbb'

class JobApplicants(models.Model):
    jobactid = models.IntegerField(primary_key=True, db_column='jobactId') # Field name made lowercase.
    jobpostid = models.ForeignKey(JobPosts, db_column='jobpostId') # Field name made lowercase.
    accountid = models.ForeignKey(Accounts, db_column='accountId') # Field name made lowercase.
    app_name = models.CharField(max_length=192)
    app_subject = models.CharField(max_length=192)
    app_coverletter = models.TextField()
    app_resumeid = models.IntegerField(null=True, db_column='app_resumeId', blank=True) # Field name made lowercase.
    app_date = models.DateTimeField()
    class Meta:
        db_table = u'job_applicants'
        in_db = 'jbb'

class JobLogo(models.Model):
    jobid = models.IntegerField(primary_key=True, db_column='jobId') # Field name made lowercase.
    logo_fileid = models.IntegerField(null=True, db_column='logo_fileId', blank=True) # Field name made lowercase.
    logo_aspect = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'job_logo'
        in_db = 'jbb'

class JobPostApproval(models.Model):
    jobpostid = models.ForeignKey(JobPosts, db_column='jobpostId') # Field name made lowercase.
    approval = models.IntegerField(primary_key=True)
    reason = models.CharField(max_length=765)
    approvedid = models.ForeignKey(OrgAccounts, db_column='approvedId') # Field name made lowercase.
    approved = models.DateTimeField()
    class Meta:
        db_table = u'job_post_approval'
        in_db = 'jbb'

class JobPostMetrics(models.Model):
    jobpostid = models.ForeignKey(JobPosts, db_column='jobpostId') # Field name made lowercase.
    count_view = models.IntegerField()
    count_apply_email = models.IntegerField()
    count_apply_web = models.IntegerField()
    adjusted = models.DateTimeField()
    class Meta:
        db_table = u'job_post_metrics'
        in_db = 'jbb'

class Network(models.Model):
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    parentid = models.ForeignKey(Organizations, null=True, db_column='parentId', blank=True) # Field name made lowercase.
    lft = models.IntegerField()
    rgt = models.IntegerField()
    class Meta:
        db_table = u'network'
        in_db = 'jbb'

class OrgAccountInfo(models.Model):
    orgactid = models.ForeignKey(OrgAccounts, db_column='orgactId') # Field name made lowercase.
    active = models.IntegerField()
    contactid = models.ForeignKey(AccountContacts, null=True, db_column='contactId', blank=True) # Field name made lowercase.
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_account_info'
        in_db = 'jbb'

class OrgAccountRoles(models.Model):
    orgactid = models.ForeignKey(OrgAccounts, db_column='orgactId') # Field name made lowercase.
    role = models.IntegerField(unique=True)
    valid = models.IntegerField()
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_account_roles'
        in_db = 'jbb'

class OrgBalanceSecure(models.Model):
    orgbalancesecure_id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    class Meta:
        db_table = u'org_balance_secure'
        in_db = 'jbb'

class OrgBalanceDetailsSecure(models.Model):
    org_balance = models.ForeignKey(OrgBalanceSecure)
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    org_name = models.CharField(max_length=765)
    org_domain = models.CharField(max_length=384)
    post_balance = models.DecimalField(max_digits=17, decimal_places=5)
    ad_balance = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=30)
    last_post_payout = models.DateTimeField()
    last_ad_payout = models.DateTimeField()
    last_payment_date = models.DateTimeField()
    class Meta:
        db_table = u'org_balance_details_secure'
        in_db = 'jbb'


class OrgBranding(models.Model):
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    logo_fileid = models.IntegerField(null=True, db_column='logo_fileId', blank=True) # Field name made lowercase.
    theme = models.IntegerField()
    theme_attributes = models.TextField()
    custom_header = models.TextField()
    custom_footer = models.TextField()
    custom_page_properties = models.TextField()
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_branding'
        in_db = 'jbb'

class OrgBrandingLinks(models.Model):
    linkid = models.IntegerField(primary_key=True, db_column='linkId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    type = models.IntegerField()
    link_order = models.IntegerField()
    link_text = models.CharField(max_length=192)
    link_url = models.CharField(max_length=384)
    class Meta:
        db_table = u'org_branding_links'
        in_db = 'jbb'

class OrgCatIndustries(models.Model):
    orgindid = models.IntegerField(primary_key=True, db_column='orgindId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    industry_code = models.CharField(max_length=18)
    class Meta:
        db_table = u'org_cat_industries'
        in_db = 'jbb'

class OrgCatIndustriesEnUs(models.Model):
    orgindid = models.ForeignKey(OrgCatIndustries, db_column='orgindId') # Field name made lowercase.
    name = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'org_cat_industries_en_us'
        in_db = 'jbb'

class OrgCatJobtypes(models.Model):
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    type_mask = models.IntegerField()
    class Meta:
        db_table = u'org_cat_jobtypes'
        in_db = 'jbb'

class OrgCatOccupations(models.Model):
    orgoccid = models.IntegerField(primary_key=True, db_column='orgoccId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    occupationid = models.ForeignKey(CatOccupationsEnUs, db_column='occupationId') # Field name made lowercase.
    top_code = models.IntegerField()
    sub_code = models.CharField(max_length=21)
    class Meta:
        db_table = u'org_cat_occupations'
        in_db = 'jbb'

class OrgCatRegions(models.Model):
    orgregid = models.IntegerField(primary_key=True, db_column='orgregId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    regionid = models.ForeignKey(CatRegionsEnUs, db_column='regionId') # Field name made lowercase.
    class Meta:
        db_table = u'org_cat_regions'
        in_db = 'jbb'

class OrgPackages(models.Model):
    orgpkgid = models.IntegerField(primary_key=True, db_column='orgpkgId') # Field name made lowercase.
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    packageid = models.ForeignKey(Packages, db_column='packageId') # Field name made lowercase.
    avail_orgid = models.ForeignKey(Organizations, db_column='avail_orgId') # Field name made lowercase.
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_packages'
        in_db = 'jbb'

class OrgPublisherInfo(models.Model):
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    publisher_id = models.IntegerField(null=True, blank=True)
    preference_listing = models.IntegerField()
    premium_cap = models.IntegerField()
    organic_cap = models.IntegerField()
    overall_cap = models.IntegerField()
    display_quantity = models.IntegerField()
    backfill_preference = models.IntegerField()
    search_location = models.CharField(max_length=765)
    search_keyword_all = models.CharField(max_length=765)
    search_keyword_exact = models.CharField(max_length=765)
    search_keyword_at_least_one = models.CharField(max_length=765)
    search_keyword_without = models.CharField(max_length=765)
    search_keyword_within_title = models.CharField(max_length=765)
    search_keyword_within_company = models.CharField(max_length=765)
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'org_publisher_info'
        in_db = 'jbb'

class OrgSettings(models.Model):
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    testmode = models.IntegerField(null=True, db_column='testMode', blank=True) # Field name made lowercase.
    updated = models.DateTimeField()
    search = models.IntegerField()
    allow_international_postings = models.IntegerField()
    allow_post_notifications = models.IntegerField()
    class Meta:
        db_table = u'org_settings'
        in_db = 'jbb'

class OrgW9Secure(models.Model):
    orgw9secure_id = models.IntegerField(primary_key=True)
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    social_security = models.CharField(max_length=765)
    ein = models.CharField(max_length=765)
    business_name = models.CharField(max_length=384)
    business_type = models.IntegerField()
    business_other_type = models.CharField(max_length=384)
    withholding_exempt = models.IntegerField()
    address = models.CharField(max_length=192)
    city = models.CharField(max_length=192)
    state = models.CharField(max_length=192)
    zip = models.CharField(max_length=48)
    country = models.CharField(max_length=192)
    backup_withholding = models.IntegerField()
    signature = models.CharField(max_length=384)
    timestamp = models.DateTimeField()
    ip_address = models.CharField(max_length=384)
    updated_id = models.IntegerField()
    class Meta:
        db_table = u'org_w9_secure'
        in_db = 'jbb'

class OrganizationMetrics(models.Model):
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    signup_ip = models.CharField(max_length=765)
    signup_gr = models.CharField(max_length=765)
    misc = models.TextField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'organization_metrics'
        in_db = 'jbb'

class PackageRevshare(models.Model):
    packageid = models.ForeignKey(Packages, db_column='packageId') # Field name made lowercase.
    pkg_jobpost_id = models.IntegerField()
    sh_fixed = models.DecimalField(max_digits=12, decimal_places=4)
    sh_percentage = models.DecimalField(max_digits=8, decimal_places=4)
    discount_fixed = models.DecimalField(max_digits=12, decimal_places=4)
    discount_percentage = models.DecimalField(max_digits=8, decimal_places=4)
    commission_fixed = models.DecimalField(max_digits=12, decimal_places=4)
    commission_percentage = models.DecimalField(max_digits=8, decimal_places=4)
    class Meta:
        db_table = u'package_revshare'
        in_db = 'jbb'

class PackageStatus(models.Model):
    packageid = models.ForeignKey(Packages, db_column='packageId') # Field name made lowercase.
    status = models.IntegerField()
    updatedid = models.ForeignKey(OrgAccounts, db_column='updatedId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'package_status'
        in_db = 'jbb'

class PaymentMethod(models.Model):
    paymentmethod_id = models.IntegerField(primary_key=True)
    orgid = models.ForeignKey(Organizations, db_column='orgId') # Field name made lowercase.
    method = models.IntegerField()
    method_id = models.IntegerField()
    updated_id = models.IntegerField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'payment_method'
        in_db = 'jbb'

class PaymentMethodCheckSecure(models.Model):
    paymentmethodchecksecure_id = models.IntegerField(primary_key=True)
    orgid = models.IntegerField(db_column='orgId') # Field name made lowercase.
    first_name = models.CharField(max_length=765)
    last_name = models.CharField(max_length=765)
    address_1 = models.CharField(max_length=765)
    address_2 = models.CharField(max_length=765)
    city = models.CharField(max_length=765)
    state = models.CharField(max_length=6)
    zip_code = models.CharField(max_length=30)
    billing_contact_first_name = models.CharField(max_length=765)
    billing_contact_last_name = models.CharField(max_length=765)
    billing_contact_email = models.CharField(max_length=765)
    billing_contact_phone = models.CharField(max_length=765)
    billing_contact_fax = models.CharField(max_length=765)
    updated_id = models.IntegerField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'payment_method_check_secure'
        in_db = 'jbb'

class PaymentMethodPaypalSecure(models.Model):
    paymentmethodpaypalsecure_id = models.IntegerField(primary_key=True)
    orgid = models.IntegerField(db_column='orgId') # Field name made lowercase.
    account = models.CharField(max_length=765)
    updated_id = models.IntegerField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'payment_method_paypal_secure'
        in_db = 'jbb'

class PayoutHistorySecure(models.Model):
    payouthistorysecure_id = models.IntegerField(primary_key=True)
    orgid = models.IntegerField(db_column='orgId') # Field name made lowercase.
    revenue = models.DecimalField(max_digits=17, decimal_places=5)
    amount = models.DecimalField(max_digits=17, decimal_places=5)
    job_post_amount = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=30)
    method = models.IntegerField()
    method_id = models.IntegerField()
    ad_server_id = models.IntegerField()
    ad_server_amount = models.DecimalField(max_digits=17, decimal_places=5)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    ad_server_start_date_time = models.DateTimeField()
    ad_server_end_date_time = models.DateTimeField()
    issue_date_time = models.DateTimeField()
    transaction_data = models.CharField(max_length=765)
    status = models.IntegerField()
    create_timestamp = models.DateTimeField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'payout_history_secure'
        in_db = 'jbb'

class PayoutSummarySaveSecure(models.Model):
    orgid = models.IntegerField(db_column='orgId') # Field name made lowercase.
    payout_history_id = models.IntegerField()
    org_name = models.CharField(max_length=765)
    domain_name = models.CharField(max_length=765)
    total_earning = models.DecimalField(max_digits=17, decimal_places=5)
    revenue = models.DecimalField(max_digits=17, decimal_places=5)
    earning = models.DecimalField(max_digits=17, decimal_places=5)
    ad_server_earning = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=15)
    payout_start_date = models.DateTimeField()
    payout_end_date = models.DateTimeField()
    ad_server_start_date = models.DateTimeField()
    ad_server_end_date = models.DateTimeField()
    has_w9 = models.IntegerField()
    status = models.IntegerField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'payout_summary_save_secure'
        in_db = 'jbb'

class PayoutSummarySecure(models.Model):
    orgid = models.IntegerField(primary_key=True, db_column='orgId') # Field name made lowercase.
    payout_history_id = models.IntegerField()
    org_name = models.CharField(max_length=765)
    domain_name = models.CharField(max_length=765)
    total_earning = models.DecimalField(max_digits=17, decimal_places=5)
    revenue = models.DecimalField(max_digits=17, decimal_places=5)
    earning = models.DecimalField(max_digits=17, decimal_places=5)
    ad_server_earning = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=15)
    payout_start_date = models.DateTimeField()
    payout_end_date = models.DateTimeField()
    ad_server_start_date = models.DateTimeField()
    ad_server_end_date = models.DateTimeField()
    has_w9 = models.IntegerField()
    status = models.IntegerField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'payout_summary_secure'
        in_db = 'jbb'

class PaypalTransactionSecure(models.Model):
    paypaltransactionsecure_id = models.IntegerField(primary_key=True)
    orgid = models.IntegerField(db_column='orgId') # Field name made lowercase.
    payout_history_id = models.IntegerField()
    transaction_data = models.CharField(max_length=765)
    payment_status = models.CharField(max_length=765)
    paypal_status = models.CharField(max_length=765)
    transaction_timestamp = models.DateTimeField()
    class Meta:
        db_table = u'paypal_transaction_secure'
        in_db = 'jbb'

class Transactions(models.Model):
    txnid = models.IntegerField(primary_key=True, db_column='txnId') # Field name made lowercase.
    invoiceid = models.ForeignKey(Invoices, db_column='invoiceId') # Field name made lowercase.
    type = models.IntegerField()
    reason = models.IntegerField()
    amount = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=9)
    transaction = models.CharField(max_length=384)
    transactedid = models.ForeignKey(OrgAccounts, db_column='transactedId') # Field name made lowercase.
    transacted_proxy_id = models.IntegerField()
    transacted = models.DateTimeField()
    payout_history_id = models.IntegerField()
    class Meta:
        db_table = u'transactions'
        in_db = 'jbb'

class TrkDiscountCode(models.Model):
    job_post_id = models.IntegerField()
    package_id = models.IntegerField()
    price = models.DecimalField(max_digits=17, decimal_places=5)
    final_price = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=9)
    discount_amount = models.DecimalField(max_digits=17, decimal_places=5)
    discount_type = models.CharField(max_length=192)
    job_limit = models.IntegerField()
    expiration_date = models.DateTimeField()
    last_updated = models.DateTimeField()
    class Meta:
        db_table = u'trk_discount_code'
        in_db = 'jbb'

class TrkJobPackage(models.Model):
    job_post_id = models.IntegerField()
    package_id = models.IntegerField()
    price = models.DecimalField(max_digits=17, decimal_places=5)
    final_price = models.DecimalField(max_digits=17, decimal_places=5)
    currency_code = models.CharField(max_length=9)
    job_limit = models.IntegerField()
    expiration_date = models.DateTimeField()
    last_updated = models.DateTimeField()
    class Meta:
        db_table = u'trk_job_package'
        in_db = 'jbb'

class Users(models.Model):
    username = models.CharField(max_length=384, primary_key=True, db_column='userName') # Field name made lowercase.
    userid = models.ForeignKey(Accounts, db_column='userId') # Field name made lowercase.
    updated = models.DateTimeField()
    class Meta:
        db_table = u'users'
        in_db = 'jbb'

class UserPassword(models.Model):
    userid = models.ForeignKey(Users, db_column='userId') # Field name made lowercase.
    password = models.CharField(max_length=34)
    password_updated = models.DateTimeField()
    class Meta:
        db_table = u'user_password'
        in_db = 'jbb'

class UserPasswordReset(models.Model):
    userid = models.ForeignKey(Users, db_column='userId') # Field name made lowercase.
    resetkey = models.CharField(max_length=60)
    sent_count = models.IntegerField()
    sent_last = models.DateTimeField()
    reset_created = models.DateTimeField()
    class Meta:
        db_table = u'user_password_reset'
        in_db = 'jbb'
