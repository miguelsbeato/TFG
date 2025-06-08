from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import *
import os
from sqlalchemy import func
from datetime import datetime, timedelta

# Inicialización de la aplicación
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Rutas de la API para Registrar

@app.route('/sesiones', methods=['POST'])
def crear_sesion():
    cuerpo = request.get_json()
    d_m = cuerpo.get('direccion_mac')
    n = cuerpo.get('navegador')
    z = cuerpo.get('zona_horaria')

    if not d_m or not n:
        return jsonify({"error": "Faltan parámetros en el cuerpo."}), 400

    nueva_sesion = Sesion(direccion_mac=d_m, tiempo_entrada=datetime.now(), tiempo_salida=None, navegador=n, zona_horaria=z)
    db.session.add(nueva_sesion)
    db.session.commit()

    return jsonify(nueva_sesion.to_dict()), 201

@app.route('/sesiones/<int:id>/finalizar', methods=['PUT'])
def finalizar_sesion(id):

    sesion = Sesion.query.get(id)
    if not sesion:
        return jsonify({"error": "Sesión no encontrada."}), 404
    
    if sesion.tiempo_salida:
        return jsonify({"error": "La sesión ya ha sido finalizada."}), 400

    sesion.tiempo_salida = datetime.now()
    db.session.commit()

    return jsonify(sesion.to_dict()), 200

@app.route('/eventos', methods=['POST'])
def crear_evento():
    cuerpo = request.get_json()
    d = cuerpo.get('descripcion')

    if not d:
        return jsonify({"error": "Faltan parámetros en el cuerpo."}), 400

    nuevo_evento = Evento(descripcion=d)
    db.session.add(nuevo_evento)
    db.session.commit()

    return jsonify(nuevo_evento.to_dict()), 201

@app.route('/iteraciones/elementos', methods=['POST'])
def registrar_interaccion_elemento():
    cuerpo = request.get_json()
    id_s = cuerpo.get('id_sesion')
    tag_e = cuerpo.get('tag_elemento')

    if not id_s or not tag_e:
        return jsonify({"error": "Faltan parámetros en el cuerpo."}), 400
    
    sesion = Sesion.query.get(id_s)
    if not sesion:
        return jsonify({"error": "Sesión no encontrada."}), 404
    
    nueva_iteracion = Iteracion(id_sesion=id_s, id_evento=1, tiempo=datetime.now())
    db.session.add(nueva_iteracion)
    db.session.commit()
    
    id_it = nueva_iteracion.id

    nueva_interaccion_elemento = Interaccion_elemento(id_iteracion=id_it, tag_elemento=tag_e)
    db.session.add(nueva_interaccion_elemento)
    db.session.commit()
    
    diccionario_total = nueva_iteracion.to_dict()
    diccionario_total.update(nueva_interaccion_elemento.to_dict())

    return jsonify(diccionario_total), 201

@app.route('/iteraciones/cambios-pagina', methods=['POST'])
def registrar_cambio_pagina():
    cuerpo = request.get_json()
    p_i = cuerpo.get('pagina_inicial')
    p_d = cuerpo.get('pagina_destino')
    id_s = cuerpo.get('id_sesion')

    if not id_s or not p_i or not p_d:
        return jsonify({"error": "Faltan parámetros en el cuerpo."}), 400
    
    sesion = Sesion.query.get(id_s)
    if not sesion:
        return jsonify({"error": "Sesión no encontrada."}), 404
    
    nueva_iteracion = Iteracion(id_sesion=id_s, id_evento=2, tiempo=datetime.now())
    db.session.add(nueva_iteracion)
    db.session.commit()
    
    id_it = nueva_iteracion.id

    nuevo_cambio_pagina = Cambio_pagina(id_iteracion=id_it, pagina_inicial=p_i, pagina_destino=p_d)
    db.session.add(nuevo_cambio_pagina)
    db.session.commit()
    
    diccionario_total = nueva_iteracion.to_dict()
    diccionario_total.update(nuevo_cambio_pagina.to_dict())

    return jsonify(diccionario_total), 201

