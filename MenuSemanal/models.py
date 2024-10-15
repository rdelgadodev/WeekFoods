from django.db import models
from WeekFoodsApp.models import Recipe, UserWeekfoods

# Se crea una base de datos donde se almacene el menu semanal para cada usuario.
# Tendrá dos campos, uno donde se almanecene el usuario  (clave foranea con la bd UserWeekfoods) 
# y otro con la receta sugerida para un determinado momento. (clave foranea con la bd Recipe)

class WeeklyMenu(models.Model):

    user_active = models.ForeignKey(UserWeekfoods, on_delete=models.CASCADE, verbose_name='Nombre de usuario')
    recipe_sug = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Receta del menú semanal')

    def __str__(self):
        return self.recipe_sug.name
