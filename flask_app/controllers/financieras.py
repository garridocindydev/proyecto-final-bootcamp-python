from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.juicio import Juicio
from functools import wraps

def financiera_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Por favor inicia sesión para acceder", "error")
            return redirect('/')
        
        if session.get('rol') not in ['admin', 'financiera']:
            flash("Acceso denegado. Se requieren privilegios de financiera o administrador.", "error")
            return redirect('/dashboard')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/financiera/juicios')
@financiera_admin_required
def financiera_juicios():
    juicios = Juicio.get_all()
    return render_template('financiera/juicios.html', juicios=juicios)

@app.route('/financiera/juicios/nuevo')
@financiera_admin_required
def nuevo_juicio():
    return render_template('financiera/nuevo_juicio.html')

@app.route('/financiera/juicios/crear', methods=['POST'])
@financiera_admin_required
def crear_juicio():
    if not Juicio.validar_juicio(request.form):
        return redirect('/financiera/juicios/nuevo')
    
    data = {
        'id_pagare': request.form['id_pagare'],
        'rol': request.form['rol'],
        'tribunal': request.form['tribunal'],
        'cuantia': request.form['cuantia'],
        'estado': 'Pendiente'
    }
    
    Juicio.save(data)
    flash("Juicio creado exitosamente", "success")
    return redirect('/financiera/juicios')

@app.route('/financiera/juicios/editar/<int:id>')
@financiera_admin_required
def editar_juicio(id):
    juicio = Juicio.get_by_id(id)
    return render_template('financiera/editar_juicio.html', juicio=juicio)

@app.route('/financiera/juicios/actualizar/<int:id>', methods=['POST'])
@financiera_admin_required
def actualizar_juicio(id):
    if not Juicio.validar_juicio(request.form):
        return redirect(f'/financiera/juicios/editar/{id}')
    
    data = {
        'id': id,
        'id_pagare': request.form['id_pagare'],
        'rol': request.form['rol'],
        'tribunal': request.form['tribunal'],
        'cuantia': request.form['cuantia'],
        'estado': request.form['estado']
    }
    
    Juicio.update(data)
    flash("Juicio actualizado exitosamente", "success")
    return redirect('/financiera/juicios')

@app.route('/financiera/juicios/eliminar/<int:id>')
@financiera_admin_required
def eliminar_juicio(id):
    Juicio.delete(id)
    flash("Juicio eliminado exitosamente", "success")
    return redirect('/financiera/juicios')
