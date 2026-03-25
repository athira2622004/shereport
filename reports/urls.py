from django.urls import path
from . import views

urlpatterns = [
    path('', views.publications, name='publications'),
    path('legalmanualenglish/', views.legal_manual_english,
         name='legal_manual_english'),
    path('legalmanualmalayalm/', views.legal_manual_malayalm,
         name='legal_manual_malayalm')
]
