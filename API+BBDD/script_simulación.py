import os
import random
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELOS
class Sesion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion_mac = db.Column(db.String, nullable=False)
    tiempo_entrada = db.Column(db.DateTime, nullable=False)
    tiempo_salida = db.Column(db.DateTime, nullable=True)
    navegador = db.Column(db.String, nullable=True)
    zona_horaria = db.Column(db.String, nullable=True)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String, nullable=False)

class Iteracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesion.id'), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    tiempo = db.Column(db.DateTime, nullable=False)

class Interaccion_elemento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_iteracion = db.Column(db.Integer, db.ForeignKey('iteracion.id'), nullable=False)
    tag_elemento = db.Column(db.String, nullable=False)

class Cambio_pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_iteracion = db.Column(db.Integer, db.ForeignKey('iteracion.id'), nullable=False)
    pagina_inicial = db.Column(db.String, nullable=False)
    pagina_destino = db.Column(db.String, nullable=False)

class Formulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_iteracion = db.Column(db.Integer, db.ForeignKey('iteracion.id'), nullable=False)
    pregunta = db.Column(db.String, nullable=False)
    respuesta = db.Column(db.String, nullable=True)

# FUNCIÓN DE SIMULACIÓN
def simular_onboarding_lineal():
    db.drop_all()
    db.create_all()

    db.session.add_all([
        Evento(id=1, descripcion="Click Elemento"),
        Evento(id=2, descripcion="Cambio Página"),
        Evento(id=3, descripcion="Formulario Final")
    ])
    db.session.commit()

    navegadores = ['Chrome', 'Firefox', 'Edge']
    zonas = ['UTC+1', 'UTC+2']

    # Cada elemento solo aparece en una página
    elementos_por_pagina = {
        '/start': ['btn_start'],
        '/intro': ['btn_intro', 'icon_intro'],
        '/features': ['btn_feat', 'icon_feat'],
        '/cta': ['btn_cta'],
        '/signup': ['btn_submit', 'btn_cancel'],
        '/exit': ['btn_close']
    }

    preguntas_respuestas = {
        '¿El proceso fue claro?': ['Sí', 'No']
    }

    flujo = ['/start', '/intro', '/features', '/cta']
    finales = ['/signup', '/exit']
    now = datetime.now()
    dias_simulados = 40
    sesiones_por_dia = [random.randint(5 + i, 10 + i) for i in range(dias_simulados)]

    for dias_atras, sesiones_hoy in enumerate(sesiones_por_dia[::-1]):
        dia_base = now - timedelta(days=dias_atras)

        for _ in range(sesiones_hoy):
            entrada = dia_base.replace(hour=random.randint(9, 18), minute=random.randint(0, 59))
            salida = entrada + timedelta(minutes=random.randint(5, 10))

            sesion = Sesion(
                direccion_mac=f"00:aa:bb:cc:dd:{random.randint(10, 99)}",
                tiempo_entrada=entrada,
                tiempo_salida=salida,
                navegador=random.choice(navegadores),
                zona_horaria=random.choice(zonas)
            )
            db.session.add(sesion)
            db.session.commit()

            tiempo_iteracion = entrada + timedelta(minutes=1)
            pagina_actual = flujo[0]
            elementos_usados = set()
            formulario_respondido = False

            def interactuar_en_pagina(pagina, tiempo):
                elementos = list(set(elementos_por_pagina[pagina]) - elementos_usados)
                if elementos:
                    n = random.randint(0, len(elementos))
                    for tag in random.sample(elementos, n):
                        it = Iteracion(id_sesion=sesion.id, id_evento=1, tiempo=tiempo)
                        db.session.add(it)
                        db.session.commit()
                        db.session.add(Interaccion_elemento(id_iteracion=it.id, tag_elemento=tag))
                        db.session.commit()
                        elementos_usados.add(tag)
                        tiempo += timedelta(minutes=1)
                return tiempo

            # Interacción inicial
            tiempo_iteracion = interactuar_en_pagina(pagina_actual, tiempo_iteracion)

            # Avance del flujo
            avanza = random.random() < 0.7
            if avanza:
                for idx in range(len(flujo) - 1):
                    siguiente = flujo[idx + 1]
                    it = Iteracion(id_sesion=sesion.id, id_evento=2, tiempo=tiempo_iteracion)
                    db.session.add(it)
                    db.session.commit()
                    db.session.add(Cambio_pagina(
                        id_iteracion=it.id,
                        pagina_inicial=pagina_actual,
                        pagina_destino=siguiente
                    ))
                    db.session.commit()
                    pagina_actual = siguiente
                    tiempo_iteracion += timedelta(minutes=1)
                    tiempo_iteracion = interactuar_en_pagina(pagina_actual, tiempo_iteracion)

                # Final
                final = random.choice(finales)
                it = Iteracion(id_sesion=sesion.id, id_evento=2, tiempo=tiempo_iteracion)
                db.session.add(it)
                db.session.commit()
                db.session.add(Cambio_pagina(
                    id_iteracion=it.id,
                    pagina_inicial=pagina_actual,
                    pagina_destino=final
                ))
                db.session.commit()
                pagina_actual = final
                tiempo_iteracion += timedelta(minutes=1)
                tiempo_iteracion = interactuar_en_pagina(pagina_actual, tiempo_iteracion)

                # Formulario solo una vez
                if not formulario_respondido:
                    it = Iteracion(id_sesion=sesion.id, id_evento=3, tiempo=tiempo_iteracion)
                    db.session.add(it)
                    db.session.commit()
                    db.session.add(Formulario(
                        id_iteracion=it.id,
                        pregunta='¿El proceso fue claro?',
                        respuesta=random.choice(preguntas_respuestas['¿El proceso fue claro?'])
                    ))
                    db.session.commit()
                    formulario_respondido = True

    print("✅ Simulación terminada con elementos únicos por página y sin repeticiones.")

# EJECUCIÓN
if __name__ == '__main__':
    with app.app_context():
        simular_onboarding_lineal()
