# coding: utf-8

from django.db import models

class Resource(models.Model):
    
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
