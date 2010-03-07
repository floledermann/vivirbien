# coding: utf-8

from south.db import db
from django.db import models
from resources.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'TagQuery.exclude'
        db.add_column('resources_tagquery', 'exclude', orm['resources.tagquery:exclude'])
        
        # Adding field 'TagQuery.boolean'
        db.add_column('resources_tagquery', 'boolean', orm['resources.tagquery:boolean'])
        
        # Adding field 'TagQuery.order'
        db.add_column('resources_tagquery', 'order', orm['resources.tagquery:order'])
        
        # Adding field 'View.order_by'
        db.add_column('resources_view', 'order_by', orm['resources.view:order_by'])
        
        # Changing field 'TagQuery.value'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True, blank=True))
        db.alter_column('resources_tagquery', 'value', orm['resources.tagquery:value'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'TagQuery.exclude'
        db.delete_column('resources_tagquery', 'exclude')
        
        # Deleting field 'TagQuery.boolean'
        db.delete_column('resources_tagquery', 'boolean')
        
        # Deleting field 'TagQuery.order'
        db.delete_column('resources_tagquery', 'order')
        
        # Deleting field 'View.order_by'
        db.delete_column('resources_view', 'order_by')
        
        # Changing field 'TagQuery.value'
        # (to signature: django.db.models.fields.CharField(max_length=100))
        db.alter_column('resources_tagquery', 'value', orm['resources.tagquery:value'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'resources.resource': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'})
        },
        'resources.tag': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': "orm['resources.Resource']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'resources.tagquery': {
            'boolean': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comparison': ('django.db.models.fields.IntegerField', [], {}),
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'queries'", 'to': "orm['resources.View']"})
        },
        'resources.view': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order_by': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'sub_views': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['resources.View']"})
        }
    }
    
    complete_apps = ['resources']
