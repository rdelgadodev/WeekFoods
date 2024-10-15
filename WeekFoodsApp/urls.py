from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='Home'),

    path('quienes_somos/', views.quienes_somos, name='Quienes somos'),

    path('como_trabajamos/', views.como_trabajamos, name='Como trabajamos'),

    path('home_usuario/', views.home_usuario, name='Home Usuario'),
]