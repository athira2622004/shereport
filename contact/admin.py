from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'purpose', 'created_at', 'is_read']
    list_filter   = ['purpose', 'is_read']
    search_fields = ['name', 'email', 'organisation']
