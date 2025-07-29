🥗 WeekFoods: Tu planificador semanal de comidas

¡Bienvenido a WeekFoods! Esta es una aplicación web diseñada para simplificar tu planificación semanal de comidas y cenas, ayudándote a llevar un control de tu alimentación y presupuesto. Olvídate de la pregunta "¿Qué comemos hoy?" y empieza a disfrutar de una vida más organizada y saludable.

🌟 Características Principales

•	Planificación Semanal: Organiza tus comidas y cenas de lunes a viernes. 
•	Gestión de Recetas:
    o	Acceso a un amplio listado de recetas. 
    o	Visualiza detalles de cada receta: elaboración, ingredientes, calorías y coste. 
    o	Crea y comparte tus propias recetas con la comunidad. 
    o	Elimina recetas que no sean de tu agrado. 
•	Creación de Menús Flexibles:
    o	Menú Filtrado: Genera un menú semanal automáticamente aplicando filtros de calorías máximas diarias y gasto diario. 
    o	Menú Personalizado: Escoge manualmente cada plato para cada día y momento (comida/cena). 
    o	Modificación del Menú: Posibilidad de modificar una, varias o todas las recetas del menú semanal generado. 
    o	Eliminación del Menú: Opción para eliminar el menú semanal completo. 
•	Lista de la Compra: Genera automáticamente una lista de los ingredientes necesarios para tu menú semanal, incluyendo el coste aproximado. 
•	Gestión de Ingredientes: Añade nuevos ingredientes a la base de datos si no existen en el listado. 
•	Comunidad: Fomenta la creación de una comunidad donde los usuarios pueden compartir y acceder a las recetas de otros. 

🎯 Objetivos del Proyecto
•	Eliminar Preocupaciones Alimentarias: Simplificar la pregunta diaria de qué cocinar. 
•	Fomentar la Vida Saludable: Ofrecer recetas equilibradas, ricas en verduras y proteínas. 
•	Economía Doméstica: Ayudar a planificar menús que no supongan un gran desembolso económico. 
•	Experiencia de Usuario: Proporcionar una web atractiva, funcional y sencilla de usar, con tutoriales en vídeo disponibles. 

🛠️ Tecnologías Utilizadas
Este proyecto ha sido desarrollado utilizando un robusto stack tecnológico: 
•	Lenguaje de Programación: Python 3 
•	Framework Web: Django (elegido por su rapidez, facilidad de uso, seguridad, panel de administración y escalabilidad). 
•	Base de Datos: PostgreSQL (seleccionado por su alta estabilidad, soporte SQL, acceso simultáneo, escalabilidad y rendimiento óptimo bajo cargas pesadas). 
•	Entorno de Desarrollo: Visual Studio Code (VSC) 
•	Entorno Virtual: Virtualenv 
•	Diseño y Maquetación:
    o	Bootstrap (librería de componentes gráficos y maquetador de diseño responsivo). 
    o	Google Fonts 
    o	Font Awesome (biblioteca de iconos vectoriales). 

📂 Modelo de Datos
El proyecto utiliza una base de datos relacional compuesta por 4 tablas principales:  
•	Ingredient: Almacena los detalles de cada ingrediente (nombre, tipo de alimento, precio). 
•	Recipe: Contiene la información de las recetas (nombre, elaboración, momento de consumo, calorías). 
•	UserWeekfoods: Relacionada con el modelo de usuario por defecto de Django, guarda información adicional del perfil de usuario. 
•	WeeklyMenu: Almacena el menú semanal de cada usuario. 
Se utilizan relaciones ManyToMany entre Ingredient y Recipe, y entre UserWeekfoods y Recipe para permitir múltiples ingredientes por receta y que todos los usuarios accedan a todas las recetas. También se usan claves foráneas para relacionar UserWeekfoods y Recipe con WeeklyMenu. 

🚀 Instalación
Para poner en marcha la aplicación web WeekFoods en tu entorno local, sigue estos sencillos pasos: 

1.- Clona el repositorio:
git clone https://github.com/RaulPW/WeekFoods.git # Asegúrate de reemplazar 'tu-usuario'
cd WeekFoods

2.- Crea y activa un entorno virtual:
python -m venv venv
source venv/bin/activate # En Linux/macOS
o .\venv\Scripts\activate en Windows

3.- Instala las dependencias:
pip install -r requirements.txt

4.- Configura tu base de datos PostgreSQL:
•	Asegúrate de tener PostgreSQL instalado y en funcionamiento.
•	Configura las credenciales de tu base de datos en el archivo settings.py de tu proyecto Django (bases de datos, usuario, contraseña).

5.- Realiza las migraciones de la base de datos:
python manage.py makemigrations
python manage.py migrate

6.- Crea un superusuario (opcional, para acceder al panel de administración de Django):
python manage.py createsuperuser

7.- Ejecuta la aplicación:
python manage.py runserver

💡 Uso
Una vez que la aplicación esté en funcionamiento:
1.	Registro/Inicio de Sesión:
    o	Si eres un usuario nuevo, haz clic en "¿Eres nuevo?" para registrarte con tus datos. 
    o	Si ya tienes una cuenta, introduce tus credenciales en la página principal y haz clic en "Login" para acceder a tu perfil. 
2.	Planifica tu Menú Semanal:
    o	Desde la página principal, puedes seleccionar manualmente las recetas para cada comida y cena, o
    o	Utiliza los filtros de calorías y gasto para que la aplicación te proponga un menú completo. 
    o	Puedes modificar las recetas seleccionadas y guardar los cambios. 
    o	También puedes eliminar todo el menú semanal para empezar de nuevo. 
3.	Gestiona tus Recetas:
    o	Accede al listado de recetas para ver las disponibles, organizadas en páginas. 
    o	Haz clic en "Ver receta" para obtener detalles de preparación e ingredientes. 
    o	Crea nuevas recetas rellenando un formulario y guardándolas. Inicialmente son privadas hasta que decidas "Compartir" para que sean accesibles a toda la comunidad. 
    o	Elimina recetas que no desees mantener. 
4.	Lista de la Compra: Accede a la sección de "Lista de la compra" para ver los ingredientes y cantidades que necesitas comprar para tu menú planificado.

🤝 Contribución
¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto o añadir nuevas funcionalidades, por favor, sigue estos pasos:
1.	Haz un "fork" de este repositorio.
2.	Crea una nueva rama (git checkout -b feature/nombre-de-tu-funcionalidad).
3.	Realiza tus cambios y haz "commit" (git commit -m 'feat: Añade nueva funcionalidad X').
4.	Sube tus cambios a tu repositorio fork (git push origin feature/nombre-de-tu-funcionalidad).
5.	Abre una Pull Request explicando tus cambios.

📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE (si existe) para más detalles.


