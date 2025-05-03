from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.juicio import Juicio
from flask_app.models.usuario import Usuario
from flask_app.models.mensaje import Mensaje

@app.route('/abogado/dashboard')
def abogado_dashboard():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    # Obtener los juicios asignados al abogado
    juicios = Juicio.obtener_por_abogado(session['usuario_id'])
    return render_template('abogado/dashboard.html', juicios=juicios)

@app.route('/abogado/juicios')
def abogado_juicios():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    juicios = Juicio.obtener_por_abogado(session['usuario_id'])
    incautadores = Usuario.get_by_role('incautador')
    return render_template('abogado/juicios.html', juicios=juicios, incautadores=incautadores)

@app.route('/abogado/juicio/asignar_incautador', methods=['POST'])
def asignar_incautador():
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    juicio_id = request.form['juicio_id']
    incautador_id = request.form['incautador_id']
    
    Juicio.asignar_incautador(juicio_id, incautador_id)
    flash('Incautador asignado exitosamente', 'success')
    return redirect('/abogado/juicios')

@app.route('/abogado/mensajes/<int:juicio_id>')
def ver_mensajes(juicio_id):
    if 'usuario_id' not in session or session.get('rol') not in ['abogado', 'super_abogado']:
        return redirect('/')
    
    mensajes = Mensaje.obtener_por_juicio(juicio_id)
    juicio = Juicio.obtener_por_id(juicio_id)
    return render_template('abogado/mensajes.html', mensajes=mensajes, juicio=juicio)
