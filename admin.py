from django.contrib import admin

from .models import ExternalModerationRequest, ModerationDecision, Moderator

class ModerationDecisionInline(admin.TabularInline):
    model = ModerationDecision

    fields = ['decision_maker', 'approved', 'when',]
    readonly_fields = ['approved', 'when', 'decision_maker']

    def has_add_permission(self, request, obj=None): # pylint: disable=arguments-differ,unused-argument
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ExternalModerationRequest)
class ExternalModerationRequestAdmin(admin.ModelAdmin):
    list_display = ('requested', 'approved', 'denied', 'timed_out', 'message',)
    list_filter = ('requested', 'approved', 'denied', 'timed_out',)
    search_fields = ('message', 'response',)

    inlines = [
        ModerationDecisionInline,
    ]

@admin.register(ModerationDecision)
class ModerationDecisionAdmin(admin.ModelAdmin):
    list_display = ('request', 'approved', 'when', 'decision_maker',)
    list_filter = ('approved', 'when', 'decision_maker',)
    search_fields = ('decision_maker', 'metadata',)

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('moderator_id', 'active',)
    list_filter = ('active',)
    search_fields = ('moderator_id', 'moderator_for', 'metadata',)
