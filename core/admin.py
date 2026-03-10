from django.contrib import admin
from .models import CrimeStatistic, DistrictData, NewsUpdate

@admin.register(CrimeStatistic)
class CrimeStatisticAdmin(admin.ModelAdmin):
    list_display = ['year', 'total_crimes', 'rape', 'cruelty_by_husband', 'kidnapping']
    list_filter = ['year']
    ordering = ['year']

@admin.register(DistrictData)
class DistrictDataAdmin(admin.ModelAdmin):
    list_display = ['district', 'year', 'total_crimes']
    list_filter = ['year', 'district']
    search_fields = ['district']

@admin.register(NewsUpdate)
class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_published', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
