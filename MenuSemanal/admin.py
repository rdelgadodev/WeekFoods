from django.contrib import admin

from .models import WeeklyMenu

@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    list_display=('user_active', 'recipe_sug')
    list_filter=('user_active',)
    




