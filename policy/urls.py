from django.urls import path
from . import views

urlpatterns = [
    path('', views.policy, name='policy'),
    path('rti-resources/', views.rti_resources, name='rti_resources'),
]
