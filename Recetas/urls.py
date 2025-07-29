from django.urls import path

from . import views

urlpatterns = [
    path('', views.RecetasListView.as_view(), name='Recetas'),
    path('eliminar/<int:recipe_id>/', views.EliminarRecetaView.as_view(), name='Eliminar'),
    path('ver_receta/<int:pk>/', views.VerRecetaDetail.as_view(), name='Ver Receta'),
    path('crear_receta/', views.CreateRecetaView.as_view(), name='Crear Receta'),
    path('agregar_ingrediente/', views.IngredientCreateView.as_view(), name='Agregar Ingrediente'),
    path('compartir_receta/<int:recipe_id>',
         views.CompartirReceta.as_view(), name='Compartir Receta'),
    path('eliminar/', views.EliminarTodasDeleteView.as_view(), name='Eliminar Todas Recetas')

]
