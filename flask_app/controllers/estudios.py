from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.juicio import Juicio
from flask_app.models.usuario import Usuario
from flask_app.models.estudio import Estudio
from flask_app.controllers.usuarios import admin_required

@app.route('/admin/estudios')
@admin_required
def admin_estudios():
    estudios = Estudio.get_all()
    return render_template('admin/estudios.html', estudios=estudios)

@app.route('/admin/estudios/nuevo')
@admin_required
def nuevo_estudio():
    return render_template('admin/nuevo_estudio.html')

@app.route('/admin/estudios/crear', methods=['POST'])
@admin_required
def crear_estudio():
    if not Estudio.validar_estudio(request.form):
        return redirect('/admin/estudios/nuevo')
    
    data = {
        'nombre': request.form['nombre']
    }
    
    Estudio.save(data)
    flash('Estudio creado exitosamente', 'success')
    return redirect('/admin/estudios')

@app.route('/admin/estudios/eliminar/<int:id>')
@admin_required
def eliminar_estudio(id):
    # Verificar si hay abogados o juicios asociados
    juicios = Estudio.get_juicios_asignados(id)
    if juicios:
        flash('No se puede eliminar el estudio porque tiene juicios asignados', 'error')
        return redirect('/admin/estudios')
    
    Estudio.delete(id)
    flash('Estudio eliminado exitosamente', 'success')
    return redirect('/admin/estudios')