@app.route('/iteraciones/formularios', methods=['POST'])
def registrar_interaccion_formulario():
    cuerpo = request.get_json()
    p = cuerpo.get('pregunta')
    r = cuerpo.get('respuesta')
    id_s = cuerpo.get('id_sesion')

    if not id_s or not p:
        return jsonify({"error": "Faltan parámetros en el cuerpo."}), 400
    
    sesion = Sesion.query.get(id_s)
    if not sesion:
        return jsonify({"error": "Sesión no encontrada."}), 404
    
    nueva_iteracion = Iteracion(id_sesion=id_s, id_evento=3, tiempo=datetime.now())
    db.session.add(nueva_iteracion)
    db.session.commit()
    
    id_it = nueva_iteracion.id

    nueva_interaccion_formulario = Formulario(id_iteracion=id_it, pregunta=p, respuesta=r)
    db.session.add(nueva_interaccion_formulario)
    db.session.commit()
    
    diccionario_total = nueva_iteracion.to_dict()
    diccionario_total.update(nueva_interaccion_formulario.to_dict())    

    return jsonify(diccionario_total), 201

# Rutas de la API para Consultar

@app.route('/sesiones', methods=['GET'])
def obtener_todas_sesiones():
    sesiones = Sesion.query.all()
    sesiones_dict = [sesion.to_dict() for sesion in sesiones]
    return jsonify(sesiones_dict), 200

@app.route('/iteraciones/elementos', methods=['GET'])
def obtener_todos_elementos():
    interacciones = Interaccion_elemento.query.all()
    interacciones_dict = [interaccion.to_dict() for interaccion in interacciones]
    return jsonify(interacciones_dict), 200

@app.route('/iteraciones/cambios-pagina', methods=['GET'])
def obtener_todas_paginas():
    cambios = Cambio_pagina.query.all()
    cambios_dict = [cambio.to_dict() for cambio in cambios]
    return jsonify(cambios_dict), 200

@app.route('/iteraciones/formularios', methods=['GET'])
def obtener_todos_formularios():
    interacciones = Formulario.query.all()
    interacciones_dict = [interaccion.to_dict() for interaccion in interacciones]
    return jsonify(interacciones_dict), 200

@app.route('/iteraciones', methods=['GET'])
def obtener_todas_iteraciones():
    iteraciones = Iteracion.query.all()
    iteraciones_dict = [iteracion.to_dict() for iteracion in iteraciones]
    return jsonify(iteraciones_dict), 200

@app.route('/sesiones/usuario', methods=['GET'])
def obtener_sesiones_finalizadas_por_direccion_mac():
    cuerpo = request.get_json()
    direccion_mac = cuerpo.get('direccion_mac')

    if not direccion_mac:
        return jsonify({"error": "Falta el parámetro direccion_mac en el cuerpo."}), 400

    sesiones = Sesion.query.filter_by(direccion_mac=direccion_mac).filter(Sesion.tiempo_salida.isnot(None)).all()
    sesiones_dict = [sesion.to_dict() for sesion in sesiones]
    return jsonify(sesiones_dict), 200

@app.route('/iteraciones/sesion', methods=['GET'])
def obtener_iteraciones_por_id_sesion():
    cuerpo = request.get_json()
    id_s = cuerpo.get('id_sesion')

    if not id_s:
        return jsonify({"error": "Falta el parámetro id_sesion en el cuerpo."}), 400

    iteraciones = Iteracion.query.filter_by(id_sesion=id_s).all()
    iteraciones_dict = [iteracion.to_dict() for iteracion in iteraciones]
    return jsonify(iteraciones_dict), 200

@app.route('/estadisticas/visitas/totales', methods=['GET'])
def get_visitas_totales():
    total_visitas = Sesion.query.count()
    return jsonify(total_visitas), 200

@app.route('/estadisticas/visitantes-unicos', methods=['GET'])
def get_visitantes_unicos():
    visitantes_unicos = db.session.query(Sesion.direccion_mac).distinct().count()
    return jsonify(visitantes_unicos), 200

@app.route('/estadisticas/visitas/promedio-por-usuario', methods=['GET'])
def get_visitas_medio_usuario():
    total_visitas = Sesion.query.count()
    visitantes_unicos = db.session.query(Sesion.direccion_mac).distinct().count()

    if visitantes_unicos == 0:
        visitas_medias = 0
    else:
        visitas_medias = total_visitas / visitantes_unicos

    return jsonify(round(visitas_medias, 2)), 200

