from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_insights, name='data_insights'),
]
