from django.contrib import admin

from .models import Ingredient, Recipe, UserWeekfoods

class IngredientAdmin(admin.ModelAdmin):
    list_display=('name_ingredient', 'type_food', 'price')
    search_fields=('name_ingredient', 'type_food', 'price')
    list_filter=('type_food',)

class RecipeAdmin(admin.ModelAdmin):
    list_display=('name', 'when_you_eat', 'calories')
    search_fields=('name', 'when_you_eat', 'calories')



admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserWeekfoods)
