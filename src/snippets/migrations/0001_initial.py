# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('snippets_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.SlugField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal('snippets', ['Category'])

        # Adding model 'Snippet'
        db.create_table('snippets_snippet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('tag_str', self.gf('tagging.fields.TagField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['snippets.Snippet'], null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('snippets', ['Snippet'])

        # Adding unique constraint on 'Snippet', fields ['slug', 'parent']
        db.create_unique('snippets_snippet', ['slug', 'parent_id'])

        # Adding M2M table for field categories on 'Snippet'
        db.create_table('snippets_snippet_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('snippet', models.ForeignKey(orm['snippets.snippet'], null=False)),
            ('category', models.ForeignKey(orm['snippets.category'], null=False))
        ))
        db.create_unique('snippets_snippet_categories', ['snippet_id', 'category_id'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('snippets_category')

        # Deleting model 'Snippet'
        db.delete_table('snippets_snippet')

        # Removing unique constraint on 'Snippet', fields ['slug', 'parent']
        db.delete_unique('snippets_snippet', ['slug', 'parent_id'])

        # Removing M2M table for field categories on 'Snippet'
        db.delete_table('snippets_snippet_categories')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'snippets.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.SlugField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'snippets.snippet': {
            'Meta': {'unique_together': "(('slug', 'parent'),)", 'object_name': 'Snippet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['snippets.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['snippets.Snippet']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tag_str': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'tagging.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'content_type', 'object_id'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['tagging.Tag']"})
        }
    }

    complete_apps = ['snippets']
