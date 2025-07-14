from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre completo', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Asunto', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(
        attrs={'class': 'form-control mensaje', 'rows': 5}))
    terms_accepted = forms.BooleanField(label='Aceptación de términos y condiciones, política de privacidad y consentimiento para el procesamiento de datos personales: para cumplir con las regulaciones de protección de datos y establecer las expectativas del usuario.',
                                        required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