@app.route('/estadisticas/tiempo/promedio-por-usuario', methods=['GET'])
def get_tiempo_medio_usuario():
    sesiones = Sesion.query.filter(Sesion.tiempo_salida.isnot(None)).all()

    if not sesiones:
        return jsonify(0), 200

    total_tiempo = sum((sesion.tiempo_salida - sesion.tiempo_entrada).total_seconds() for sesion in sesiones if sesion.tiempo_entrada and sesion.tiempo_salida)
    total_sesiones = len(sesiones)

    tiempo_medio = total_tiempo / total_sesiones if total_sesiones > 0 else 0

    return jsonify(round(tiempo_medio, 2)), 200

@app.route('/estadisticas/elemento-mas-iteraciones', methods=['GET'])
def obtener_elemento_con_mas_interacciones():
    # Realiza la consulta para contar las interacciones por cada tag_elemento
    interacciones_por_tag = db.session.query(
        Interaccion_elemento.tag_elemento,
        func.count(Interaccion_elemento.id).label('interacciones')
    ).group_by(Interaccion_elemento.tag_elemento).order_by(func.count(Interaccion_elemento.id).desc()).first()

    if interacciones_por_tag:
        # Si hay interacciones, devolvemos el tag con más interacciones
        return jsonify({
            'tag_elemento': interacciones_por_tag.tag_elemento,
            'interacciones': interacciones_por_tag.interacciones
        }), 200
    else:
        return jsonify({"error": "No hay interacciones registradas."}), 404

@app.route('/estadisticas/tasa-rebote', methods=['GET'])
def calcular_tasa_rebote():
    # Obtener todas las sesiones finalizadas
    sesiones = Sesion.query.filter(Sesion.tiempo_salida.isnot(None)).all()

    # Contar el número total de sesiones
    total_sesiones = len(sesiones)

    if total_sesiones == 0:
        return jsonify({"error": "No hay sesiones registradas."}), 404

    # Contar el número de sesiones de rebote
    sesiones_rebote = 0

    for sesion in sesiones:
        # Verificar si hay algún cambio de página (primer evento de la sesión)
        cambios = Cambio_pagina.query.join(Iteracion).filter(Iteracion.id_sesion == sesion.id).all()
        interacciones = Interaccion_elemento.query.join(Iteracion).filter(Iteracion.id_sesion == sesion.id).all()

        # Si no hay cambios de página ni interacciones con elementos (es una sesión de rebote)
        if len(cambios) == 0 and len(interacciones) == 0:
            sesiones_rebote += 1

    # Calcular la tasa de rebote
    tasa_rebote = (sesiones_rebote / total_sesiones) * 100
    return jsonify(tasa_rebote), 200

@app.route('/estadisticas/paginas/promedio-por-sesion', methods=['GET'])
def obtener_numero_medio_paginas():
    # Obtener todas las sesiones finalizadas
    sesiones = Sesion.query.filter(Sesion.tiempo_salida.isnot(None)).all()

    # Contar el número total de sesiones
    total_sesiones = len(sesiones)

    if total_sesiones == 0:
        return jsonify({"error": "No hay sesiones registradas."}), 404

    # Contar el número total de cambios de página
    total_cambios_pagina = 0

    for sesion in sesiones:
        # Contar los cambios de página en cada sesión
        cambios = Cambio_pagina.query.join(Iteracion).filter(Iteracion.id_sesion == sesion.id).all()
        
        # El número de páginas visitadas es el número de cambios de página + 1 (por la página inicial)
        total_cambios_pagina += len(cambios) + 1

    # Calcular el número medio de páginas visitadas
    numero_medio_paginas = total_cambios_pagina / total_sesiones

    return jsonify(numero_medio_paginas), 200

