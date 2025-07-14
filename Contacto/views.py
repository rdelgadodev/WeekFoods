from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse

from WeekFoods import settings
from .forms import ContactForm


def contacto(request):
    print('e')

    # Guardamos en una variable el formulario de contacto creado en el archivo forms.py
    contact_form = ContactForm()

    # Comprobamos si se ha rellenado el formulario y enviado datos
    if request.method == 'POST':
        print('entrara')
        # Recogemos los datos introducidos
        contact_form = ContactForm(data=request.POST)

    # Debemos comprobar si el formulario es válido.
    # En caso que los datos sean correctos los almacenamos en variables
        if contact_form.is_valid():
            name = contact_form.cleaned_data.get('name')
            email = contact_form.cleaned_data.get('email')
            subject = contact_form.cleaned_data.get('subject')
            message = contact_form.cleaned_data.get('message')
            terms_accepted = contact_form.cleaned_data.get('terms_accepted')

            # Vamos a intentar enviar el mail:
            try:
                send_mail(subject, f'De {name} <{email}>\nMensaje:\n{message}', email, [
                          settings.EMAIL_HOST_USER], fail_silently=False,)
                # Indicar al usuario que se ha enviado correctamente.
                messages.success(
                    request, 'Gracias por contactar con nosotros!')
                return redirect(reverse('Contacto') + '?valido')
            except Exception as e:
                print('entra aqui')
                messages.error(
                    request, 'No se ha podido enviar el mensaje, intentelo mas tarde')
                return render(request, 'Contacto/contacto.html', {'mi_formulario': contact_form})

        else:
            return render(request, 'Contacto/contacto.html', {'mi_formulario': contact_form})

    return render(request, 'Contacto/contacto.html', {'mi_formulario': contact_form})
