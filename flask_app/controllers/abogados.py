from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app
from flask_app.models.juicio import Juicio
from flask_app.models.usuario import Usuario
from flask_app.models.notificacion import Notificacion

@app.route('/abogado/dashboard')
def ver_dashboard_abogado():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    # Obtener los juicios asignados al abogado
    juicios = Juicio.obtener_por_abogado(session['usuario_id'])
    # Obtener el conteo de notificaciones no leídas
    notificaciones_count = Notificacion.contar_no_leidas(session['usuario_id'])
    return render_template('abogado/dashboard.html', juicios=juicios, notificaciones_count=notificaciones_count)

@app.route('/abogado/juicios')
def abogado_juicios():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    # Si es super_abogado, obtiene todos los juicios, si no, solo los suyos
    if session.get('rol') == 'super_abogado':
        juicios = Juicio.obtener_todos()
    else:
        juicios = Juicio.obtener_por_abogado(session['usuario_id'])
    
    incautadores = Usuario.get_by_role('incautador')
    abogados = Usuario.get_by_role('abogado')  # Get list of attorneys
    notificaciones_count = Notificacion.contar_no_leidas(session['usuario_id'])
    return render_template('abogado/juicios.html',
                         rol_usuario=session.get('rol'),
                         juicios=juicios,
                         incautadores=incautadores,
                         abogados=abogados,
                         notificaciones_count=notificaciones_count)

@app.route('/abogado/juicios/<int:juicio_id>/asignar_incautador', methods=['POST'])
def asignar_incautador(juicio_id):
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    incautador_id = request.form['incautador_id']
    
    Juicio.asignar_incautador(juicio_id, incautador_id)
    flash('Incautador actualizado exitosamente', 'success')
    return redirect('/abogado/juicios')

@app.route('/asignar_abogado/juicios/<int:juicio_id>', methods=['POST'])
def asignar_abogado_al_juicio(juicio_id):
    if 'usuario_id' not in session or session.get('rol') not in ['super_abogado']:
        return redirect('/')
    
    abogado_id = request.form['abogado_id']
    
    Juicio.asignar_abogado(juicio_id, abogado_id)
    flash('Abogado asignado exitosamente al juicio', 'success')
    return redirect('/abogado/juicios')

@app.route('/abogado/comentarios')
def ver_comentarios_incautador():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    # Obtener las asignaciones y sus comentarios para el abogado
    from flask_app.models.asignacion import Asignacion
    asignaciones = Asignacion.get_asignaciones_con_comentarios(session['usuario_id'])
    notificaciones_count = Notificacion.contar_no_leidas(session['usuario_id'])
    return render_template('abogado/comentarios.html',
                         asignaciones=asignaciones,
                         notificaciones_count=notificaciones_count)

@app.route('/abogado/mensajes/<int:juicio_id>')
def ver_mensajes(juicio_id):
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    mensajes = Mensaje.obtener_por_juicio(juicio_id)
    juicio = Juicio.obtener_por_id(juicio_id)
    notificaciones_count = Notificacion.contar_no_leidas(session['usuario_id'])
    return render_template('abogado/mensajes.html',
                         mensajes=mensajes,
                         juicio=juicio,
                         notificaciones_count=notificaciones_count)

@app.route('/abogado/notificaciones')
def obtener_notificaciones():
    if 'usuario_id' not in session:
        return jsonify([])
    
    notificaciones = Notificacion.obtener_no_leidas(session['usuario_id'])
    notificaciones_json = []
    
    for notif in notificaciones:
        if notif.comentario:
            fecha = notif.created_at.strftime('%d/%m/%Y %H:%M') if notif.created_at else ''
            
            notificaciones_json.append({
                'id': notif.id,
                'mensaje': notif.comentario.comentario,
                'incautador': notif.comentario.incautador_nombre,
                'asignacion_id': notif.comentario.asignacion_id,
                'tipo': notif.comentario.tipo_comentario,
                'fecha': fecha
            })
    
    return jsonify(notificaciones_json)

@app.route('/abogado/notificaciones/<int:notificacion_id>/leer', methods=['POST'])
def marcar_notificacion_leida(notificacion_id):
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return jsonify({'error': 'No autorizado'}), 401
    
    Notificacion.marcar_como_leida(notificacion_id)
    return jsonify({'success': True})
