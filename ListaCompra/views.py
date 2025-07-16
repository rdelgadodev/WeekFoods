from WeekFoodsApp.models import UserWeekfoods
from MenuSemanal.models import WeeklyMenu
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

"""Vista basada en clases para mostrar la lista de la compra del usuario. El usuario debe estar autenticado."""


class ListaCompraView(LoginRequiredMixin, TemplateView):
    template_name = 'ListaCompra/lista_compra.html'

    # Función para almacenar los ingredientes, sus cantidades y precio de las recetas del usuario.
    def _calculate_shopping_list(self, user_weekfoods):

        # Almacenamos todas las recetas propuestas al usuario para esta semana.
        recetas_semanales = WeeklyMenu.objects.filter(
            user_active=user_weekfoods)
        # Creamos diccionario donde almacenamos en clave:valor {ingrediente:[cantidad, precio]}
        shopping_dict = {}

        # Iteramos sobre cada elemento del menu semanal.
        for menu_item in recetas_semanales:
            # Se verifica que exista recipe_sug
            if menu_item.recipe_sug:
                # Almacenamos todos los ingredientes de la receta actual
                ingredients_in_recipe = menu_item.recipe_sug.ingredients.all()

                # Iteramos sobre cada ingrediente para añadirlo a nuestro diccionario
                for ing in ingredients_in_recipe:
                    # Comprobamos que este ingrediente no este ya en el diccionario:
                    if ing.name_ingredient not in shopping_dict:
                        # Si no esta, asignamos al nombre del ingrediente cantidad 1 y su precio
                        shopping_dict[ing.name_ingredient] = [1, ing.price]
                    else:
                        # Si ya esta repetido, debemos añadir 1 a cantidad
                        shopping_dict[ing.name_ingredient][0] += 1
                        # Recalculamos el precio acumulado para este ingrediente
                        # Se multiplica la cantidad total por el precio unitario y se redondea en 2 decimales.
                        shopping_dict[ing.name_ingredient][1] = round(
                            shopping_dict[ing.name_ingredient][0]*ing.price, 2)

        # Devolvemos el diccionario
        return shopping_dict

    def _calculate_total_shopping_price(self, shopping_list_data):

        # creamos variable inicial con valor total = 0
        total_price = 0

        # Iteramos sobre el diccionario para ir sumando los precios totales
        for price in shopping_list_data.values():
            total_price += price[1]

        # Devolvemos el precio total redondeado
        return round(total_price, 2)

     # Prepara el diccionario que se pasará como contexto al template.

    def get_context_data(self, **kwargs):
        # LLamar al metodo de la superclase TemplateView para obtener el contexto base.
        context = super().get_context_data(**kwargs)

        # Debemos conocer el usuario que se encuentra ahora activo en la web
        # ya que cada uno dispone de un menu semanal propio
        user_actual = UserWeekfoods.objects.get(user=self.request.user)

        # Llamamos al método para conocer la lista de ingredientes y su cantidades y precios
        shopping_dict = self._calculate_shopping_list(user_actual)

        # Ordenamos el diccionario de la lista de la compra
        # Se ordena de mayor cantidad a menor.
        # La función lambda x: x[1][0] accede al primer elemento (cantidad) del valor del diccionario.
        # Como sorted te devuelve una lista ponemos dict al principio
        sorted_shopping_dict = dict(
            sorted(shopping_dict.items(), key=lambda x: x[1][0], reverse=True))

        # LLamamos al método para conocer el precio total de la compra
        total_price = self._calculate_total_shopping_price(shopping_dict)

        # Añadimos estos datos al contexto que se pasará al template.
        context['shopping_dict'] = sorted_shopping_dict
        context['total_price'] = total_price

        return context
