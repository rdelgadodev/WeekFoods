from django.shortcuts import render, redirect, HttpResponse
from WeekFoodsApp.models import Recipe, UserWeekfoods
from .models import WeeklyMenu
from django.contrib import messages
import random
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MenuSemanalView(LoginRequiredMixin, TemplateView):

    template_name = 'MenuSemanal/menu_semanal.html'

    def _select_dinner(self, user_active):

        # Almacenamos todas las recetas del usuario filtrado por when_you_eat
        recipe_dinner = user_active.recipe.filter(when_you_eat='Comida')

        if recipe_dinner:
            # Escogemos una receta al azar
            random_recipe_dinner = random.choice(recipe_dinner)
            # Devolvemos esa receta
            return random_recipe_dinner
        else:
            return None

    def _select_supper(self, user_active):

        # Almacenamos todas las recetas del usuario filtrado por when_you_eat
        recipe_supper = user_active.recipe.filter(when_you_eat='Cena')

        # Escogemos una receta al azar
        if recipe_supper:
            random_recipe_supper = random.choice(recipe_supper)
            # Devolvemos esa receta
            return random_recipe_supper
        else:
            return None
    
    def _check_calories(self, max_calories, recipe_dinner, recipe_supper):
        
        #Verificamos que las recetas no estén vacias
        if not recipe_dinner or not recipe_supper:
            return False
        
        
        # Sumamos el total de calorias de ambas recetas seleccionadas al azar
        # Si la suma es mas pequeña que el total de calorias que ha puesto el usuario devuelve True.
        total_calories = recipe_dinner.calories + recipe_supper.calories
        if total_calories <= max_calories:
            return True
        
        return False
    
    def _check_price(self, max_waste, recipe_dinner, recipe_supper):
        
        #Verificamos que las recetas no estén vacias
        if not recipe_dinner or not recipe_supper:
            return False
        
        # Creamos una variable donde almacenaremos el total del coste de las recetas seleccionadas al azar
        total_waste = 0
        
        # Debemos acceder a los ingredientes de cada receta para saber su precio y sumarlo.
        ingredients_dinner = recipe_dinner.ingredients.all()
        ingredients_supper = recipe_supper.ingredients.all()
        
        #Recorremos cada uno de los ingredientes para saber sus precios y sumarlos en total_waste
        for ing in ingredients_dinner:
            total_waste += ing.price
            
        for ing in ingredients_supper:
            total_waste += ing.price
        
        #Comprobamos si supera el mínimo establecido por el usuario.
        if total_waste <= max_waste:
            return True
        
        return False
    

    def _use_filter(self, user_active, max_calories, max_waste):
        
        #Creamos una lista donde almacenaremos todas las recetas que devolveremos
        list_recipes = list()
        
        #Contador con número de intentos para buscar las recetas
        count_try = 0
        
        #El total de recetas deben ser 10, creamos un bucle while para que vaya rellenando la lista hasta que se llegue a ese total.
        while len(list_recipes) < 10:
            
            #Sumamos cada vez que inicia el bucle un intento
            count_try += 1
            
            #Condicional para cuando llegue a 1000 intentos
            if count_try == 1000:
                break
            
            #Generamos una receta para cada momento
            recipe_dinner = self._select_dinner(user_active)
            recipe_supper = self._select_supper(user_active)
            
            #Comprobamos que no esten vacios las recetas
            if not recipe_dinner or not recipe_supper:
                break
            
            #Comprobamos que ambas recetas cumplen con los requisitos que indica el usuario.
            if self._check_calories(max_calories, recipe_dinner, recipe_supper) and self._check_price(max_waste, recipe_dinner, recipe_supper):
                if recipe_dinner not in list_recipes and recipe_supper not in list_recipes:
                    list_recipes.append(recipe_dinner)
                    list_recipes.append(recipe_supper)
                
                
        return list_recipes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtenemos el usuario activo
        user_active = UserWeekfoods.objects.get(user=self.request.user)

        # Obtenemos las recetas de comida y cena del usuario
        recetas_dia = user_active.recipe.filter(when_you_eat='Comida')
        recetas_noche = user_active.recipe.filter(when_you_eat='Cena')
        
        #Debemos comprobar que el usuario tiene almacenados mínimo 5 recetas de cada(comida y cena) para que se pueda generar un menú, hacer uso del filtrado y modficado del menú semanal.
        has_enough_recipes = True
        if recetas_dia.count() < 5 or recetas_noche.count() < 5:
            has_enough_recipes = False
            
        context['minimo'] = has_enough_recipes

        # Obtenemos las recetas del menú semanal del usuario
        recetas = WeeklyMenu.objects.filter(
            user_active=user_active).order_by('id')
        
        context['recetas'] = recetas
        context['recetas_dia'] = recetas_dia
        context['recetas_noche'] = recetas_noche
        
        # Recuperamos el estado de los checkboxes de la sesión. Si no existe, usamos un diccionario vacío.
        context['check_recipes'] = self.request.session.get('check_recipes', {})

        return context

    # Tenemos que manejar 4 posibilidades de envío de información:

    def post(self, request, *args, **kwargs):

        # Almacenamos en una variable el usuario actual
        user_active = UserWeekfoods.objects.get(user=self.request.user)

        # Almecenamos en una variable todas las recetas que tiene la base de datos de WeeklyMenu
        all_recipes_weekly = WeeklyMenu.objects.filter(
            user_active=user_active).order_by('id')

        # Primera opción que el usuario clique en filtrar
        if request.POST.get('filtro'):

            # Capturamos los valores introducidos en los inputs de calorias y precio
            max_calories = int(request.POST.get('calorias', 1600))
            max_waste = int(request.POST.get('gasto', 10))

            # Para poder hacer uso del filtrado, debemos comprobar que las cantidades que se han introducido sean correctas.
            # Iniciamos el True una variable que cambiará a false si los datos introducidos no son los adecuados.
            correct_values = True

            # Comprobamos que se introducen las cantidades correctas antes de continuar, enviando mensajes al usuario
            if max_calories < 1600:
                messages.warning(
                    self.request, 'Las calorias deben ser mayor o igual a 1600')
                correct_values = False
            if max_waste < 10:
                messages.warning(
                    self.request, 'El gasto semanal debe ser superior o igual a 10')
                correct_values = False

            # Si esta todo correcto, procedemos a filtrar las recetas que deben aparecer en el menu.
            if correct_values:

                # Llamamos al metodo _use_filter para modificar el WeeklyMenu del usuario actual
                new_menu = self._use_filter(
                    user_active, max_calories, max_waste)
                
                #Comprobamos que se ha devuelto 10 recetas dentro del menú.
                if len(new_menu) < 10:
                    messages.warning(self.request, 'No se pudo generar un menú semanal completo con los filtros actuales o no hay suficientes combinaciones de recetas. Intente ajustar los filtros o añadir más recetas a su listado')
                    if 'check_recipes' in self.request.session:
                        del self.request.session['check_recipes']
                    return redirect ('Menu Semanal')

                # Eliminamos todos los objetos que actualmente estan en WeeklyMenu del usuario
                all_recipes_weekly.delete()

                # Creamos el nuevo menu, debemos iterar todas las recetas que hemos obtenido del filtrado
                for recipe in new_menu:
                    new_week_menu = WeeklyMenu(
                        user_active=user_active, recipe_sug=recipe)
                    new_week_menu.save()

                messages.success(
                    self.request, 'El menú se ha creado con éxito')
                
                if 'check_recipes' in self.request.session:
                    del self.request.session['check_recipes']

                return redirect('Menu Semanal')

            
        elif request.POST.get('guardar'):
            
            # Creamos una lista donde almacenamos el valor de cada select
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
            
                     
            #Creamos una lista vacía donde almacenaremos las recetas del modelo Recipe que coinciden con las seleccionadas por el usuario.
            list_recipes = list()
            
            #Debemos comprobar uno por uno las respuestas de los request.
            #En caso de haber información se buscará en el modelo Recipe su objeto.
            #En caso que el request haya devuelto None, se dejará la receta existente en el modelo WeeklyMenu
            #Recorremos las recetas seleccionadas
            
            for i, recipe_name_from_post in enumerate(recipes_select):
                print(recipe_name_from_post)
                if recipe_name_from_post is not None:
                    list_recipes.append(Recipe.objects.get(name=recipe_name_from_post))
                else:
                    list_recipes.append((all_recipes_weekly)[i].recipe_sug)
                
            # Eliminamos todos los objetos que actualmente estan en WeeklyMenu del usuario
            all_recipes_weekly.delete()

            # Creamos el nuevo menu, debemos iterar todas las recetas que hemos obtenido del filtrado
            for recipe in list_recipes:
                new_week_menu = WeeklyMenu(
                user_active=user_active, recipe_sug=recipe)
                new_week_menu.save()

            messages.success(
                self.request, 'El menú se ha guardado con éxito')
                
            if 'check_recipes' in self.request.session:
                del self.request.session['check_recipes']

            return redirect('Menu Semanal')
            
        elif request.POST.get('cambiar'):
            check_recipes = {}
            
            for i in range(10):
                if request.POST.get(f'check_{i}') == 'on':
                    check_recipes[str(i)] = 'on'
            
            self.request.session['check_recipes'] = check_recipes
            
            return redirect ('Menu Semanal')
                    
            
            
        elif request.POST.get('eliminar'):
            
            #Procedemos a eliminar las recetas dentro del modelo WeeklyMenu del usuario activo.
            all_recipes_weekly.delete()
            
            #Enviamos mensaje de exito
            messages.success(self.request, 'Menú eliminado con éxito')
            
            #Eliminamos los estados de los checkbox
            if 'check_recipes' in self.request.session:
                del self.request.session['check_recipes']
            
            return redirect('Menu Semanal')
            
        return redirect('Menu Semanal')


