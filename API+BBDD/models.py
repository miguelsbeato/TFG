from database import db
from datetime import datetime, timedelta

class Sesion(db.Model): # Tabla de Sesiones
    id = db.Column(db.Integer, primary_key=True)
    direccion_mac = db.Column(db.String, nullable=False)
    tiempo_entrada = db.Column(db.DateTime, nullable=False)
    tiempo_salida = db.Column(db.DateTime, nullable=True)
    navegador = db.Column(db.String, nullable=True)
    zona_horaria = db.Column(db.String, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'direccion_mac': self.direccion_mac,
            'tiempo_entrada': self.tiempo_entrada,
            'tiempo_salida': self.tiempo_salida if self.tiempo_salida else None,
            'navegador': self.navegador if self.navegador else None,
            'zona_horaria': self.zona_horaria if self.zona_horaria else None
        }
    
class Evento(db.Model): # Tabla de Eventos (1: Interacción con Elementos, 2: Cambio de Página, 3: Formulario)
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
        }
        
class Iteracion(db.Model): # Tabla de Iteraciones
    id = db.Column(db.Integer, primary_key=True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    tiempo = db.Column(db.DateTime, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_sesion': self.id_sesion,
            'id_evento': self.id_evento,
            'tiempo': self.tiempo
        }
    
class Interaccion_elemento(db.Model): # Tabla de Interacción con Elementos
    id = db.Column(db.Integer, primary_key=True)
    id_iteracion = db.Column(db.Integer, db.ForeignKey('iteracion.id'), nullable=False)
    tag_elemento = db.Column(db.String, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_iteracion': self.id_iteracion,
            'tag_elemento': self.tag_elemento
        }
    
class Cambio_pagina(db.Model): # Tabla de Cambio de Página
    id = db.Column(db.Integer, primary_key=True)
    id_iteracion = db.Column(db.Integer, db.ForeignKey('iteracion.id'), nullable=False)
    pagina_inicial = db.Column(db.String, nullable=False)
    pagina_destino = db.Column(db.String, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_iteracion': self.id_iteracion,
            'pagina_inicial': self.pagina_inicial,
            'pagina_destino': self.pagina_destino
        }
    
class Formulario(db.Model): # Tabla de Formularios
    id = db.Column(db.Integer, primary_key=True)
    id_iteracion = db.Column(db.Integer, db.ForeignKey('iteracion.id'), nullable=False)
    pregunta = db.Column(db.String, nullable=False)
    respuesta = db.Column(db.String, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_iteracion': self.id_iteracion,
            'pregunta': self.pregunta,
            'respuesta': self.respuesta
        }