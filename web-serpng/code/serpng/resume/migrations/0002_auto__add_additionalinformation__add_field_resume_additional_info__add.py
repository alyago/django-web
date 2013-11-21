# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdditionalInformation'
        db.create_table('resume_additionalinformation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
        ))
        db.send_create_signal('resume', ['AdditionalInformation'])

        # Adding field 'Resume.additional_info'
        db.add_column('resume_resume', 'additional_info',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.AdditionalInformation'], unique=True, null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Content.pdf'
        db.add_column('resume_content', 'pdf',
                      self.gf('serpng.resume.fields.BlobField')(null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'AdditionalInformation'
        db.delete_table('resume_additionalinformation')

        # Deleting field 'Resume.additional_info'
        db.delete_column('resume_resume', 'additional_info_id')

        # Deleting field 'Content.pdf'
        db.delete_column('resume_content', 'pdf')

    models = {
        'resume.additionalinformation': {
            'Meta': {'object_name': 'AdditionalInformation'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'resume.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'street2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'resume.award': {
            'Meta': {'object_name': 'Award'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']"})
        },
        'resume.certifications': {
            'Meta': {'object_name': 'Certifications'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']"})
        },
        'resume.contact': {
            'Meta': {'object_name': 'Contact'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Address']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'cell_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'resume.content': {
            'Meta': {'object_name': 'Content'},
            'file_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parsed_resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pdf': ('serpng.resume.fields.BlobField', [], {'null': 'True', 'blank': 'True'}),
            'raw_resume': ('serpng.resume.fields.BlobField', [], {'null': 'True', 'blank': 'True'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'resume.education': {
            'Meta': {'ordering': "('-end_date',)", 'object_name': 'Education'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'resume.job': {
            'Meta': {'ordering': "('-end_date',)", 'object_name': 'Job'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naics_code': ('django.db.models.fields.IntegerField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'resume.publication': {
            'Meta': {'object_name': 'Publication'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']"})
        },
        'resume.resume': {
            'Meta': {'object_name': 'Resume'},
            'add_date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'additional_info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.AdditionalInformation']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Contact']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'employer_opt_in': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'search_query': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Skill']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'submitted': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'summary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Summary']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'})
        },
        'resume.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'resume.summary': {
            'Meta': {'object_name': 'Summary'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['resume']