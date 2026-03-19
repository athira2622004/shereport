from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_insights, name='data_insights'),
    path('incidents/', views.incident_map, name='incident_map'),
]
