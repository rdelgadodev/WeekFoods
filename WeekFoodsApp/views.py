from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
import random
from .models import Recipe, UserWeekfoods
import requests
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'WeekfoodsApp/home.html')


def quienes_somos(request):
    return render(request, 'WeekfoodsApp/quienes_somos.html')


def como_trabajamos(request):
    return render(request, 'WeekfoodsApp/como_trabajamos.html')


class HomeUsuarioView(LoginRequiredMixin, ListView):
    # Queremos listar objetos del tipo Recipe
    model: Recipe
    # Plantilla donde se renderiza
    template_name = 'WeekFoodsApp/home_usuario.html'
    # Nombre de la variable que se pasara como contexto a la plantilla
    context_object_name = 'list_recipe'

    # Sobreescribimos este método para definir el QuerySet que se mostrará

    def get_queryset(self):
        # Obtenemos todas las recetas de que disponemos en el modelo Recipe
        all_instance_recipe = Recipe.objects.all()

        # Convertimos el QuerySet en lista para poder usar el random.sample
        recipe_list = list(all_instance_recipe)

        # Seleccionar 3 recetas al azar o todas las disponibles si hay menos de 3.
        # Este bloque maneja el caso en que no haya suficientes recetas en la base de datos.
        if len(recipe_list) >= 3:
            recipe_suggestion = random.sample(recipe_list, 3)
        else:
            recipe_suggestion = recipe_list

        return recipe_suggestion
    
      


