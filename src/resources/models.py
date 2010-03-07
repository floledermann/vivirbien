# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Resource(models.Model):
    
    name = models.CharField(max_length=200)
    shortname = models.SlugField(max_length=100, db_index=True, unique=True, help_text=_('(Will be part of the resources\' URL)'))
    
    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    
    key = models.CharField(max_length=100, db_index=True)
    value = models.TextField()
    
    resource = models.ForeignKey(Resource, related_name='tags')
    
    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def get_tag(self):
        part = self.value.partition(':')
        return self.key + '=' + part[0] + part[1]

tag_comparison_choices = enumerate([
    _('is present'),
    _('equals'),
    _('begins with'),
])

    
class View(models.Model):
    
    name = models.CharField(max_length=200)
    shortname = models.SlugField(max_length=100, db_index=True, unique=True, help_text=_('(Will be part of the resources\' URL)'))

    order_by = models.CharField(max_length=200)
    
    sub_views = models.ManyToManyField('self', related_name='parent_views')
    
    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class TagQuery(models.Model):
    
    boolean = models.IntegerField(choices=enumerate([_('AND'),_('OR')]), default=0)
    exclude = models.BooleanField(default=False)
    
    key = models.CharField(max_length=100, db_index=True)
    comparison = models.IntegerField(choices=tag_comparison_choices)
    value = models.CharField(max_length=100, blank=True, null=True)
    
    order = models.IntegerField(default=0)
    
    view = models.ForeignKey(View, related_name='queries')

    class Meta:
        ordering = ['order']
    
