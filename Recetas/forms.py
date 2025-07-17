from django.forms import ModelForm, TextInput, NumberInput, Select, URLInput
from django import forms
from WeekFoodsApp.models import Recipe, Ingredient


class RecipeForms(forms.ModelForm):

    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Recipe
        fields = ['name', 'elaboration',
                  'when_you_eat', 'calories', 'ingredients']
        widgets = {'name': TextInput(attrs={'class': 'form-control'}),
                   'elaboration': URLInput(attrs={'class': 'form-control', 'placeholder': 'Insert URL de video de la receta'}),
                   'when_you_eat': Select(),
                   'calories': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 350'}),}


class IngredientForms(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name_ingredient', 'type_food', 'price']
        widgets = {
            'name_ingredient': TextInput(attrs={'required': True, 'class': 'form-control'}),
            'type_food': Select(attrs={'required': True, 'class': 'form-control'}),
            'price': NumberInput(attrs={'required': True, 'class': 'form-control'})
        }
