from django.urls import path
from . import views

urlpatterns = [
    path('',                      views.lawyer_list,    name='lawyer_list'),
    path('connect/<int:pk>/',     views.connect_lawyer, name='connect_lawyer'),
    path('register/',             views.register_lawyer, name='register_lawyer'),
]
