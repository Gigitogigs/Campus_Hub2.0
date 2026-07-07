from django.contrib import admin
from .models import Event, Post

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization__name', 'event_date', 'event_location',)
    search_fields = ('title', 'organization__name', 'event_date',)
    list_filter = ('organization', 'event_date',)
    ordering = ('-event_date',)
    list_per_page = 50

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'user', 'created_at',)
    search_fields = ('title', 'organization__name', 'user__display_name',)
    list_filter = ('organization', 'user', 'created_at',)
    ordering = ('-created_at',)
    list_per_page = 50