from django.contrib import admin

from .models import ExternalModerationRequest


@admin.register(ExternalModerationRequest)
class ExternalModerationRequestAdmin(admin.ModelAdmin):
    list_display = ('requested', 'approved', 'denied', 'timed_out', 'moderator', 'message',)
    list_filter = ('requested', 'approved', 'denied', 'timed_out', 'moderator')
    search_fields = ('message', 'response',)
