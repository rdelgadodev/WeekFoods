from django.shortcuts import render, redirect, HttpResponse
from WeekFoodsApp.models import Recipe, UserWeekfoods
from .models import WeeklyMenu
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required


@login_required
def menu_semanal(request):

    # Se va a elaborar un menú semanal para el usuario. Estas son las opciones que ofrecemos:
    # Opcion 1. Que el usuario escoja las recetas que quiera de toda la semana y guarde ese menu.

    # Opción 2.- Que a través de los filtro de los que dispone, le ofrecemos un menu semanal completo.

    # Opción 3.- Una vez usado los filtros, tiene la opcion de poder eliminar una o varias recetas
    # y escoger otra en su lugar.

    # Opción 4. Conocer cual es el coste de elaborar ese menu semanal escogido u ofrecido.

    # ----------------------------------------------------------------------------------------------------------- #
    # ----------------------------------------------------------------------------------------------------------- #

    # OPCION 1.

    # Cada usuario dispone de su propio listado de recetas.
    # Debemos almacenar en una variable el objeto usuario para conocer su listado.
    user_active = UserWeekfoods.objects.get(user=request.user)

    # Existen dos posibilidades:
    # Posibilidad 1. El usuario todavía no dispone de un menú semanal guardado en la tabla WeeklyMenu,
    # por lo que debemos ofrecer al usuario un desplegable para que escoja dos recetas para cada dia (comida y cena).

    # Posibilidad 2. El usuario ya tiene un menu semanal guardado y debemos ofrecerselo por pantalla y
    # que pueda cambiar las recetas que crea oportunas.

    # POSIBILIDAD 1.
    # Debemos ofrecer al usuario la posibilidad de escoger para cada día (comida y cena) la receta que quiere.
    # Tenemos que pasar por contexto 2 listados uno para las recetas de comidas y otro de cenas.
    recetas_dia = user_active.recipe.filter(when_you_eat='Comida')
    recetas_noche = user_active.recipe.filter(when_you_eat='Cena')

    # POSIBILIDAD 2.
    # pasaremos por contexto los valores de la tabla WeeklyMenu que serán las recetas de la semana
    # que se mostrarán por pantalla. Ordenamos por id para evitar desorden
    recetas = WeeklyMenu.objects.filter(
        user_active=user_active).order_by('id')


# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

    # OPCIÓN 2. Uso del filtro.

    # Creamos 5 funciones para cuando se clicle sobre la opción filtrar:
        # select_dinner
        # select_supper
        # check_calories
        # check_price
        # use_filter

    # Función para escoger un plato para la comida.
    def select_dinner(user_active):

        # Almacenamos todas la recetas filtrando por comidas
        all_recipes_dinner = user_active.recipe.filter(when_you_eat='Comida')

        # Escogemos una receta aleatoria para comer
        random_recipe_dinner = random.choice(all_recipes_dinner)

        return random_recipe_dinner

    # Función para escoger una receta para la cena.
    def select_supper(user_active):

        # Almacenamos todas la recetas filtrando por cena
        all_recipes_supper = user_active.recipe.filter(when_you_eat='Cena')

        # Escogemos una receta aleatoria para cenar
        random_recipe_supper = random.choice(all_recipes_supper)

        return random_recipe_supper

    # Función para comprobar que las calorias diarias indicadas por el usuario no se exceden.
    def check_calories(max_calories_diary, random_recipe_dinner, random_recipe_supper):

        # Si el resultado de restar al máximo de calorias indicado por el usuario
        # las calorias de las recetas es mayor o igual a 0,
        # cumple el requisito de las calorias máximas.
        if max_calories_diary - (random_recipe_dinner.calories + random_recipe_supper.calories) >= 0:
            return True

    # Función para comprobar que el presupuesto diario indicado por el usuario no se exceda.
    def check_price(max_money, random_recipe_dinner, random_recipe_supper):

        # Debemos ir sumando el precio de cada uno de los ingredientes de la receta escogida:
        total_price = 0

        # Creamos variables donde se almacenan todos los ingredientes de la receta escogida aleatoriamente.
        ing_dinner = random_recipe_dinner.ingredients.all()
        ing_supper = random_recipe_supper.ingredients.all()

        # Recorremos los objetos ingredientes para hallar los precios de cada uno.
        for p in ing_dinner:
            total_price += p.price
        for p in ing_supper:
            total_price += p.price

        # Si el resultado de restar el máximo de gasto por el precio de la receta es mayor o igual a 0,
        # cumple el requisito del gasto máximo.
        if max_money >= total_price:
            return True

    # Función para usar la opcion filtro cuando el usuario lo requiera.
    def use_filter(user_active, max_calories_diary, max_money):

        # Creamos una lista donde almacenamos todas las recetas que mostraremos por pantalla.
        showlist_recipes = list()

        # Debemos seleccionar 10 recetas para toda la semana.
        while len(showlist_recipes) < 10:

            # Debemos seleccionar 2 recetas diarias (comida y cena).
            # Llamamos a las funciones.
            recipe_dinner = select_dinner(user_active)
            recipe_supper = select_supper(user_active)

            # Llamamos a las funciones que verifican que las recetas escogidas cumplen con los requisitos de calorias y presupuesto.
            # Solo se llamarán a esas funciones si el usuario ha introducidos datos.
            # Para poder llamar a dicha funcion, primero debemos comprobar que no se han escogido con anterioridad estas recetas.
            if recipe_dinner not in showlist_recipes and recipe_supper not in showlist_recipes:

                if max_calories_diary > 0:
                    verify_calories = check_calories(
                        max_calories_diary, recipe_dinner, recipe_supper)
                elif max_calories_diary == 0:
                    verify_calories = True

                if max_money > 0:
                    verify_price = check_price(
                        max_money, recipe_dinner, recipe_supper)
                elif max_money == 0:
                    verify_price = True

                if verify_calories and verify_price:
                    showlist_recipes.append(recipe_dinner)
                    showlist_recipes.append(recipe_supper)

        return showlist_recipes


# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

    # Comprobamos si se ha hecho uso de algún input.
    if request.method == 'POST':

        # Input filtro
        if request.POST.get('filtro'):

            # Al pulsar en filtrar debemos facilitar al usuario el menú semanal.
            # Actualmente las recetas de este menú se deberían encontrar en la tabla WeeklyMenu.
            # Pueden ocurrir dos cosas:
                # 1.- La tabla se encuentre vacía porque es la primera vez que se hace uso del filtro o se ha eliminado todo.
                # 2.- La tabla contiene recetas de un menú semanal ofrecido anteriormente.

            # Debemos comprobar que se han introducido datos correctos.
            # Primer paso es almacenar en dos variables las calorias y gasto máximo indicado por el usuario.
            # Deberemos hacer uso de un condicion en caso que el usuario no haya indicado ninguna cantidad.
            # Se indicará valor 0 en ese caso.

            max_calories_diary = (request.POST.get('calorias'))

            max_money = (request.POST.get('gasto'))

            if not max_calories_diary:
                
                max_calories_diary = 0

            if not max_money:
                max_money = 0

            # Saldrá mansaje de error en caso que el usuario haya introducido un número negativo.
            if int(max_calories_diary) < 0 or int(max_money) < 0:
                messages.warning(request, 'Por favor, introduzca un valor dentro del rango indicado o deje en blanco')
            # Saldrá mansaje de error en caso que el usuario introduzca valores por debajo de los exigidos.
            elif (int(max_calories_diary) < 1600 and int(max_calories_diary) > 0) or (int(max_money) < 10 and int(max_money) > 0):
                messages.warning(request, 'Por favor, introduzca un valor dentro del rango indicado o dejelo en blanco')
            else:

                # Llamamos a la función creada anteriormente que nos devuelve un listado de recetas.
                showlist_recipes = use_filter(user_active, int(max_calories_diary), int(max_money))

                # En el supuesto 2, tenemos que borrar los datos que contiene la tabla WeeklyMenu.
                recetas.delete()

                # Creamos tantos objetos de la clase WeeklyMenu como recetas existen en la lista anterior.
                # Estos objetos se visualizaran en el template.
                for recipe in showlist_recipes:
                    WeeklyMenu.objects.create(
                        user_active=user_active, recipe_sug=recipe)

            return render(request, 'MenuSemanal/menu_semanal.html', {'recetas': recetas,
                                                                     'recetas_dia': recetas_dia,
                                                                     'recetas_noche': recetas_noche,})

