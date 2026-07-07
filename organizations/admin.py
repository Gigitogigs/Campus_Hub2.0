from django.contrib import admin
from .models import University, Organization, OrganizationMember

# Register your models here.
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name','is_active', 'created_at',)
    search_fields = ('name', 'short_name', 'email_domain',)
    list_filter = ('email_domain',)
    ordering = ('-created_at',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'organization_type', 'category',)
    search_fields = ('name',)
    list_filter = ('university', 'category', 'organization_type',)
    ordering = ('-university',)

@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'is_creator',)
    list_filter = ('organization', 'role', 'is_creator',)
    search_fields = ('user__display_name', 'organization__name',)
    ordering = ('-created_at',)