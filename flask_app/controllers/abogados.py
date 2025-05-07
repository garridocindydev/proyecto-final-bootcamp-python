from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.juicio import Juicio
from flask_app.models.usuario import Usuario
from flask_app.models.mensaje import Mensaje

@app.route('/abogado/dashboard')
def ver_dashboard_abogado():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    # Obtener los juicios asignados al abogado
    juicios = Juicio.obtener_por_abogado(session['usuario_id'])
    return render_template('abogado/dashboard.html', juicios=juicios)

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
    return render_template('abogado/juicios.html', juicios=juicios, incautadores=incautadores, abogados=abogados)

@app.route('/abogado/juicios/<int:juicio_id>/asignar_incautador', methods=['POST'])
def asignar_incautador(juicio_id):
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    juicio_id = request.form['juicio_id']
    incautador_id = request.form['incautador_id']
    
    Juicio.asignar_incautador(juicio_id, incautador_id)
    flash('Incautador asignado exitosamente', 'success')
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
    return render_template('abogado/comentarios.html', asignaciones=asignaciones)
    return redirect('/abogado/juicios')

@app.route('/abogado/mensajes/<int:juicio_id>')
def ver_mensajes(juicio_id):
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    mensajes = Mensaje.obtener_por_juicio(juicio_id)
    juicio = Juicio.obtener_por_id(juicio_id)
    return render_template('abogado/mensajes.html', mensajes=mensajes, juicio=juicio)
