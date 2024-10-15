from django.shortcuts import render, redirect

from .forms import ContactForm

def contacto(request):

    # Guardamos en una variable el formulario de contacto creado en el archivo forms.py
    contact_form = ContactForm()

    # Comprobamos si se ha rellenado el formulario y enviado datos
    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST) # Recogemos los datos introducidos

    # Debemos comprobar si el formulario es válido. 
    # En caso que los datos sean correctos los almacenamos en variables
        if contact_form.is_valid:

            # Indicar al usuario que se ha enviado correctamente.
            return redirect ('/contacto/?valido')
        
    return render(request, 'Contacto/contacto.html', {'mi_formulario' : contact_form}) 




