from flask import render_template, request, redirect, session, flash, jsonify
from flask_app import app
from flask_app.models.asignacion import Asignacion, Comentario
from functools import wraps

def incautador_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session or session.get('rol') != 'incautador':
            flash("Acceso no autorizado", "error")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/incautador/asignaciones')
@incautador_required
def lista_asignaciones():
    asignaciones = Asignacion.get_asignaciones_incautador(session['usuario_id'])
    return render_template('incautador/asignaciones.html', asignaciones=asignaciones)

@app.route('/incautador/asignacion/<int:id>/estado', methods=['POST'])
@incautador_required
def actualizar_estado_asignacion(id):
    nuevo_estado = request.form.get('estado')
    observaciones = request.form.get('observaciones')
    
    if nuevo_estado not in ['Pendiente', 'En_Proceso', 'Ejecutado', 'Fallido']:
        flash("Estado inválido", "error")
        return redirect('/incautador/asignaciones')
    
    Asignacion.actualizar_estado(id, nuevo_estado, observaciones)
    flash("Estado actualizado exitosamente", "success")
    return redirect('/incautador/asignaciones')

@app.route('/incautador/asignacion/<int:id>/comentario', methods=['POST'])
@incautador_required
def agregar_comentario(id):
    if not request.form.get('comentario'):
        flash("El comentario no puede estar vacío", "error")
        return redirect('/incautador/asignaciones')
    
    data = {
        'asignacion_id': id,
        'incautador_id': session['usuario_id'],
        'comentario': request.form.get('comentario'),
        'tipo_comentario': request.form.get('tipo_comentario', 'Otro')
    }
    
    Comentario.crear(data)
    flash("Comentario agregado exitosamente", "success")
    return redirect('/incautador/asignaciones')
