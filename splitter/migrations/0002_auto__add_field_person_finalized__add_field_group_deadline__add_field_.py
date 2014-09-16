# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.finalized'
        db.add_column(u'splitter_person', 'finalized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Group.deadline'
        db.add_column(u'splitter_group', 'deadline',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Group.currency'
        db.add_column(u'splitter_group', 'currency',
                      self.gf('django.db.models.fields.CharField')(default='usd', max_length=7),
                      keep_default=False)

        # Adding field 'Group.url_hash'
        db.add_column(u'splitter_group', 'url_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=6, null=True),
                      keep_default=False)

        # Adding field 'Group.paid'
        db.add_column(u'splitter_group', 'paid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Group.payment_algorithm'
        db.add_column(u'splitter_group', 'payment_algorithm',
                      self.gf('django.db.models.fields.CharField')(default='reg', max_length=3),
                      keep_default=False)

        # Adding field 'Item.comment'
        db.add_column(u'splitter_item', 'comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.finalized'
        db.delete_column(u'splitter_person', 'finalized')

        # Deleting field 'Group.deadline'
        db.delete_column(u'splitter_group', 'deadline')

        # Deleting field 'Group.currency'
        db.delete_column(u'splitter_group', 'currency')

        # Deleting field 'Group.url_hash'
        db.delete_column(u'splitter_group', 'url_hash')

        # Deleting field 'Group.paid'
        db.delete_column(u'splitter_group', 'paid')

        # Deleting field 'Group.payment_algorithm'
        db.delete_column(u'splitter_group', 'payment_algorithm')

        # Deleting field 'Item.comment'
        db.delete_column(u'splitter_item', 'comment')


    models = {
        u'splitter.group': {
            'Meta': {'object_name': 'Group'},
            'administrator_ID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['splitter.Person']", 'null': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'usd'", 'max_length': '7'}),
            'deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'payment_algorithm': ('django.db.models.fields.CharField', [], {'default': "'reg'", 'max_length': '3'}),
            'person_passcodes_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'use_categories': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_dates': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_descriptions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_pictures': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'splitter.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'finalized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_ID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['splitter.Group']"}),
            'header_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'passcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user_login': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['splitter']