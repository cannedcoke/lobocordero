
# ======== IMPORTACIONES ========
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from conexion import app, db
from models import Respuesta, Politico, Pregunta, Proyecto
from sqlalchemy import func
from sqlalchemy.orm import joinedload

app.secret_key = 'clave-segura'


# ======== RUTAS BÁSICAS ========

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


# ======== ENCUESTA ========
@app.route('/encuesta')
@app.route('/encuesta/<int:id_politico>', methods=['GET', 'POST'])
def encuesta(id_politico=None):
    if id_politico is None:
        p_first = Politico.query.first()
        if not p_first:
            return '<h2>No hay políticos cargados</h2>', 404
        return redirect(url_for('encuesta', id_politico=p_first.id))

    politico = Politico.query.get_or_404(id_politico)

    if request.method == 'POST':
        for i in range(1, 8):
            opinion_valor = request.form.get(f'preg{i}')
            if not opinion_valor:
                continue
            db.session.add(Respuesta(
                id_politico=id_politico,
                id_pregunta=i,
                id_opinion=int(opinion_valor)
            ))
        db.session.commit()
        flash('Encuesta guardada correctamente.')
        redirect_url = request.form.get('redirect_url') or url_for('mostrar_encuesta')
        return redirect(redirect_url)

    if Pregunta.query.count() == 0:
        for t in [
            "¿Cumple con sus promesas?",
            "¿Nivel de transparencia?",
            "¿Usa correctamente los recursos?",
            "¿Volverías a votarlo?",
            "¿Compromiso con el bienestar ciudadano?",
            "¿Rinde cuentas ante la ciudadanía?",
            "¿Palabra que lo describe mejor?"
        ]:
            db.session.add(Pregunta(descripcion=t))
        db.session.commit()

    preguntas = Pregunta.query.all()
    mensajes = get_flashed_messages()
    return render_template('encuesta.html', p=politico, preguntas=preguntas, mensajes=mensajes)


# ======== RESULTADOS ========
@app.route('/resultados/<int:id_politico>')
def resultados_por_politico(id_politico):
    politico = Politico.query.get_or_404(id_politico)
    preguntas = Pregunta.query.all()
    data = []

    for pregunta in preguntas:
        conteos = (
            db.session.query(Respuesta.id_opinion, func.count(Respuesta.id_respuesta))
            .filter(
                Respuesta.id_pregunta == pregunta.id_pregunta,
                Respuesta.id_politico == id_politico
            )
            .group_by(Respuesta.id_opinion)
            .all()
        )
        labels = [f"Opción {c[0]}" for c in conteos]
        valores = [c[1] for c in conteos]
        data.append({
            "pregunta": pregunta.descripcion,
            "labels": labels,
            "valores": valores
        })

    return render_template('resultados.html', resultados=data, politico=politico)


