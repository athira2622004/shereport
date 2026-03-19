from django.contrib import admin
from .models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ['crime_type', 'district', 'incident_date', 'reported_to_police',
                    'needs_legal_help', 'is_anonymous', 'status', 'created_at']
    list_filter = ['crime_type', 'district', 'status',
                   'is_anonymous', 'reported_to_police', 'needs_legal_help']
    readonly_fields = ['created_at', 'crime_type', 'district', 'incident_date', 'incident_time',
                       'institution', 'reported_to_police', 'needs_legal_help', 'evidence_file',
                       'help_filing_complaint', 'help_legal_support', 'help_court_support',
                       'help_recovery', 'help_safety_planning', 'help_ngo_referral',
                       'help_other', 'help_other_text',
                       'description', 'is_anonymous', 'name', 'contact']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False
