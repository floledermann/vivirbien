from django.contrib import admin
from django.conf import settings

from snippets.models import *

class SnippetAdmin(admin.ModelAdmin):
    if 'tagging' in settings.INSTALLED_APPS:
        list_display = ('__unicode__', 'lang', 'tag_str', 'active', 'date')
        # this will work in 1.3
        #list_filter = ('rel_tags__tag__name', )
    else:
        list_display = ('__unicode__', 'lang', 'active', 'date')

    list_filter = ('lang', 'categories') #, 'parent'
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user

        # always save model! this is where it is done
        obj.save()


admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Category)

