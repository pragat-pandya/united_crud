from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    # Handle fieldsets - ensure it's a tuple before concatenation
    _base_fieldsets = BaseUserAdmin.fieldsets or ()
    fieldsets = _base_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'date_of_birth')}),
    )
    
    # Handle add_fieldsets - ensure it's a tuple before concatenation
    _base_add_fieldsets = getattr(BaseUserAdmin, 'add_fieldsets', None) or ()
    add_fieldsets = _base_add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'date_of_birth', 'email')}),
    )
