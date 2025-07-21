from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from WeekFoodsApp.models import UserWeekfoods, Recipe, Ingredient
from django.core.paginator import Paginator
from .forms import RecipeForms, IngredientForms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, DeleteView, CreateView


class RecetasListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'Recetas/recetas.html'
    context_object_name = 'recipes'
    paginate_by = 5  # Número de recetas por página

    def get_queryset(self):

        # Obtiene el usuario actual y filtra las recetas asociadas a él
        user_actual = UserWeekfoods.objects.get(user=self.request.user)
        queryset = user_actual.recipe.all()
        return queryset

    def get_context_data(self, **kwargs):
        # Llama al método get_context_data de la superclase (ListView)
        context = super().get_context_data(**kwargs)

        # Alias para la lista paginada de recetas, útil si el template espera 'page_object'
        context['page_object'] = context[self.context_object_name]

        # 'paginator' es el objeto Paginator completo
        context['paginator'] = context['page_obj'].paginator

        return context


# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

class EliminarRecetaView(LoginRequiredMixin, View):
    """
    Vista basada en clases para eliminar una receta específica.
    Requiere que el usuario esté autenticado.
    """

    def post(self, request, recipe_id, *args, **kwargs):

        # Obtenemos al usuario actual
        user_actual = UserWeekfoods.objects.get(user=request.user)
        # Obtiene la receta a eliminar
        recipe_to_remove = user_actual.recipe.get(id=recipe_id)
        # Elimina la receta del usuario actual
        user_actual.recipe.remove(recipe_to_remove)
        # Añadimos mensaje de exito al usuario
        messages.success(
            request, f'Receta {recipe_to_remove.name} eliminada con éxito')

        return redirect('Recetas')


# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

    """
    Vista basada en clases para mostrar los detalles de una receta específica.
    Requiere que el usuario esté autenticado.
    """


class VerRecetaDetail(LoginRequiredMixin, DetailView):
    # Define el modelo del cual esta DetailView obtendrá un único objeto.
    model = Recipe
    # Define la plantilla HTML que esta vista renderizará.
    template_name = 'Recetas/ver_receta.html'
    # Define el nombre de la variable de contexto que contendrá el objeto Recipe
    # principal en la plantilla. Así, en el template, será {{ recipe_select }}.
    context_object_name = 'recipe_select'

    """
        Preparamos el diccionario de contexto que se pasará a la plantilla.
        Calcular el precio total de los ingredientes de la receta seleccionada
        y añadir los ingredientes y el precio al contexto.
        """

    def get_context_data(self, **kwargs):
        # Llama al método get_context_data de la superclase (DetailView)
        # para obtener el contexto base que ya proporciona Django.
        # Este contexto ya incluirá 'recipe_select' (el objeto Recipe principal).
        context = super().get_context_data(**kwargs)

        # El objeto Recipe principal ya está disponible como context['recipe_select']
        # De aqui sacaremos todos los ingredientes y el precio total.
        recipe_select = context['recipe_select']

        # Ingredientes
        ingredient_recipe_select = recipe_select.ingredients.all()

        # Calcular precio total
        total_price = 0
        for ing in ingredient_recipe_select:
            total_price += ing.price

         # Añadir los contextos adicionales al diccionario 'context'.
        context['ingredient_recipe_select'] = ingredient_recipe_select
        context['total_price'] = round(total_price, 2)

        return context


class compartirReceta(LoginRequiredMixin, View):
    """
    Vista basada en clases para compartir una receta con todos los usuarios.
    Requiere que el usuario esté autenticado.
    """

    def post(self, request, recipe_id, *args, **kwargs):
        # Obtiene la receta a compartir
        share_recipe = Recipe.objects.get(id=recipe_id)

        # Obtiene todos los usuarios registrados
        total_user = UserWeekfoods.objects.all()
        for u in total_user:
            u.recipe.add(share_recipe)

        messages.success(request, 'Receta compartida con éxito')
    
        return redirect('Recetas')

# @login_required
# def compartir_receta(request, recipe_id):

#     share_recipe = Recipe.objects.get(id=recipe_id)

#     total_user = UserWeekfoods.objects.all()
#     for u in total_user:
#         u.recipe.add(share_recipe)

#     return redirect('/recetas/?valido')

# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #


class CreateRecetaView(LoginRequiredMixin, CreateView):
    """
    Vista basada en clases para crear una nueva receta.
    Requiere que el usuario esté autenticado.
    """
    model = Recipe
    template_name = 'Recetas/crear_receta.html'
    form_class = RecipeForms
    success_url = reverse_lazy('Recetas')

    def form_valid(self, form):
        # Llama al método form_valid de la superclase (CreateView)
        # para procesar el formulario y guardar el objeto Recipe.
        response = super().form_valid(form)

        # Añade la receta recién creada al usuario actual.
        user_actual = UserWeekfoods.objects.get(user=self.request.user)
        user_actual.recipe.add(self.object)

        # Mensaje de éxito
        messages.success(self.request, 'Receta creada con éxito')

        return response


# ----------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------- #

@login_required
def agregar_ingrediente(request):

    # Guardamos en una variable el formulario de ingrediente creado en el archivo forms.py
    form_ingredient = IngredientForms()

    if request.method == 'POST':
        form_ingredient = IngredientForms()  # Recogemos los datos introducidos

        if form_ingredient.is_valid:
            name = request.POST.get('name_ingredient')
            type_food = request.POST.get('type_food')
            price = request.POST.get('price')

            # Comprobamos que el ingrediente no exista en la base de datos:
            if Ingredient.objects.filter(name_ingredient__icontains=name):
                messages.warning(
                    request, 'Este ingrediente ya esta creado. Por favor, vuelva a la receta y filtre su búsqueda')

            else:

                # Creamos un nuevo ingrediente con los datos facilitados por el usuario
                new_ingredient = Ingredient.objects.create(
                    name_ingredient=name.capitalize(), type_food=type_food, price=price)

                # Indicar al usuario que se ha guardado correctamente.
                return redirect('/recetas/agregar_ingrediente/?valido')

    return render(request, 'Recetas/agregar_ingrediente.html', {'form_ingredient': form_ingredient})
