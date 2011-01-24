# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from datetime import datetime

class Resource(models.Model):
    
    name = models.CharField(max_length=200)
    shortname = models.SlugField(max_length=200, db_index=True, unique=True, help_text=_('(Will be part of the resources\' URL)'))

    featured = models.BooleanField(default=False)
    protected = models.BooleanField(default=False, help_text=_('(Hidden from anonymous users)'))
    
    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    start_date = models.DateTimeField(null=True, blank=True, help_text=_('Format: yyyy-mm-dd hh:mm (time is optional)'))
    end_date = models.DateTimeField(null=True, blank=True, help_text=_('Format: yyyy-mm-dd hh:mm (time is optional)'))
    
    class Meta:
        ordering = ['name']
        permissions = (
            ('feature_resource', "Mark resource as featured"),
        )

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    
    # use validators in django 1.2 to limit characters
    key = models.CharField(max_length=100, db_index=True)
    value = models.TextField(db_index=True)
    
    resource = models.ForeignKey(Resource, related_name='tags')
    
    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creation_date']
        permissions = (
            ('batch_rename_tags', "Batch rename tags"),
        )
    
    def get_tag(self):
        part = self.value.partition(':')
        return self.key + '=' + part[0] + part[1]

    
class View(models.Model):
    
    name = models.CharField(max_length=200)
    shortname = models.SlugField(max_length=100, db_index=True, unique=True, help_text=_('(Will be part of the views\' URL)'))

    featured = models.BooleanField(default=False)
    protected = models.BooleanField(default=False, help_text=_('(Hidden from anonymous users)'))

    order_by = models.CharField(max_length=200, null=True, blank=True)
    
    sub_views = models.ManyToManyField('self', related_name='parent_views', null=True, blank=True)
    
    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    include_past = models.BooleanField(default=False)
    include_current  = models.BooleanField(default=True)
    include_upcoming = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        permissions = (
            ('feature_view', "Mark view as featured"),
        )

    def __unicode__(self):
        return self.name

#    def _get_resources(self):
#        qs = Resource.objects.all()
#        for query in self.queries.all():
#            qs = query.apply(qs)
#            
#        return qs

    def get_resources(self):
        qs = Resource.objects.all()
        if not self.include_past:
            qs = qs.exclude(end_date__lt=datetime.now())
        if not self.include_upcoming:
            qs = qs.exclude(start_date__gt=datetime.now())
        q = None
        for query in self.queries.all():
            if query.boolean == 0: #AND
                if q:
                    qs = qs.filter(q)
                q = query.get_q()
            else:
                q = q and q | query.get_q() or query.get_q()

        if q:
            qs = qs.filter(q)
        
        return qs.distinct()

    def get_description(self):
        def desc_f(i, query):
            if i==0:
                return query.get_description()
            return string_concat(' <em>', query.get_boolean_str(), '</em> ', query.get_description())
        
        desc = [desc_f(index, query) for index, query in enumerate(self.queries.all())]
        if len(desc):
            return string_concat(*desc)
        else:
            return _('All tags')
        
_tag_comparison_choices = [
    (0, _('is present')),
    (1, '='),
    (2, _('begins with')),
]

_tag_boolean_choices = [
    (0, _('and')),
    (1, _('or')),
]

class TagQuery(models.Model):
    
    boolean = models.IntegerField(choices=_tag_boolean_choices, default=1)
    exclude = models.BooleanField(default=False)
    
    key = models.CharField(max_length=100, db_index=True)
    comparison = models.IntegerField(choices=_tag_comparison_choices)
    value = models.CharField(max_length=100, blank=True, null=True)
    
    order = models.IntegerField(default=0)

    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    
    view = models.ForeignKey(View, related_name='queries')

    class Meta:
        ordering = ['order','creation_date']
    
    def get_q(self):
        from django.db.models import Q
        q = {
             0: Q(tags__key=self.key),
             1: Q(tags__key=self.key, tags__value=self.value), #str(self.value)),
             2: Q(tags__key=self.key, tags__value__startswith=self.value), #str(self.value)),
        }[self.comparison]
        
        if self.exclude:
            q = ~q
        return q
    
    def get_description(self):
        return string_concat(self.key, ' <em>', _tag_comparison_choices[self.comparison][1], '</em> ', self.value)
    
    def get_boolean_str(self):
        return _tag_boolean_choices[self.boolean][1]

_icon_choices = [
    ('default',_('Default Icon')),
    ('red', _('Red'))
]

class Icon(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='uploads/icons/', help_text='Should be of square proportions. Will be resized to 20x20 pixels.')

    creator = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class TagMapping(models.Model):
    
    key = models.CharField(max_length=100, db_index=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    show_in_list = models.BooleanField(default=False)
    icon = models.ForeignKey(Icon, blank=True, null=True)
    
    subicon = models.BooleanField(default=False, verbose_name=_('Subicon only'))
    
    order = models.IntegerField(default=0)

    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
       
    view = models.ForeignKey(View, related_name='mappings')

    class Meta:
        ordering = ['order','creation_date']


from transmeta import TransMeta

class Area(models.Model):   
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100)
    # for now just store a string with the bounds
    # TODO look into geodjango    
    bounds = models.CharField(max_length=255)

    class Meta:
        translate = ('name', )

    def __unicode__(self):
        return self.name

    def delete(self):
        self.context_set.clear()
        super(Area, self).delete()


class Context(models.Model): 
   
    area = models.ForeignKey(Area, null=True, blank=True, verbose_name=_('Area'))

    def delete(self):
        self.user_profile_set.clear()
        super(Context, self).delete()

    def to_json(self):
        if self.area:
            return "{area:[%s]}" % self.area.bounds        
        return "{}"


class ResourceTemplate(models.Model):
    __metaclass__ = TransMeta
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    shortname = models.SlugField(max_length=100, db_index=True, unique=True, help_text=_('(Will be part of the template\'s URL)'))
    description = models.TextField(blank=True)

    featured = models.BooleanField(default=False)

    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        translate = ('name', 'description', )


class TagTemplateGroup(models.Model):
    __metaclass__ = TransMeta
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    template = models.ForeignKey(ResourceTemplate, related_name='tag_groups')
    order = models.IntegerField(default=0)

    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        translate = ('name', )


class TagTemplate(models.Model):
    __metaclass__ = TransMeta
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    key = models.CharField(max_length=100)
    value = models.TextField(blank=True)

    template = models.ForeignKey(ResourceTemplate, related_name='tags')
    group = models.ForeignKey(TagTemplateGroup, related_name='tags')
    order = models.IntegerField(default=0)

    creator = models.ForeignKey(User, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        translate = ('name', )


class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True, related_name='resources_profile')
    context = models.ForeignKey(Context, null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username


def user_post_save(sender, instance, created, **kwargs):
    if created:    
        UserProfile.objects.get_or_create(user=instance)
  
models.signals.post_save.connect(user_post_save, sender=User)


