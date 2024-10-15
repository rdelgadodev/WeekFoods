from django.db import models
from django.contrib.auth.models import User


# Tabla Ingredientes
class Ingredient(models.Model):

    option_type_food = [
        ('Aceites', 'Aceites'),
        ('Lácteos', 'Lácteos'),
        ('Legumbres', 'Legumbres'),
        ('Setas', 'Setas'),
        ('Verduras', 'Verduras'),
        ('Frutas', 'Frutas'),
        ('Cereales', 'Cereales'),
        ('Pescado', 'Pescado'),
        ('Marisco', 'Marisco'),
        ('Carnes', 'Carnes'),
        ('Especias', 'Especias'),
        ('Frutos secos', 'Frutos secos')
    ]
    name_ingredient = models.CharField(max_length=100, 
                                       verbose_name='Nombre', 
                                       unique='True')
    
    type_food = models.CharField(max_length=30, 
                                 verbose_name='Tipo de alimento', 
                                 choices=option_type_food)
    
    price = models.FloatField(verbose_name='Precio')

    class Meta():
        ordering = ['name_ingredient']

    def __str__(self):
        return self.name_ingredient


# Tabla Recetas
class Recipe(models.Model):

    moments_of_day = [('Comida', 'Comida'), ('Cena', 'Cena')]

    name = models.CharField(max_length=100, verbose_name='Nombre')
    
    elaboration = models.URLField(verbose_name='Elaboración')

    when_you_eat = models.CharField(max_length=7,
                              verbose_name='Momento del día para comer', 
                              choices=moments_of_day,
                              default='comida')

    calories = models.IntegerField(verbose_name='calorias')


    # Se creará una base de datos que une cada receta con sus ingredientes correspondientes.
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Ingredientes')
    
    

    def __str__(self):
        return self.name


# Tabla Usuario
class UserWeekfoods(models.Model):

    # Usamos el modelo User que nos ofrece Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Nombre de usuario')

    # Se creará una base de datos que almacena todas las recetas de las que dispone cada usuario.
    recipe = models.ManyToManyField(Recipe, verbose_name='Recetas')

    def __str__(self):
        return self.user.first_name