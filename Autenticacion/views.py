from django.shortcuts import render, redirect, HttpResponse
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
        return render(request, 'Registro/registro.html', {'form':form})
        

    def post(self, request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

             # creamos usuario dentro de la base de datos creada en models
            userweekfoods = UserWeekfoods(user=usuario)
            userweekfoods.save()
            userweekfoods.recipe.set(Recipe.objects.all())

            return redirect('Home Usuario')
        
        else:
            if request.POST['password1'] != request.POST['password2']:
                messages.warning(request, "Los dos campos de contraseña no coinciden")
            elif (len(request.POST['password1'])) < 8 or (len(request.POST['password2'])) < 8:
                messages.warning(request, "La contraseña debe tener mínimo 8 carácteres")
            else:
                messages.warning(request, "Usuario ya existe")
            
            return render(request, 'Registro/registro.html', {'form':form})


# Función para cerrar la sesion del usuario
def cerrar_sesion(request):
    logout(request)
    return redirect('Home')


# Función para que el usuario acceda a su perfil. Logearse.
def logear(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
       
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home Usuario')
            else:
                messages.error(request, 'Usuario no válido')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Por favor, vuelva a intentarlo.')
            return redirect('Home')
    
    form = AuthenticationForm()
    return render(request, 'WeekfoodsApp/home.html', {'form':form})