# ======== CARGA INICIAL ========
def cargar_politicos_si_no_existen():
    datos = [
        {
            "nombre": "Fernando Armindo Lugo Méndez",
            "partido": "Frente Guasú",
            "titulo": "Expresidente",
            "foto": "lugo.png",
            "proyectos": [
                {"titulo": "Impuesto a la soja", "descripcion": "Propuso nuevos impuestos a la exportación de soja para mejorar la distribución de la tierra."},
                {"titulo": "Reforma agraria", "descripcion": "Prometió una reforma agraria para mejorar la distribución de la tierra en Paraguay, pero enfrentó bloqueos parlamentarios y no avanzó."},
                {"titulo": "Lucha contra la corrupción", "descripcion": "Se propuso luchar contra el clientelismo y la corrupción en el gobierno."},
                {"titulo": "Promesa incumplida: Reforma agraria", "descripcion": "Compromiso central de su gobierno que no prosperó por oposición legislativa y fue truncado por su destitución en 2012."}
            ]
        },
        {
            "nombre": "Santiago Peña Palacios",
            "partido": "Partido Colorado – Honor Colorado",
            "titulo": "Presidente",
            "foto": "pena.png",
            "proyectos": [
                {"titulo": "Hospital de Itauguá", "descripcion": "Proyecto para convertir el Hospital Nacional en un centro de referencia internacional."},
                {"titulo": "Promesa incumplida: 500.000 nuevos puestos de trabajo", "descripcion": "Comprometió crear medio millón de empleos en su primer año, pero el desempleo aumentó."},
                {"titulo": "Promesa incumplida: Política exterior efectiva – cobro a Argentina por energía", "descripcion": "Prometió gestionar cobros por energía de Itaipú, pero no logró concretar los pagos."}
            ]
        },
        {
            "nombre": "Silvio Adalberto Ovelar Benítez",
            "partido": "Partido Colorado",
            "titulo": "Senador",
            "foto": "silvio.png",
            "proyectos": [
                {"titulo": "Letrina Cero", "descripcion": "Plan para reemplazar letrinas por baños sexados en escuelas, con ampliación presupuestaria para el MEC."},
                {"titulo": "PGN 2026", "descripcion": "Lideró el estudio del PGN 2026 priorizando salud y educación."},
                {"titulo": "Prevención de violencia adolescente", "descripcion": "Proyecto para prevenir la violencia adolescente con talleres y campañas."},
                {"titulo": "Promesa incumplida: Planillerismo y falta de respuestas institucionales", "descripcion": "Fue criticado por justificar casos de planillerismo en instituciones públicas sin respuestas efectivas."}
            ]
        },
        {
            "nombre": "Esperanza Martínez Lleida de Portillo",
            "partido": "Frente Guasú",
            "titulo": "Senadora",
            "foto": "esperanza.png",
            "proyectos": [
                {"titulo": "Ley de etiquetado OGM", "descripcion": "Obliga a identificar productos con organismos genéticamente modificados."},
                {"titulo": "Protección a periodistas", "descripcion": "Establece medidas para proteger a periodistas y defensores de derechos humanos."},
                {"titulo": "Prohibición de cianuro en minería", "descripcion": "Elimina el uso de cianuro en la minería para cuidar el ambiente."},
                {"titulo": "Promesa incumplida: Discursos frente a la realidad social", "descripcion": "Criticó al gobierno por promesas sociales incumplidas y falta de políticas efectivas en salud y bienestar."}
            ]
        },
        {
            "nombre": "Basilio 'Bachi' Núñez",
            "partido": "Partido Colorado – Honor Colorado",
            "titulo": "Senador",
            "foto": "basilio.png",
            "proyectos": [
                {"titulo": "Control del espacio aéreo", "descripcion": "Permitir el derribo o control firme de aeronaves ilícitas."},
                {"titulo": "Regulación de IA en Paraguay", "descripcion": "Propuesta para un marco legal de privacidad y transparencia en IA."},
                {"titulo": "Protección de Datos Personales", "descripcion": "Busca asegurar derechos ciudadanos en la nueva norma de datos personales."},
                {"titulo": "Promesa incumplida: Más viajes que cumplimiento", "descripcion": "Se le critica por priorizar viajes y exposición mediática sobre resultados legislativos concretos."}
            ]
        },
        {
            "nombre": "Raúl Latorre",
            "partido": "Partido Colorado – Honor Colorado",
            "titulo": "Diputado",
            "foto": "raul.png",
            "proyectos": [
                {"titulo": "Hambre Cero", "descripcion": "Programa que beneficia a más de un millón de niños en edad escolar."},
                {"titulo": "DNIT", "descripcion": "Creación de la Dirección Nacional de Ingresos Tributarios para mejorar recaudación."},
                {"titulo": "Modernización de defensa", "descripcion": "Impulsó la modernización de defensa nacional con radares y aviones Super Tucano."},
                {"titulo": "Promesa incumplida: Creación de empleo real", "descripcion": "Prometió generar trabajo y desarrollo, pero fue criticado por nepotismo y falta de resultados visibles."}
            ]
        },
        {
            "nombre": "Daniel Centurión",
            "partido": "Partido Colorado – Fuerza Republicana",
            "titulo": "Diputado",
            "foto": "daniel.png",
            "proyectos": [
                {"titulo": "Reforma del JEM", "descripcion": "Fortalece la independencia judicial en el Jurado de Enjuiciamiento de Magistrados."},
                {"titulo": "Ley de compensación económica", "descripcion": "Compensa a Asunción por su condición de capital mejorando infraestructura."},
                {"titulo": "Aumento de penas por corrupción", "descripcion": "Hasta 25 años para funcionarios en delitos graves."},
                {"titulo": "Promesa incumplida: Transparencia y rendición", "descripcion": "Prometió rendir cuentas en su gestión, pero no presentó resultados concretos ni informes públicos."}
            ]
        },
        {
            "nombre": "Mauricio Espínola",
            "partido": "Partido Colorado – Fuerza Republicana",
            "titulo": "Diputado",
            "foto": "mauricio.png",
            "proyectos": [
                {"titulo": "PRONARA", "descripcion": "Programa Nacional de Reproducción Asistida de acceso gratuito."},
                {"titulo": "Derechos humanos y jóvenes detenidos", "descripcion": "Promueve respeto a las libertades civiles."},
                {"titulo": "Fiscalización de fondos binacionales", "descripcion": "Promueve transparencia en Itaipú y Yacyretá."},
                {"titulo": "Promesa incumplida: Salud sin avances visibles", "descripcion": "Se le critica por falta de resultados en sus propuestas de salud pública y promesas no concretadas."}
            ]
        }
    ]

    for d in datos:
        existente = Politico.query.filter_by(nombre=d["nombre"]).first()
        if not existente:
            nuevo = Politico(
                nombre=d["nombre"],
                partido=d["partido"],
                titulo=d["titulo"],
                foto=d["foto"]
            )
            db.session.add(nuevo)
            db.session.commit()
            for p in d["proyectos"]:
                db.session.add(Proyecto(
                    id_politico=nuevo.id,
                    titulo=p["titulo"],
                    descripcion=p["descripcion"]
                ))
    db.session.commit()