@app.route('/estadisticas/iteraciones/promedio-por-usuario', methods=['GET'])
def obtener_numero_interacciones_por_usuario():
    # Obtener todas las sesiones finalizadas
    sesiones = Sesion.query.filter(Sesion.tiempo_salida.isnot(None)).all()

    if not sesiones:
        return jsonify({"error": "No hay sesiones registradas."}), 404

    total_interacciones = 0
    total_usuarios = 0

    # Contar el número de interacciones por sesión
    for sesion in sesiones:
        # Contar interacciones con elementos
        interacciones_elementos = Interaccion_elemento.query.join(Iteracion).filter(Iteracion.id_sesion == sesion.id).all()
        
        # Contar cambios de página
        cambios_pagina = Cambio_pagina.query.join(Iteracion).filter(Iteracion.id_sesion == sesion.id).all()
        
        # Contar interacciones en formularios
        interacciones_formularios = Formulario.query.join(Iteracion).filter(Iteracion.id_sesion == sesion.id).all()
        
        # Sumar todas las interacciones de la sesión
        total_interacciones += len(interacciones_elementos) + len(cambios_pagina) + len(interacciones_formularios)
        total_usuarios += 1

    if total_usuarios == 0:
        return jsonify({"error": "No hay usuarios registrados."}), 404

    # Calcular el número medio de interacciones por usuario
    numero_medio_interacciones = total_interacciones / total_usuarios

    return jsonify(numero_medio_interacciones), 200

@app.route('/sesiones/direcciones-mac', methods=['GET'])
def obtener_direcciones_mac_unicas():
    direcciones_mac = db.session.query(Sesion.direccion_mac).distinct().all()
    direcciones_mac_lista = [direccion[0] for direccion in direcciones_mac]
    return jsonify(direcciones_mac_lista), 200

@app.route('/estadisticas/visitas/ultimos-30-dias', methods=['POST'])
def visitas_ultimos_30_dias():
    data = request.get_json()
    direccion_mac = data.get("direccion_mac") if data else None
    
    # Fecha de inicio (hace 30 días)
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    # Construcción de la consulta
    query = db.session.query(func.date(Sesion.tiempo_entrada), func.count(Sesion.id))
    query = query.filter(Sesion.tiempo_entrada >= fecha_inicio)
    
    if direccion_mac:
        query = query.filter(Sesion.direccion_mac == direccion_mac)
    
    query = query.group_by(func.date(Sesion.tiempo_entrada))
    visitas = query.all()
    
    # Crear un diccionario con todos los días en los últimos 30 días con valor 0
    visitas_dict = {
        (fecha_inicio + timedelta(days=i)).date().isoformat(): 0 for i in range(30)
    }
    
    # Actualizar con los valores reales obtenidos de la base de datos
    for fecha, cantidad in visitas:
        visitas_dict[str(fecha)] = cantidad
    
    return jsonify(visitas_dict), 200

@app.route('/estadisticas/navegadores/porcentajes', methods=['GET'])
def navegadores_uso():
    # Obtener el número de sesiones por navegador
    navegador_data = (
        db.session.query(Sesion.navegador, func.count(Sesion.id))
        .group_by(Sesion.navegador)
        .all()
    )
    
    # Calcular el total de sesiones
    total_sesiones = sum(cantidad for _, cantidad in navegador_data)
    
    # Crear un diccionario con los porcentajes de uso
    navegador_dict = {
        navegador: round((cantidad / total_sesiones) * 100, 2) if total_sesiones > 0 else 0
        for navegador, cantidad in navegador_data
    }
    
    return jsonify(navegador_dict), 200

@app.route('/estadisticas/zonas-horarias/porcentajes', methods=['GET'])
def zonas_horarias_uso():
    # Obtener el número de sesiones por zona horaria
    zona_horaria_data = (
        db.session.query(Sesion.zona_horaria, func.count(Sesion.id))
        .group_by(Sesion.zona_horaria)
        .all()
    )
    
    # Calcular el total de sesiones
    total_sesiones = sum(cantidad for _, cantidad in zona_horaria_data)
    
    # Crear un diccionario con los porcentajes de uso de las zonas horarias
    zona_horaria_dict = {
        zona_horaria: round((cantidad / total_sesiones) * 100, 2) if total_sesiones > 0 else 0
        for zona_horaria, cantidad in zona_horaria_data
    }
    
    return jsonify(zona_horaria_dict), 200