# ----------------------------------------------------------------------------------------------------------- #

        # Input guardar.
        if request.POST.get('guardar'):

            # En este punto existen dos opciones:
                # Opción A. Ha seleccionado todas las recetas del menú.
                # Opción B. Ha modificado solo algunas de las recetas tras haber usado la opción filtro.

            # Sea cual sea la opción creamos una lista donde almacenamos el valor de cada select
            # para saber la receta seleccionada para que forme parte del menu semanal.

            recipes_select = [request.POST.get('recipe_dinner_monday'),
                              request.POST.get('recipe_supper_monday'),
                              request.POST.get('recipe_dinner_tuesday'),
                              request.POST.get('recipe_supper_tuesday'),
                              request.POST.get('recipe_dinner_wednesday'),
                              request.POST.get('recipe_supper_wednesday'),
                              request.POST.get('recipe_dinner_thursday'),
                              request.POST.get('recipe_supper_thursday'),
                              request.POST.get('recipe_dinner_friday'),
                              request.POST.get('recipe_supper_friday')]

            # En caso de que nos encontremos en la opción A, el valor de recetas esta vacío,
            # ya que no existen recetas guardadas en la tabla WeeklyMenu.
            # Se creará tantos objetos de la clase WeeklyMenu como recetas existen en la lista anterior.
            # Estos objetos se visualizaran en el template.
            if not recetas:

                for rec in recipes_select:
                    recipe = Recipe.objects.get(name=rec)
                    WeeklyMenu.objects.create(
                        user_active=user_active, recipe_sug=recipe)

            else:

                # recorremos la lista para encontrar aquellas recetas que el usuario quiere modificar y su posición.
                # de esta manera nos permitirá modificar la base de datos WeeklyMenu que se mostrará por pantalla
                # una vez el usuario marque la opción guardar.
                for p, select in enumerate(recipes_select):

                    if select is not None:

                        # En la variable 'recetas' creada al inicio del código tenemos almacenado todos los objetos
                        # que existen en la clase WeeklyMenu y que componen el menú semanal.

                        # Dentro de la variable 'recetas' debemos encontrar el objeto que queremos modificar.
                        # Como sabemos la posición ('p') en la que se encuentra dicho objeto,
                        # gracias a recorrer el listado de 'recipe_select',
                        # podemos modificar su valor de recipe_sug.

                        # El nuevo valor debe ser un objeto de la clase Recipe.
                        # Lo encontraremos gracias a que sabemos el nombre de la receta (valor select).

                        recetas[p].recipe_sug = Recipe.objects.get(name=select)
                        recetas[p].save()

            # Actualizamos el valor de recetas tras el cambio y lo ordenamos por id para evitar desorden
            recetas = WeeklyMenu.objects.filter(
                user_active=user_active).order_by('id')
            return render(request, 'MenuSemanal/menu_semanal.html', {'recetas': recetas})

# ----------------------------------------------------------------------------------------------------------- #

        # Input eliminar.
        if request.POST.get('eliminar'):
            recetas.delete()
            return redirect('Menu Semanal')

# ----------------------------------------------------------------------------------------------------------- #

        # OPCIÓN 3.
        # Input cambiar
        if request.POST.get('cambiar'):

            # Creamos una lista donde almacenamos el valor del checkbox de cada receta
            # De esta manera sabremos qué receta se ha clicado o no para poder ofrecer al usuario alternativa.

            check_recipes = [request.POST.get('check_0'),
                             request.POST.get('check_1'),
                             request.POST.get('check_2'),
                             request.POST.get('check_3'),
                             request.POST.get('check_4'),
                             request.POST.get('check_5'),
                             request.POST.get('check_6'),
                             request.POST.get('check_7'),
                             request.POST.get('check_8'),
                             request.POST.get('check_9')]

            return render(request, 'MenuSemanal/menu_semanal.html', {'usu': request.user,
                                                                     'recetas': recetas,
                                                                     'recetas_dia': recetas_dia,
                                                                     'recetas_noche': recetas_noche,
                                                                     'check_recipes': check_recipes})

    else:
        return render(request, 'MenuSemanal/menu_semanal.html', {'recetas': recetas, 'recetas_dia': recetas_dia, 'recetas_noche': recetas_noche})
