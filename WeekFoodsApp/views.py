from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from .models import UserWeekfoods
import requests


def home(request):
    return render(request, 'WeekfoodsApp/home.html')


def quienes_somos(request):
    return render(request, 'WeekfoodsApp/quienes_somos.html')


def como_trabajamos(request):
    return render(request, 'WeekfoodsApp/como_trabajamos.html')


@login_required
def home_usuario(request):

    # En esta página inicial, vamos a sugerir al usuario 3 recetas al azar.
    # Obtenemos las recetas que el usuario tiene almacenadas en su cuenta.

    user_name = request.user  # Consultamos que usuario esta ahora activo en la web
    # almacenamos todos los datos de ese usuario
    user_recipes = UserWeekfoods.objects.get(user=user_name)
    # Almacenamos todas las recetas de las que dispone y lo ponemos en formato lista para usar posteriormente random.sample.
    recipes = list(user_recipes.recipe.all())

    # Creamos una lista donde almacenaremos 3 recetas que aleatoriamente serán escogidas.
    # Esa lista se pasará como contexto para su visualizacion.
    list_recipes_suggestion = list()

    # Usamos condicional if para ir escogiendo las 3 recetas al azar.
    # Si el lista de recetas es mayor o igual a 3, escogerá 3 al azar, si es menor, pondrá todas las que haya.

    if len(recipes) >= 3:
        list_recipes_suggestion = random.sample(recipes, 3)

    else:
        list_recipes_suggestion = recipes

    return render(request, 'WeekFoodsApp/home_usuario.html', {'list_recipe': list_recipes_suggestion})
