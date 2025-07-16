from django.contrib import admin

from .models import Ingredient, Recipe, UserWeekfoods


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name_ingredient', 'type_food', 'price']
    search_fields = ['name_ingredient', 'type_food', 'price']
    list_filter = ['type_food']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'when_you_eat', 'calories']
    search_fields = ['name', 'when_you_eat', 'calories']


@admin.register(UserWeekfoods)
class UserWeekfoodsAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    list_filter = ['user']