@app.route('/estadisticas/visitas/acumuladas', methods=['POST'])
def visitas_acumuladas():
    data = request.get_json()
    direccion_mac = data.get("direccion_mac") if data else None
    
    # Fecha de inicio (hace 30 días)
    fecha_inicio = (datetime.now() - timedelta(days=30)).date()
    fecha_fin = datetime.now().date()
    
    # Construcción de la consulta
    query = db.session.query(func.date(Sesion.tiempo_entrada), func.count(Sesion.id))
    query = query.filter(Sesion.tiempo_entrada >= fecha_inicio)
    
    if direccion_mac:
        query = query.filter(Sesion.direccion_mac == direccion_mac)
    
    query = query.group_by(func.date(Sesion.tiempo_entrada))
    visitas = dict(query.all())  # Convertir el resultado en un diccionario {fecha: cantidad}
    
    # Acumular visitas día a día
    visitas_acumuladas = 0
    visitas_dict = {}
    
    for i in range(31):  # Para incluir hoy también
        fecha = (fecha_inicio + timedelta(days=i)).isoformat()
        visitas_acumuladas += visitas.get(fecha, 0)  # Sumar las visitas del día si existen
        visitas_dict[fecha] = visitas_acumuladas  # Guardar el valor acumulado

    return jsonify(visitas_dict), 200

@app.route('/estadisticas/tiempo/acumulado', methods=['GET'])
def tiempo_medio_acumulado():
    # Fecha de inicio (hace 30 días)
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    # Consultar las sesiones para obtener el tiempo medio por día
    sesiones = (
        db.session.query(
            func.date(Sesion.tiempo_entrada),  # Agrupar por fecha
            func.sum(func.julianday(Sesion.tiempo_salida) - func.julianday(Sesion.tiempo_entrada)).label('tiempo_total')
        )
        .filter(Sesion.tiempo_entrada >= fecha_inicio)
        .filter(Sesion.tiempo_salida.isnot(None))  # Solo sesiones que han finalizado
        .group_by(func.date(Sesion.tiempo_entrada))
        .all()
    )

    # Calcular el tiempo medio por día
    tiempo_medio_dict = {
        str(fecha): round(tiempo_total / len(sesiones), 2) if len(sesiones) > 0 else 0
        for fecha, tiempo_total in sesiones
    }
    
    return jsonify(tiempo_medio_dict), 200

@app.route('/estadisticas/tiempo/promedio-por-dia', methods=['POST'])
def tiempo_medio_por_dia():
    data = request.get_json()
    direccion_mac = data.get("direccion_mac") if data else None
    
    # Fecha de inicio (hace 30 días)
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    # Obtener todas las fechas de los últimos 30 días
    fechas_ultimos_30_dias = [
        (fecha_inicio + timedelta(days=i)).date().isoformat() for i in range(30)
    ]
    
    # Construcción de la consulta
    query = db.session.query(
        func.date(Sesion.tiempo_entrada),  # Agrupar por fecha
        func.avg(func.julianday(Sesion.tiempo_salida) - func.julianday(Sesion.tiempo_entrada)).label('tiempo_medio')
    ).filter(Sesion.tiempo_entrada >= fecha_inicio)
    
    if direccion_mac:
        query = query.filter(Sesion.direccion_mac == direccion_mac)
    
    query = query.filter(Sesion.tiempo_salida.isnot(None))  # Solo sesiones que han finalizado
    query = query.group_by(func.date(Sesion.tiempo_entrada))
    
    sesiones = query.all()
    
    # Crear un diccionario con todas las fechas y tiempo medio 0 por defecto
    tiempo_medio_dict = {fecha: 0 for fecha in fechas_ultimos_30_dias}
    
    # Actualizar el diccionario con los tiempos medios calculados
    for fecha, tiempo_medio in sesiones:
        tiempo_medio_dict[str(fecha)] = round(tiempo_medio * 1440, 2)  # Convertir de días a minutos
    
    return jsonify(tiempo_medio_dict), 200

