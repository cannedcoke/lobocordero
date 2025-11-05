# ======== MODELOS ========
# Importa SQLAlchemy para manejar la base de datos usando un ORM (mapa objeto-relacional)
from flask_sqlalchemy import SQLAlchemy

# Inicializa el objeto de base de datos
db = SQLAlchemy()

# ======== TABLA: POLITICO ========
class Politico(db.Model):
    __tablename__ = 'politico'  # Nombre real de la tabla en la base de datos

    # Columnas
    id = db.Column(db.Integer, primary_key=True)           # Identificador único
    foto = db.Column(db.String(50), nullable=True)         # Nombre del archivo de la foto
    nombre = db.Column(db.String(50), nullable=True)       # Nombre del político
    partido = db.Column(db.String(50), nullable=True)      # Partido político al que pertenece
    titulo = db.Column(db.String(50), nullable=True)       # Cargo o título (Ej: Presidente, Senador)

    # Relaciones
    respuesta = db.relationship('Respuesta', back_populates='politico')  # Relación con las respuestas
    proyectos = db.relationship('Proyecto', back_populates='politico')   # Relación con los proyectos

    # Constructor
    def __init__(self, nombre, partido, titulo, foto=None):
        self.nombre = nombre
        self.partido = partido
        self.titulo = titulo
        self.foto = foto


# ======== TABLA: PREGUNTA ========
class Pregunta(db.Model):
    __tablename__ = 'pregunta'  # Tabla de las preguntas de la encuesta

    id_pregunta = db.Column(db.Integer, primary_key=True)       # Identificador único
    descripcion = db.Column(db.String(100), nullable=False)     # Texto de la pregunta

    # Relación con respuestas
    respuesta = db.relationship('Respuesta', back_populates='pregunta')

    # Constructor
    def __init__(self, descripcion):
        self.descripcion = descripcion


# ======== TABLA: RESPUESTA ========
class Respuesta(db.Model):
    __tablename__ = 'respuesta'  # Tabla de las respuestas enviadas por los usuarios

    id_respuesta = db.Column(db.Integer, primary_key=True)           # Identificador único
    id_politico = db.Column(db.Integer, db.ForeignKey('politico.id'))  # Relación con político
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id_pregunta'))  # Relación con pregunta
    id_opinion = db.Column(db.Integer, nullable=False)                # Valor numérico de la opinión (1-5, etc.)

    # Relaciones inversas
    politico = db.relationship('Politico', back_populates='respuesta')
    pregunta = db.relationship('Pregunta', back_populates='respuesta')

    # Constructor
    def __init__(self, id_politico, id_pregunta, id_opinion):
        self.id_politico = id_politico
        self.id_pregunta = id_pregunta
        self.id_opinion = id_opinion


# ======== TABLA: PROYECTO ========
class Proyecto(db.Model):
    __tablename__ = 'proyecto'  # Tabla de proyectos asociados a los políticos

    idproyecto = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Identificador del proyecto
    id_politico = db.Column(db.Integer, db.ForeignKey('politico.id'))         # Relación con político
    titulo = db.Column(db.String(100), nullable=False)                        # Título del proyecto
    descripcion = db.Column(db.Text, nullable=False)                          # Descripción detallada del proyecto

    # Relación inversa con político
    politico = db.relationship('Politico', back_populates='proyectos')

    # Constructor
    def __init__(self, id_politico, titulo, descripcion):
        self.id_politico = id_politico
        self.titulo = titulo
        self.descripcion = descripcion