# ======== FILTROS ========
@app.route("/mostrarencuesta")
def mostrar_encuesta():
    politicos = Politico.query.options(joinedload(Politico.proyectos)).all()
    proyectos = Proyecto.query.all()
    if not politicos:
        return '<h2>No hay políticos cargados</h2>', 404
    return render_template('politicos.html', politicos=politicos, proyectos=proyectos)

@app.route("/presidentes")
def mostrar_presidentes():
    presidentes = (
        Politico.query.options(joinedload(Politico.proyectos))
        .filter(Politico.titulo.ilike("%presidente%"))
        .all()
    )
    if not presidentes:
        return '<h2>No hay presidentes cargados</h2>', 404
    return render_template('politicos.html', politicos=presidentes)

@app.route("/diputados")
def mostrar_diputados():
    diputados = (
        Politico.query.options(joinedload(Politico.proyectos))
        .filter(Politico.titulo.ilike("%diputado%"))
        .all()
    )
    if not diputados:
        return '<h2>No hay diputados cargados</h2>', 404
    return render_template('politicos.html', politicos=diputados)

@app.route("/senadores")
def mostrar_senadores():
    senadores = (
        Politico.query.options(joinedload(Politico.proyectos))
        .filter(Politico.titulo.ilike("%senador%"))
        .all()
    )
    if not senadores:
        return '<h2>No hay senadores cargados</h2>', 404
    return render_template('politicos.html', politicos=senadores)


# ======== EJECUCIÓN PRINCIPAL ========
if __name__ == '__main__':
    with app.app_context():
        cargar_politicos_si_no_existen()
    app.run(debug=True)
