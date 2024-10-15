from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from WeekFoodsApp.models import UserWeekfoods
from MenuSemanal.models import WeeklyMenu


@login_required
def lista_compra(request):

    # Debemos conocer el usuario que se encuentra ahora activo en la web
    # ya que cada uno dispone de un menu semanal propio
    user_actual = UserWeekfoods.objects.get(user=request.user)

    # Creamos función para guardar en un diccionario 
    # la cantidad y precio de cada ingrediente que compone cada receta de la semana. 
    def dic_ingredient_quantity():

        # Guardamos en una variable todos los objetos de la clase WeeklyMenu, filtrado por el usuario activo
        # de tal manera que podamos obtener los ingredientes y precios.
        recetas = WeeklyMenu.objects.filter(user_active = user_actual)

        # Creamos diccionario donde su clave:valor es nombre_ingrediente:[cantidad, precio]
        shopping_dict = {}
        

        for receta in recetas:
            
            # Guardamos en una variable todos los ingredientes de la receta que estemos comprobando.
            ingred = receta.recipe_sug.ingredients.all()

            # Recorremos cada ingrediente para saber si figura en el diccionario y saber si ya se ha repetido.
            for ing in ingred:
                
                # Si el ingrediente no esta en el diccionario, crea un elemento nuevo dando como valor una lista
                # que contiene la cantidad y el precio
                if ing.name_ingredient not in shopping_dict:
                    shopping_dict[ing.name_ingredient] = [1, ing.price]

                else:
                    shopping_dict[ing.name_ingredient][0] += 1
                    shopping_dict[ing.name_ingredient][1] = round(shopping_dict[ing.name_ingredient][0]*ing.price, 2)
        return shopping_dict

    # Funcion para calcular el precio total de la compra
    def total_price(shopping_dict):

        # Iniciamos variable a 0 donde se irá almecenando el precio total
        price_total = 0

        # Recorremos el diccionario con todos los ingredientes
        # Recorremos la parte valor del diccionario para multiplicar la cantidad de ingrediente por su precio
        for ing in shopping_dict.values():
            for quantity, price in enumerate(ing):

                price_total += quantity*price

        return round(price_total,2)


    # Hacemos uso de las funciones creadas que se pasarán como contexto al template.
    # Ordenamos el diccionario de mayor a menor cantidad de ingredientes necesarios.
    shopping_dict = dic_ingredient_quantity()
    sorted_shopping_dict = dict(sorted(shopping_dict.items(), key=lambda x: x[1], reverse=True))
    
    
    total_price = total_price(shopping_dict)
    
    return render(request, 'ListaCompra/lista_compra.html', {'shopping_dict':sorted_shopping_dict,
                                                             'total_price':total_price})
    
