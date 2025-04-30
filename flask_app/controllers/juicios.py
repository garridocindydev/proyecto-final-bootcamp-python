from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.juicio import Juicio

@app.route('/financiera')
def financiera():
    # if 'user_id' not in session:
    #     return redirect('/')
    juicios = Juicio.obtener_todos()
    return render_template('financiera.html', juicios=juicios)


@app.route('/crear_juicio', methods=['POST'])
def crear_juicio():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Juicio.validar_juicio(request.form):
        return redirect('/financiera')
    
    data = {
        'id_pagare': request.form['id_pagare'],
        'rol': request.form['rol'],
        'tribunal': request.form['tribunal'],
        'cuantia': request.form['cuantia']
    }
    
    Juicio.crear_juicio(data)
    flash('Juicio creado exitosamente', 'success')
    return redirect('/financiera')

@app.route('/asignar_juicio/<int:juicio_id>', methods=['POST'])
def asignar_juicio(juicio_id):
    if 'user_id' not in session:
        return redirect('/')
    
    estudio_id = request.form['estudio']
    Juicio.asignar_estudio(juicio_id, estudio_id)
    flash('Juicio asignado exitosamente', 'success')
    return redirect('/financiera')

@app.route('/terminar_juicio/<int:juicio_id>', methods=['POST'])
def terminar_juicio(juicio_id):
    if 'user_id' not in session:
        return redirect('/')
    
    Juicio.terminar_juicio(juicio_id)
    flash('Juicio terminado exitosamente', 'success')
    return redirect('/financiera')
