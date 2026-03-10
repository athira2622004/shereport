from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_support, name='get_support'),
    path('reporting-guidance/', views.reporting_guidance, name='reporting_guidance'),
    path('legal-literacy/', views.legal_literacy, name='legal_literacy'),
    path('referral-information/', views.referral_info, name='referral_info'),
    path('submit-report/', views.submit_report, name='submit_report'),
]
