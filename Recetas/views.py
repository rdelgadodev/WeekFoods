from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from WeekFoodsApp.models import UserWeekfoods, Recipe, Ingredient
from django.core.paginator import Paginator
from .forms import RecipeForms, IngredientForms
from django.contrib import messages


@login_required
def recetas(request):

    # Debemos conocer el usuario que se encuentra ahora activo en la web
    # ya que cada uno dispone de un listado de recetas propio
    user_actual = UserWeekfoods.objects.get(user=request.user)

    # Guardamos en una variable todas las recetas de la base de datos.
    recipe_list = user_actual.recipe.all()

# ----------------------------------------------------------------------------------------------------------- #

    # Código para hacer uso de la paginacion de Django:

    # Obtener del url la página en la que nos encontramos actualmente.
    actual_page = request.GET.get('page') or 1

    # Decidimos cuantas receta por página queremos.
    paginator = Paginator(recipe_list, 5)

    # Para enviar al template las recetas que pertenecen a la página
    recipes = paginator.get_page(actual_page)

    # Casteamos el valor de 'actual_page' para que nos devuelva un valor entero, ya que puede ser un string
    current_page = int(actual_page)

    # Buscamos el número de páginas que tenemos para poder iterar con ella
    pages = range(1, recipes.paginator.num_pages + 1)
    
    return render(request, 'Recetas/recetas.html', {'recipes': recipes,
                                                    'pages': pages,
                                                    'current_page': current_page})

# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

@login_required
def eliminar_receta(request, recipe_id):

    # Debemos conocer el usuario que se encuentra ahora activo en la web
    # ya que cada uno dispone de un listado de recetas propio
    user_actual = UserWeekfoods.objects.get(user=request.user)

    # Eliminamos la receta indicada por el usuario
    user_actual.recipe.remove(recipe_id)

    return redirect('Recetas')

# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

@login_required
def ver_receta(request, recipe_id):

    # Pasamos como parametros al template los datos de la receta seleccionada por el usuario.
    # Almacenamos en una variable todos los datos y en otro los ingredientes.
    recipe_select = Recipe.objects.get(id=recipe_id)
    ingredient_recipe_select = recipe_select.ingredients.all()

    total_price = 0

    for ing in ingredient_recipe_select:
        total_price += ing.price

    return render(request, 'Recetas/ver_receta.html', {'recipe_select' : recipe_select,
                                                       'ingredient_recipe_select' : ingredient_recipe_select,
                                                       'total_price' : round(total_price, 2)})

# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #


@login_required
def compartir_receta(request, recipe_id):

    share_recipe = Recipe.objects.get(id=recipe_id)

    total_user = UserWeekfoods.objects.all()
    for u in total_user:
        u.recipe.add(share_recipe)

    return redirect('/recetas/?valido')

# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

@login_required
def crear_receta(request):
    
    # Guardamos en una variable el formulario de receta creado en el archivo forms.py
    form_recipe = RecipeForms() 

    # Comprobamos si se ha rellenado el formulario y enviado datos
    if request.method == 'POST':
        recipe_form = RecipeForms(request.POST) # Recogemos los datos introducidos

    # Debemos comprobar si el formulario es válido. 
    # En caso que los datos sean correctos los almacenamos en variables.
    
        if recipe_form.is_valid:
            name = request.POST.get('name')
            elaboration = request.POST.get('elaboration')
            eating = request.POST.get('when_you_eat')
            calories = request.POST.get('calories')
            ingredients = request.POST.getlist('ingredients')

            # Antes de guardar la nueva receta comprobamos la variable "ingredients" no esta vacía.
            if ingredients:
            

                # Creamos un objeto de la clase Recipe para que se guarde en la base de datos.
                new_recipe = Recipe(name = name.capitalize(), 
                                    elaboration = elaboration,
                                    when_you_eat = eating,
                                    calories = calories)
                new_recipe.save()
                new_recipe.ingredients.set(ingredients)

                # Se añade esta receta al usuario.
                user_actual = UserWeekfoods.objects.get(user=request.user)
                user_actual.recipe.add(new_recipe)


                # Indicar al usuario que se ha guardado correctamente la receta.
                return redirect ('/recetas/crear_receta/?valido')

            else:
                messages.warning(request, 'Debe seleccionar los ingredientes')
                
   

    return render(request, 'Recetas/crear_receta.html', {'form_recipe':form_recipe})

# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

@login_required
def agregar_ingrediente(request):

    # Guardamos en una variable el formulario de ingrediente creado en el archivo forms.py
    form_ingredient = IngredientForms()

    if request.method == 'POST':
        form_ingredient = IngredientForms() # Recogemos los datos introducidos

        if form_ingredient.is_valid:
            name = request.POST.get('name_ingredient')
            type_food = request.POST.get('type_food')
            price = request.POST.get('price')

            # Comprobamos que el ingrediente no exista en la base de datos:
            if Ingredient.objects.filter(name_ingredient__icontains = name):
                messages.warning(request, 'Este ingrediente ya esta creado. Por favor, vuelva a la receta y filtre su búsqueda')
                

            else:

                # Creamos un nuevo ingrediente con los datos facilitados por el usuario
                new_ingredient = Ingredient.objects.create(name_ingredient = name.capitalize(), type_food = type_food, price = price)

                # Indicar al usuario que se ha guardado correctamente.
                return redirect('/recetas/agregar_ingrediente/?valido')

        
    
    return render(request, 'Recetas/agregar_ingrediente.html', {'form_ingredient':form_ingredient})
    
