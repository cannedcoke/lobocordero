🐺 Lobo Cordero — Perfiles Políticos del Paraguay

Descripción general
Lobo Cordero es una aplicación web desarrollada con Flask y SQLite, enfocada en promover la transparencia política y la participación ciudadana en Paraguay.
El sistema presenta perfiles de políticos con sus proyectos, permite realizar encuestas ciudadanas y muestra resultados visuales mediante gráficos dinámicos.
La idea central es acercar información clara, verificable y accesible sobre los representantes del país.

---

Tecnologías utilizadas
Python 3 con Flask como framework principal.
SQLite para la base de datos local.
SQLAlchemy para el manejo de modelos ORM.
HTML5, CSS3 y Jinja2 para el front-end.
Chart.js para la visualización de resultados.

---

Estructura principal del proyecto
/static

* /img → Imágenes de políticos, logos y fondos
* /styles → Archivos CSS (style.css, styleEncuesta.css, politicos.css, styleNosotros.css)

/templates

* index.html → Página de inicio
* politicos.html → Tarjetas interactivas con los perfiles
* encuesta.html → Formulario de encuestas
* resultados.html → Gráficos de resultados con Chart.js
* nosotros.html → Página “Sobre Nosotros”

Archivos principales:

* app.py → Controlador principal Flask
* conexion.py → Configuración de la base de datos
* models.py → Definición de tablas y relaciones ORM

---

Funcionalidades principales
Carga automática de políticos con sus proyectos y promesas cumplidas o no.
Encuestas por político con siete preguntas predeterminadas.
Resultados de encuestas visualizados en gráficos de barras.
Filtros por presidentes, diputados y senadores.
Interfaz adaptable y accesible.
Efectos visuales como tarjetas interactivas, transiciones y fondos dinámicos.
Página informativa con misión y visión del proyecto.

---

Instalación y ejecución

1. Clonar el repositorio:
   git clone [https://github.com/](https://github.com/)cannedcoke/lobocordero.git
   cd lobocordero

2. Crear y activar el entorno virtual:
   python -m venv .venv
   source .venv/bin/activate (Linux o macOS)
   .venv\Scripts\activate (Windows)

3. Instalar dependencias:
   pip install flask sqlalchemy

4. Ejecutar la aplicación:
   python app.py( en las siguientes instancias se puede usar flask run)

5. Acceder desde el navegador:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

Integrantes del equipo
Miqueas Zarate
David Gonzalez
Damian Lopez
Camila Torres
Horacio Sosa
Tobias Viera

---

Licencia
Proyecto académico — Todos los derechos reservados © 2025 Lobo Cordero.

---

Nota final
Lobo Cordero nace como una herramienta ciudadana que busca informar sin manipular, mostrar sin adornos y recordar que la transparencia no se promete, se demuestra.
