from django.contrib import admin

from resources.models import *

class TagInline(admin.TabularInline):
    model = Tag
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
    list_filter = ['creation_date', 'creator',]
    #date_hierarchy = 'creation_date'

    fieldsets = (
        (None, {'fields': ('name', )}),
        ('Navigation options', {'fields': ('shortname', ),
                     'classes': ('collapse', )}),
        ('Editing', {'fields': ('creator', ),
                     'classes': ('collapse', )}),
    )

class TagQueryInline(admin.TabularInline):
    
    model = TagQuery
    extra = 1


class ViewAdmin(admin.ModelAdmin):
    inlines = [TagQueryInline]
    prepopulated_fields = {'shortname': ('name',)} 
    save_on_top = True


admin.site.register(Resource, ResourceAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Icon)

