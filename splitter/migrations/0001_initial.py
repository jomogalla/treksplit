# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'splitter_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('passcode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('group_ID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['splitter.Group'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('user_login', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('header_color', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'splitter', ['Person'])

        # Adding model 'Item'
        db.create_table(u'splitter_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('person_ID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['splitter.Person'])),
            ('receipt_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'splitter', ['Item'])

        # Adding model 'Group'
        db.create_table(u'splitter_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('passcode', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('person_passcodes_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_dates', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_categories', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_pictures', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_descriptions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('administrator_ID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['splitter.Person'], null=True)),
        ))
        db.send_create_signal(u'splitter', ['Group'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'splitter_person')

        # Deleting model 'Item'
        db.delete_table(u'splitter_item')

        # Deleting model 'Group'
        db.delete_table(u'splitter_group')


    models = {
        u'splitter.group': {
            'Meta': {'object_name': 'Group'},
            'administrator_ID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['splitter.Person']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'person_passcodes_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_categories': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_dates': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_descriptions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_pictures': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'splitter.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'person_ID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['splitter.Person']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'receipt_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'splitter.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'group_ID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['splitter.Group']"}),
            'header_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user_login': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['splitter']