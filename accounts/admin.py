from django.contrib import admin
from .models import User, UserPublic, UserManager

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('university_email', 'first_name', 'last_name', 'is_active', 'created_at',)
    search_fields = ('university_email', 'first_name', 'last_name',)
    list_filter = ('is_active', 'created_at',)
    ordering = ('-created_at',)
    list_per_page = 50

@admin.register(UserPublic)
class UserPublicAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'university', 'course', 'created_at',)
    search_fields = ('display_name', 'university', 'course',)
    list_filter = ('course', 'university',)
    ordering = ('-created_at',)
    list_per_page = 50
