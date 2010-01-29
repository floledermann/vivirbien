# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    
    name = models.CharField(max_length=200)
    shortname = models.SlugField(db_index=True, unique=True)
    
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
