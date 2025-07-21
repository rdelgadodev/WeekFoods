// Evento que se dispara cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    //Creamos constantes con los valores que necesitamos capturar
    //Ingrediente que el usuario ingresa
    const inputUser = document.getElementById('ingredient-search');
    //Listado de ingredientes
    const listIngredients = document.getElementById('id_ingredients');

    //Procederemos a seguir con la funcion si ambas constantes existen
    if (inputUser && listIngredients){
        // Guardamos en una constante el conjunto de ingredientes
        const itemIngredients = listIngredients.querySelectorAll(':scope > div');

        //Creamos evento para cada vez que el usuario escriba en el input.
        document.addEventListener('input', function(){

            //Guardamos en una variable el valor del input introducido
            const inputIngredient = inputUser.value.toLowerCase();

            //Iteramos sobre todos los ingredientes
            itemIngredients.forEach(item => {
                // En una constante guardamos el contenido del label
                const labelText = item.textContent.toLowerCase();

                //Hacemos comparación para ver si existe el ingrediente escrito en nuestro listado
                if (labelText.includes(inputIngredient)){
                    // Como existe el ingrediente, modificamos el estilo del label (item)
                    item.style.display = 'block';
                } else {
                    //Sino existe, no mostramos por pantalla el ingrediente
                    item.style.display = 'none'
                }

            });
        })
    } else{
        console.warn('No se encuentran las constantes')
    }
    
    
})