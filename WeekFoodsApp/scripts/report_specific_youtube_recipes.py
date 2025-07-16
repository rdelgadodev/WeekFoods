from django.apps import apps
import sys

# --- Configuración ---
APP_NAME = 'WeekFoodsApp'
MODEL_NAME = 'Recipe'
# ID de video específico que quieres usar para la comprobación
YOUTUBE_ID_TO_CHECK = 'V8MU0BlN4Wk' 

def report_recipes_with_specific_youtube_id():
    """
    Busca recetas que contengan un ID de video de YouTube específico
    en su campo 'elaboration' y las reporta, indicando que su enlace
    debe ser comprobado.
    """
    try:
        # Obtener el modelo Recipe dinámicamente
        Recipe = apps.get_model(APP_NAME, MODEL_NAME)
    except LookupError:
        print(f"ERROR: No se pudo encontrar el modelo '{MODEL_NAME}' en la aplicación '{APP_NAME}'.")
        print("Por favor, verifica que APP_NAME y MODEL_NAME sean correctos y que la aplicación esté en INSTALLED_APPS.")
        sys.exit(1)

    print(f"--- Reporte de recetas con el ID de video '{YOUTUBE_ID_TO_CHECK}' ---")
    print("-" * 50)

    # Buscar recetas que contengan el ID específico en su campo 'elaboration'
    # Usamos __contains para buscar la subcadena
    recipes_found = Recipe.objects.filter(elaboration__contains=YOUTUBE_ID_TO_CHECK)
    
    if not recipes_found.exists():
        print(f"No se encontraron recetas que contengan el ID '{YOUTUBE_ID_TO_CHECK}'.")
        return

    count_reported = 0
    print(f"Se encontraron {recipes_found.count()} recetas que contienen el ID '{YOUTUBE_ID_TO_CHECK}':")
    print("\n--- Recetas a Comprobar ---")
    for recipe in recipes_found:
        count_reported += 1
        print(f"\n  - Receta ID: {recipe.id}")
        print(f"    Nombre: {recipe.name}")
        print(f"    Enlace Potencial: https://www.youtube.com/watch?v={YOUTUBE_ID_TO_CHECK}")
        print("    ACCIÓN REQUERIDA: Comprobar manualmente este enlace y actualizar la receta si es necesario.")
    
    print("\n" + "=" * 50)
    print(f"¡Reporte completado! Se identificaron {count_reported} recetas para revisión.")