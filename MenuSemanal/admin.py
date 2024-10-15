from django.contrib import admin

from .models import WeeklyMenu

class WeeklyMenuAdmin(admin.ModelAdmin):
    list_display=('user_active', 'recipe_sug')
    list_filter=('user_active',)
    

admin.site.register(WeeklyMenu, WeeklyMenuAdmin)


