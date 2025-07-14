from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from WeekFoodsApp.models import UserWeekfoods, Recipe


# Creamos una clase registro donde tendrá dos funciones:
# Funcion get para enviar el formulario de registro al template
# Función post para recoger los datos del nuevo usuario y se registre en la tabla usuarios
# además de asignar todas las recetas existentes a ese usuario.
class Registro(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'Registro/registro.html', {'form': form})

    def post(self, request):
        # Crea una instancia del formulario
        form = RegisterForm(request.POST)

        # Verificar si los datos son validos
        if form.is_valid():

            # Guardamos el usuario
            usuario = form.save()

            # Logea al usuario
            login(request, usuario)

            # creamos usuario dentro de la base de datos creada en models y le asignamos todas las recetas
            userweekfoods = UserWeekfoods(user=usuario)
            userweekfoods.save()
            userweekfoods.recipe.set(Recipe.objects.all())

            # Redirige a la pagina de home del usuario logeado
            return redirect('Home Usuario')

        else:
            # El objeto 'form' ya contiene todos los errores de validación en 'form.errors'.
            # Estos errores se mostrarán automáticamente en la plantilla HTML
            messages.error(
                request, "Hubo errores en el formulario. Por favor, revisa los campos marcados.")

            return render(request, 'Registro/registro.html', {'form': form})


# Función para cerrar la sesion del usuario
def cerrar_sesion(request):
    logout(request)
    return redirect('Home')


# Función para que el usuario acceda a su perfil. Logearse.
def logear(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user_valid = form.get_user()  # Obtienes al usuario
            return redirect('Home Usuario')

        else:
            # Si existen errores, pasaran a traves de form.errors.
            return render(request, 'WeekfoodsApp/home.html', {'form': form})

    form = AuthenticationForm()
    return render(request, 'WeekfoodsApp/home.html', {'form': form})
