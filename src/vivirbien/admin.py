from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    ordering = ('-date_joined',)

# replace user admin with our own version
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

