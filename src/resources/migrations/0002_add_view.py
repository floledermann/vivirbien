# coding: utf-8

from south.db import db
from django.db import models
from resources.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'View'
        db.create_table('resources_view', (
            ('id', orm['resources.view:id']),
            ('name', orm['resources.view:name']),
            ('shortname', orm['resources.view:shortname']),
            ('creator', orm['resources.view:creator']),
            ('creation_date', orm['resources.view:creation_date']),
        ))
        db.send_create_signal('resources', ['View'])
        
        # Adding model 'TagQuery'
        db.create_table('resources_tagquery', (
            ('id', orm['resources.tagquery:id']),
            ('key', orm['resources.tagquery:key']),
            ('comparison', orm['resources.tagquery:comparison']),
            ('value', orm['resources.tagquery:value']),
            ('view', orm['resources.tagquery:view']),
        ))
        db.send_create_signal('resources', ['TagQuery'])
        
        # Adding ManyToManyField 'View.sub_views'
        db.create_table('resources_view_sub_views', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_view', models.ForeignKey(orm.View, null=False)),
            ('to_view', models.ForeignKey(orm.View, null=False))
        ))
        
        # Changing field 'Resource.shortname'
        # (to signature: django.db.models.fields.SlugField(max_length=100, unique=True, db_index=True))
        db.alter_column('resources_resource', 'shortname', orm['resources.resource:shortname'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'View'
        db.delete_table('resources_view')
        
        # Deleting model 'TagQuery'
        db.delete_table('resources_tagquery')
        
        # Dropping ManyToManyField 'View.sub_views'
        db.delete_table('resources_view_sub_views')
        
        # Changing field 'Resource.shortname'
        # (to signature: django.db.models.fields.SlugField(unique=True, max_length=50, db_index=True))
        db.alter_column('resources_resource', 'shortname', orm['resources.resource:shortname'])
        
    
    
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
            'comparison': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'view': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'queries'", 'to': "orm['resources.View']"})
        },
        'resources.view': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shortname': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'db_index': 'True'}),
            'sub_views': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['resources.View']"})
        }
    }
    
    complete_apps = ['resources']
