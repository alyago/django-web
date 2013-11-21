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

class AbbreviationsUsaEnUs(models.Model):
    state_name = models.CharField(max_length=192)
    state_abbr = models.CharField(max_length=6)

    class Meta:
        db_table = u'abbreviations_usa_en_us'
        in_db = 'cat_location'

class CountriesEnUs(models.Model):
    country_code = models.CharField(max_length=6, primary_key=True)
    country_name = models.CharField(max_length=192)
    class Meta:
        db_table = u'countries_en_us'
        in_db = 'cat_location'


class FipsEnUs(models.Model):
    country_code = models.CharField(max_length=6)
    state_code = models.IntegerField()
    county_code = models.IntegerField()
    city_code = models.IntegerField()
    name = models.CharField(max_length=192)

    class Meta:
        db_table = u'fips_en_us'
        in_db = 'cat_location'


class ZipsEnUs(models.Model):
    zip_code = models.CharField(primary_key=True, max_length=15)
    zip_type = models.CharField(max_length=3)
    city_name = models.CharField(max_length=192)
    city_type = models.CharField(max_length=3) # 'D' is the default city name.
    county_name = models.CharField(max_length=192)
    county_fips = models.CharField(max_length=15)
    state_name = models.CharField(max_length=192)
    state_abbr = models.CharField(max_length=6)
    state_fips = models.CharField(max_length=6)
    msa_code = models.CharField(max_length=12)
    area_code = models.CharField(max_length=9)
    time_zone = models.CharField(max_length=48)
    utc = models.DecimalField(max_digits=5, decimal_places=1)
    dst = models.CharField(max_length=3)
    latitude = models.DecimalField(max_digits=11, decimal_places=6)
    longitude = models.DecimalField(max_digits=11, decimal_places=6)

    class Meta:
        db_table = u'zips_en_us'
        in_db = 'cat_location'
