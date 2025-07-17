from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecetasListView.as_view(), name='Recetas'),
    path('eliminar/<int:recipe_id>/', views.EliminarRecetaView.as_view(), name='Eliminar'),
    path('ver_receta/<int:pk>/', views.VerRecetaDetail.as_view(), name='Ver Receta'),
    path('crear_receta/', views.crear_receta, name='Crear Receta'),
    path('agregar_ingrediente/', views.agregar_ingrediente,
         name='Agregar Ingrediente'),
    path('compartir_receta/<int:recipe_id>',
         views.compartir_receta, name='Compartir Receta'),

]
