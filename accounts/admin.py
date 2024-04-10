from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Account
class UserCustomAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'username','last_login','date_joined','is_active']
    list_display_links = ['email', 'first_name','last_name','username']
    readonly_fields = ['last_login','date_joined']
    ordering = ['date_joined']
    list_filter = ()
    fieldsets = ()
    filter_horizontal= ()
    
admin.site.register(Account, UserCustomAdmin)