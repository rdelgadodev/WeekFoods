from django.urls import path

from . import views

urlpatterns = [
    path('', views.recetas, name='Recetas'),
    path('eliminar/<int:recipe_id>/', views.eliminar_receta, name='Eliminar'),
    path('ver_receta/<int:recipe_id>/', views.ver_receta, name='Ver Receta'),
    path('crear_receta/', views.crear_receta, name='Crear Receta'),
    path('agregar_ingrediente/', views.agregar_ingrediente, name='Agregar Ingrediente'),
    path('compartir_receta/<int:recipe_id>', views.compartir_receta, name='Compartir Receta'),

]