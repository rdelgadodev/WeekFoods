from django.urls import path

from . import views

urlpatterns = [
    path('', views.MenuSemanalView.as_view(), name='Menu Semanal'),
]