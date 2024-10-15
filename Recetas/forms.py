from django.forms import ModelForm, TextInput, NumberInput, Select, URLInput
from django import forms
from WeekFoodsApp.models import Recipe, Ingredient

"""class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, ingredient):
        return ingredient.name"""

class RecipeForms(ModelForm):  

    ingredients = forms.ModelMultipleChoiceField(queryset = Ingredient.objects.all(),
                                                 widget = forms.CheckboxSelectMultiple)

    class Meta:
        model = Recipe
        fields = ['name', 'elaboration', 'when_you_eat', 'calories', 'ingredients']
        widgets = {'name': TextInput(attrs={'required':True}),
                   'elaboration': URLInput(attrs={'required':True}),
                   'when_you_eat': Select(attrs={'required':True}),
                   'calories': NumberInput(attrs={'required':True})}
        

    
        

class IngredientForms(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name_ingredient', 'type_food', 'price']
        widgets = {
            'name_ingredient': TextInput(attrs={'required':True}),
            'type_food': Select(attrs={'required':True}),
            'price': NumberInput(attrs={'required':True})
        }