from django.contrib import admin
from .models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ['crime_type', 'district', 'is_anonymous', 'status', 'created_at']
    list_filter  = ['crime_type', 'district', 'status', 'is_anonymous']
    readonly_fields = ['created_at', 'crime_type', 'district', 'description',
                       'is_anonymous', 'name', 'contact']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False
