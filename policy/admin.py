
from django.contrib import admin
from .models import PolicyUpdate


@admin.register(PolicyUpdate)
class PolicyUpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['-date']
# Register your models here.
