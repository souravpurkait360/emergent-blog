from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'avatar', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile', {'fields': ('email', 'role')}),
    )
    ordering = ['-date_joined']
