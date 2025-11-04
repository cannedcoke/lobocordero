from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Politico(db.Model):
    __tablename__='politico'
    id=db.Column(db.Integer, primary_key=True)
    foto=db.Column(db.String(50), nullable=True )
    nombre=db.Column(db.String(50), nullable=True)
    partido=db.Column(db.String(50), nullable=True)
    titulo=db.Column(db.Integer, nullable=True)

    respuesta=db.relationship('Respuesta', back_populates='politico')
    proyectos = db.relationship('Proyecto', back_populates='politico')
    def __init__(self,nombre, foto, partido, titulo):
        self.nombre=nombre
        self.foto=foto
        self.partido=partido
        self.titulo=titulo

class Pregunta(db.Model):
    __tablename__='pregunta'
    id_pregunta=db.Column(db.Integer, primary_key=True)
    descripcion=db.Column(db.String(50), nullable=True)

    respuesta=db.relationship('Respuesta', back_populates='pregunta')
    def __init__(self, descripcion):
     
        self.descripcion=descripcion

class Opinion(db.Model):
    __tablename__='opinion'
    id_opinion=db.Column(db.Integer, primary_key=True)
    descripcion=db.Column(db.String(50), nullable=True)

    respuesta=db.relationship('Respuesta', back_populates='opinion')

    def __init__(self,descripcion):
        
        self.descripcion=descripcion
class Respuesta(db.Model):
    __tablename__='respuesta'
    id_respuesta=db.Column(db.Integer, primary_key=True)
    id_politico=db.Column(db.Integer, db.ForeignKey('politico.id'))
    id_pregunta=db.Column(db.Integer, db.ForeignKey('pregunta.id_pregunta'))
    id_opinion=db.Column(db.Integer, db.ForeignKey('opinion.id_opinion'))

    politico=db.relationship('Politico', back_populates='respuesta')
    pregunta=db.relationship('Pregunta', back_populates='respuesta')
    opinion=db.relationship('Opinion', back_populates='respuesta')


    def __init__(self, id_politico, id_pregunta, id_opinion):
    
        self.id_politico=id_politico
        self.id_pregunta=id_pregunta
        self.id_opinion=id_opinion
            
class Proyecto(db.Model):
    __tablename__='proyecto'
    idproyecto=db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_politico=db.Column(db.Integer, db.ForeignKey('politico.id'))
    titulo=db.Column(db.String(100))
    descripcion=db.Column(db.Text, nullable=False)

    politico=db.relationship('Politico', back_populates='proyectos')
    def __init__(self, id_politico,titulo,descripcion):
        self.id_politico=id_politico
        self.titulo=titulo
        self.descripcion=descripcion
        


