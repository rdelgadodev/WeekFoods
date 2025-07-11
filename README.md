DESCRIPCIÓN GENERAL

En esta época en la que vivimos, donde prima la inmediatez, necesitamos tener bajo control y planificado nuestro día a día. Una parte importante de la planificación es nuestra alimentación, por ello he creado una aplicación web que ayude al usuario a planificar las comidas y cenas de la semana (de lunes a viernes). 
Para poder llevar a cabo la organización de este menú semanal, el usuario contará con un listado de recetas que le ofreceremos cuando inicie sesión en su perfil o se registre como nuevo cliente. Podrá crear y compartir recetas con los demás miembros de nuestra aplicación. También tendrá la opción de eliminar recetas que no sean de su gusto.

Se le ofrecerá al usuario tres opciones a la hora de elaborar el menú semanal:

A.	Podrá solicitar requisitos a ese menú semanal a través de filtros, como son el máximo de calorías diarios que desea consumir y el máximo de gasto diario que está dispuesto a hacer. 

B.	Podrá escoger cada plato que desea consumir para un momento concreto. Para ello tendrá a su disposición un listado de recetas.

Una vez presentado el menú semanal, el consumidor tiene la posibilidad de modificar una, varias o todas las recetas. Podrá solicitar ver la lista de la compra que debe realizar para poder cocinar todas las recetas, así como el coste aproximado de todo ello.
Pero no todo acaba aquí, se les ofrece a los usuarios poder acceder a todo el listado de recetas que dispone, visualizar como se elabora el plato, que ingredientes necesita, calorías que consumirá y el coste de dicha receta. Además, podrá crear nuevas recetas e incluir ingredientes que no tuviésemos contemplados.



OBJETIVOS Y ALCANCE

El principal objetivo de este proyecto es crear una aplicación que ofrezca un servicio al usuario que le ayude a eliminar sus preocupaciones alimentarias.  ¿Cuántas veces nos preguntamos, que hacemos hoy para comer? Con esta aplicación web obtendrás siempre la respuesta.
Uno de los objetivos secundarios de esta aplicación es inculcar, a través de las recetas que ofrecemos, la cultura de la vida saludable. Ofrecer recetas que contienen, en la mayoría de casos, productos con grandes cantidades de verduras y proteínas, que son las grandes claves de una comida sana.
Otros de los objetivos que queremos alcanzar es poder hacer que la elaboración de todas estas recetas no suponga un gran desembolso económico, que este al alcance de cualquier bolsillo. 
Por último, se quiere crear una pequeña comunidad, un portal donde poder acceder para que cada usuario pueda aportar y compartir sus recetas. 
Para poder lograr estos objetivos se ha planteado que la web sea estéticamente bonita, que sea atrayente para el usuario, no muy cargante a la vista, que sea funcional y sencilla para que cualquier tipo de persona pueda manejarse en ella. (Se le ofrece al usuario un pequeño tutorial con videos para que visualice el funcionamiento de la aplicación).



STACK TECNOLÓGICO

El stack tecnológico que se ha usado en este proyecto es el siguiente:
•	Python 3. Como lenguaje de programación base

•	Visual Studio Code (VSC). IDE escogido para el desarrollo del proyecto. Se valoró la opción del Pycharm, pero se descartó porque me siento mas cómodo y familiarizado con VSC.

•	Django. Framework web para Python.

•	PostgreSQL. Sistema de bases de datos de código abierto, altamente estable, que proporciona soporte a diferentes funciones de SQL.

•	Virtualenv. Entorno virtual de Python donde se programará el proyecto.

•	Google Fonts. Fuentes más bonitas que las fuentes estándar.

•	Bootstrap. Librería de componentes gráficos y maquetador de diseño.

•	Font Awesome. Biblioteca de iconos y herramientas que se puede utilizar en el desarrollo de sitios web. Se escogió porque utiliza fuentes vectoriales, en lugar de tener que cargar archivos de imagen pesados, los iconos de Font Awesome se representan como caracteres tipográficos. Esto significa que se pueden escalar y modificar fácilmente sin perder calidad.

MODELO DE DATOS

El tipo de base de datos que se ha escogido es relacional ya que son necesarias sus características para el buen funcionamiento de nuestra aplicación web. Las características que han hecho que elijamos esta opción son:

•	La sencillez a la hora de trabajar en ella, es fácil de crear y accesible con la opción de ampliar la base de datos sin perjudicar a las aplicaciones existentes.  
•	No existe la duplicidad de registros, lo que favorece más a la comprensión y la accesibilidad.  
•	Accesibilidad de varios usuarios en una misma base y al mismo tiempo.
•	Otro punto a destacar es que el rendimiento de las bases de datos relacionales es muy bueno en cuanto a la gran variedad de herramientas que contiene y presenta una experiencia de usuario rápida.

La base de datos que se ha creado para realizar este proyecto está compuesta por 4 tablas. Detallo las entidades y atributos de cada una de ellas. También se indica las relaciones que existen entre ellas mediante algunos de sus atributos:
Aquí se describe la estructura de las principales tablas y sus campos asociados:

| Entidad           | Atributos                                                                                                  |
|:------------------|:-----------------------------------------------------------------------------------------------------------|
| **Ingredient**    | `name_ingredient`, `type_food`, `price`                                                                    |
| **Recipe**        | `name`, `elaboracion`, `when_you_eat`, `calories`, `ingredients(*1)`                                        |
| **UserWeekfoods** | `user(*2)`, `recipe(*3)`                                                                                     |
| **WeeklyMenu(*4)** | `user_active`, `recipe_sug`                                                                                | 

(1)	Se ha usado una relación ManyToMany para relacionar las tablas Ingredient y Recipe, de tal manera que existen recetas que contienen varios ingredientes y existen ingredientes que pueden pertenecer a varias recetas.

(2)	Se ha usado una relación OneToOneField para relacionar la tabla User (modelo que Django ofrece) con la tabla UserWeekfoods. 

(3)	Se ha usado una relación ManytoMany con las tablas UserWeekfoods y Recipe, así todos los usuarios pueden acceder a todas las recetas y todas las recetas son accesibles para todos los usuarios.

(4)	Para ambos atributos se ha usado una clave foránea, de tal manera podamos relacionar los datos de usuarios (UserWeekfoods) y recetas (Recipe) con un menú semanal (WeeklyMenu) 







