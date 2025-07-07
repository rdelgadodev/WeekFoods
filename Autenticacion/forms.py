from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # Personalizamos los campos a mostrar en el formulario

    # email
    email = forms.EmailField(
        # Etiqueta que se muestra en el formulario HTML
        label='Email',
        # Controlar como se ve y se comportan este campo
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'ejemplo@dominio.com', 'autocomplete': 'email'}),
        max_length=64,
        help_text='Introduce una dirección de correo válida'
    )

    # password1
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres', 'autocomplete': 'new-password'
        })
    )

    # password2
    password2 = forms.CharField(
        label='Repita contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Repita contraseña', 'autocomplete': 'new-password'
        })
    )

    # username
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Indique nombre de usuario', 'autocomplete': 'username'
        })
    )

    # firstname
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
                               'class': 'form-control', 'placeholder': 'Indique su nombre', 'autocomplete': 'firstName'})
    )

    # secondname
    last_name = forms.CharField(
        label='Apellido',
        widget=forms.TextInput(attrs={
                               'class': 'form-control', 'placeholder': 'Indique su apellido', 'autocomplete': 'lastName'})
    )

    class Meta(UserCreationForm.Meta):

        # Especificamos el modelo al que este formulario está asociado
        model = User

        # Definimos qué campos queremos que aparezcan en el formulario.
        fields = UserCreationForm.Meta.fields + ('email', 'first_name',
                                                 'last_name')
