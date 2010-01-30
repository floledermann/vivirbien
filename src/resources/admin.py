from django.contrib import admin
from django import forms

from resources.models import *

class TagInline(admin.TabularInline):
    model = Tag
#    exclude = ['creator', ]
    extra = 1
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        
        field = super(TagInline, self).formfield_for_dbfield(db_field, **kwargs)
               
        if db_field.name == 'value':
            field.widget = admin.widgets.AdminTextInputWidget()

        return field


class ResourceAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    prepopulated_fields = {'shortname': ('name',)} 
    save_on_top = True

    fieldsets = (
        (None, {'fields': ('name', )}),
        ('Navigation options', {'fields': ('shortname', ),
                     'classes': ('collapse', )}),
        ('Editing', {'fields': ('creator', ),
                     'classes': ('collapse', )}),
    )
    
admin.site.register(Resource, ResourceAdmin)