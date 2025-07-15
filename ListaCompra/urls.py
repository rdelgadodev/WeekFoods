from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListaCompraView.as_view(), name='Lista Compra'),

]
