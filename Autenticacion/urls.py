from django.urls import path

from .views import Registro, cerrar_sesion, logear

urlpatterns = [
    path('', Registro.as_view(), name='Registro'),
    path('cerrar_sesion/', cerrar_sesion, name='Logout'),
    path('logear/', logear, name='Logear'),

]