@app.route('/estadisticas/datos-flujo', methods=['GET'])
def obtener_datos_sankey():
    # Obtener todos los cambios de página
    cambios_pagina = db.session.query(Cambio_pagina).all()
    
    # Crear un diccionario para contar los flujos de usuarios entre páginas
    flujos = {}
    total_usuarios = 0  # Contador de total de usuarios

    for cambio in cambios_pagina:
        origen = cambio.pagina_inicial
        destino = cambio.pagina_destino
        
        # Inicializamos las claves si no existen
        if origen not in flujos:
            flujos[origen] = {}
        if destino not in flujos[origen]:
            flujos[origen][destino] = 0
        
        # Incrementamos el contador de usuarios entre estas dos páginas
        flujos[origen][destino] += 1
        total_usuarios += 1  # Incrementamos el total de usuarios

    # Convertir el diccionario de flujos en el formato adecuado para el gráfico
    rows = []
    for origen, destinos in flujos.items():
        for destino, usuarios in destinos.items():
            # Calcular el porcentaje en lugar de devolver el número de usuarios
            porcentaje = (usuarios / total_usuarios) * 100
            rows.append({
                'origen': str(origen),  # Convertir a string para el gráfico
                'destino': str(destino),  # Convertir a string para el gráfico
                'porcentaje': round(porcentaje, 2)  # Devolver el porcentaje con 2 decimales
            })
    
    # Retornar los datos en formato JSON
    return jsonify(rows)

@app.route('/iteraciones/sesion', methods=['POST'])
def interacciones_sesion():
    data = request.get_json()
    id_sesion = data.get('id_sesion')

    if not id_sesion:
        return jsonify({"error": "Falta el parámetro id_sesion"}), 400

    # Consultamos las iteraciones relacionadas con la sesión
    iteraciones = db.session.query(
        Iteracion.tiempo,
        Iteracion.id_evento,
        Interaccion_elemento.tag_elemento,
        Cambio_pagina.pagina_inicial,
        Cambio_pagina.pagina_destino,
        Formulario.pregunta,
        Formulario.respuesta
    ).outerjoin(
        Interaccion_elemento, Interaccion_elemento.id_iteracion == Iteracion.id
    ).outerjoin(
        Cambio_pagina, Cambio_pagina.id_iteracion == Iteracion.id
    ).outerjoin(
        Formulario, Formulario.id_iteracion == Iteracion.id
    ).filter(
        Iteracion.id_sesion == id_sesion
    ).order_by(Iteracion.tiempo.asc()).all()

    # Preparamos la respuesta
    resultado = []
    for iteracion in iteraciones:
        evento_dict = {
            'tiempo': iteracion.tiempo,
            'tipo_evento': 'interaccion' if iteracion.id_evento == 1 else 'cambio_pagina' if iteracion.id_evento == 2 else 'formulario'
        }

        if iteracion.id_evento == 1:  # Interacción con un elemento
            evento_dict['elemento'] = iteracion.tag_elemento
        elif iteracion.id_evento == 2:  # Cambio de página
            evento_dict['pagina_inicial'] = iteracion.pagina_inicial
            evento_dict['pagina_destino'] = iteracion.pagina_destino
        elif iteracion.id_evento == 3:  # Formulario
            evento_dict['pregunta'] = iteracion.pregunta
            evento_dict['respuesta'] = iteracion.respuesta

        resultado.append(evento_dict)

    return jsonify(resultado), 200

@app.route('/sesiones/tiempo/direcciones-mac', methods=['POST'])
def obtener_sesiones_por_mac():
    cuerpo = request.get_json()
    direccion_mac = cuerpo.get('direccion_mac')

    if not direccion_mac:
        return jsonify({"error": "Falta el parámetro direccion_mac en el cuerpo."}), 400

    # Ordenar las sesiones por 'tiempo_entrada' de manera descendente
    sesiones = db.session.query(Sesion.id, Sesion.tiempo_entrada).filter_by(direccion_mac=direccion_mac).order_by(Sesion.tiempo_entrada.desc()).all()
    
    # Formatear las sesiones a una lista de diccionarios
    resultado = [{'id': s.id, 'tiempo_entrada': s.tiempo_entrada.isoformat()} for s in sesiones]

    return jsonify(resultado), 200

# Creación de la base de datos antes de iniciar la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen
    app.run(debug=True)