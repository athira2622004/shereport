from django.contrib import admin
from .models import LawyerVolunteer, LawyerConnectionRequest, StudentVolunteer, StudentConnectionRequest


@admin.register(LawyerVolunteer)
class LawyerVolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'district',
                    'pro_bono', 'reduced_cost', 'is_approved', 'registered_at']
    list_filter = ['specialization', 'district',
                   'is_approved', 'pro_bono', 'reduced_cost']
    search_fields = ['name', 'email', 'bar_council_no']
    list_editable = ['is_approved']
    ordering = ['-registered_at']
    readonly_fields = ['registered_at']


@admin.register(StudentVolunteer)
class StudentVolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'year_of_study', 'district',
                    'is_supervised', 'is_approved', 'registered_at']
    list_filter = ['year_of_study', 'district', 'is_approved', 'is_supervised']
    search_fields = ['name', 'email', 'college']
    list_editable = ['is_approved']
    ordering = ['-registered_at']
    readonly_fields = ['registered_at']


@admin.register(LawyerConnectionRequest)
class LawyerConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['lawyer', 'survivor_name',
                    'is_anonymous', 'status', 'requested_at']
    list_filter = ['status', 'is_anonymous']
    list_editable = ['status']
    readonly_fields = ['requested_at', 'lawyer',
                       'survivor_name', 'contact', 'message', 'is_anonymous']
    ordering = ['-requested_at']


@admin.register(StudentConnectionRequest)
class StudentConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'survivor_name',
                    'is_anonymous', 'status', 'requested_at']
    list_filter = ['status', 'is_anonymous']
    list_editable = ['status']
    readonly_fields = ['requested_at', 'student',
                       'survivor_name', 'contact', 'message', 'is_anonymous']
    ordering = ['-requested_at']
