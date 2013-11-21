# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table('resume_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('street2', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(default='', max_length=40, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('resume', ['Address'])

        # Adding model 'Contact'
        db.create_table('resume_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('work_phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('home_phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('cell_phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Address'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('resume', ['Contact'])

        # Adding model 'Summary'
        db.create_table('resume_summary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
        ))
        db.send_create_signal('resume', ['Summary'])

        # Adding model 'Skill'
        db.create_table('resume_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
        ))
        db.send_create_signal('resume', ['Skill'])

        # Adding model 'Resume'
        db.create_table('resume_resume', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('add_date_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('search_query', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('submitted', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Contact'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
            ('summary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Summary'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Skill'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
            ('employer_opt_in', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')(max_length=11, null=True, blank=True)),
        ))
        db.send_create_signal('resume', ['Resume'])

        # Adding model 'Content'
        db.create_table('resume_content', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('raw_resume', self.gf('serpng.resume.fields.BlobField')(null=True, blank=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(default='', max_length=512, null=True, blank=True)),
            ('parsed_resume', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Resume'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('resume', ['Content'])

        # Adding model 'Job'
        db.create_table('resume_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('employer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=4096, null=True, blank=True)),
            ('naics_code', self.gf('django.db.models.fields.IntegerField')(max_length=6, null=True, blank=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Resume'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('resume', ['Job'])

        # Adding model 'Education'
        db.create_table('resume_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Resume'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('resume', ['Education'])

        # Adding model 'Publication'
        db.create_table('resume_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Resume'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('resume', ['Publication'])

        # Adding model 'Certifications'
        db.create_table('resume_certifications', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Resume'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('resume', ['Certifications'])

        # Adding model 'Award'
        db.create_table('resume_award', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resume.Resume'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('resume', ['Award'])

    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table('resume_address')

        # Deleting model 'Contact'
        db.delete_table('resume_contact')

        # Deleting model 'Summary'
        db.delete_table('resume_summary')

        # Deleting model 'Skill'
        db.delete_table('resume_skill')

        # Deleting model 'Resume'
        db.delete_table('resume_resume')

        # Deleting model 'Content'
        db.delete_table('resume_content')

        # Deleting model 'Job'
        db.delete_table('resume_job')

        # Deleting model 'Education'
        db.delete_table('resume_education')

        # Deleting model 'Publication'
        db.delete_table('resume_publication')

        # Deleting model 'Certifications'
        db.delete_table('resume_certifications')

        # Deleting model 'Award'
        db.delete_table('resume_award')

    models = {
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
            'raw_resume': ('serpng.resume.fields.BlobField', [], {'null': 'True', 'blank': 'True'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['resume.Resume']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'resume.education': {
            'Meta': {'object_name': 'Education'},
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