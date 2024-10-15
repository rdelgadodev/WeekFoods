from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from .models import UserWeekfoods

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
    
    user_name=request.user # Consultamos que usuario esta ahora activo en la web
    user_recipes = UserWeekfoods.objects.get(user=user_name) # almacenamos todos los datos de ese usuario
    recipes = user_recipes.recipe.all() # Almacenamos todas las recetas de las que dispone.
   
    # Creamos una lista donde almacenaremos 3 recetas que aleatoriamente serán escogidas.
    # Esa lista se pasará como contexto para su visualizacion.
    list_recipes_suggestion = list()

    
    

    # Usamos bucle while para ir escogiendo recetas al azar.
    # Mientras el total del listado no sea 3, seguirá buscando 
    # y se usa condicional para que no aparezcan recetas repetidas.
    while ((len(list_recipes_suggestion)) < 3):
        random_recipe = random.choice(recipes)
        if random_recipe not in list_recipes_suggestion:
            list_recipes_suggestion.append(random_recipe)
        
   
    return render(request, 'WeekFoodsApp/home_usuario.html', {'list_recipe': list_recipes_suggestion})


