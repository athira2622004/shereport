from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('what-is-she-report/', views.what_is_she_report,
         name='what_is_she_report'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
]
