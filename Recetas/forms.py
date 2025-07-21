from django.forms import ModelForm, TextInput, NumberInput, Select, URLInput
from django import forms
from WeekFoodsApp.models import Recipe, Ingredient
import re

# Patron de expresion regular para validar URLs de YouTube
YOUTUBE_ID_PATTERN = re.compile(
    r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})'
)

# En este formulario debemos hacer dos validaciones, de url(que sea de youtube) y de ingredientes(haremos un mensaje personalizado si no se ha seleccionado ninguno).


class RecipeForms(forms.ModelForm):

    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox-button-list'}), required=False)

    class Meta:
        model = Recipe
        fields = ['name', 'elaboration',
                  'when_you_eat', 'calories', 'ingredients']
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'elaboration': URLInput(attrs={'class': 'form-control', 'placeholder': 'Insert URL de video de la receta de youtube'}),
                   'when_you_eat': Select(),
                   'calories': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 350'}), }

    def clean_elaboration(self):
        """
        Valida que la URL de elaboración sea una URL de YouTube válida y la transforma
        a un formato de incrustación estándar (embed URL) antes de guardarla.
        """
        elaboration = self.cleaned_data.get('elaboration')

        if elaboration:
            match = YOUTUBE_ID_PATTERN.match(elaboration)
            if not match:
                raise forms.ValidationError(
                    'La URL debe ser un enlace válido de YouTubet.')

            # Si la URL es válida, extraemos el ID del video.
            video_id = match.group(1)
            # Transformar a formato de incrustación estándar
            elaboration = f'https://www.youtube.com/embed/{video_id}'

            # Si la URL es válida, extraemos el ID del video.
            return elaboration

        return elaboration

    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients')
        if not ingredients:
            raise forms.ValidationError(
                'Debes seleccionar al menos un ingrediente.')
        return ingredients


class IngredientForms(ModelForm):

    type_food = forms.ChoiceField(choices=Ingredient.option_type_food,
                                  widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Ingredient
        fields = ['name_ingredient', 'type_food', 'price']
        widgets = {
            'name_ingredient': TextInput(attrs={'class': 'form-control'}),
            'type_food': Select(),
            'price': NumberInput(attrs={'class': 'form-control'})
        }
        
    def clean_name_ingredient(self):
        # Validar que el nombre del ingrediente no este creado previamente.
        print(self.cleaned_data)
        name = self.cleaned_data['name_ingredient']
        if Ingredient.objects.filter(name_ingredient__iexact=name).exists() :
            raise forms.ValidationError('Este ingrediente ya existe. Por favor, vuelva a la receta y filtre su búsqueda')
        return name.capitalize()
