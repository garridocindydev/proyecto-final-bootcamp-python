from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.estudio import Estudio
from flask_bcrypt import Bcrypt
from functools import wraps

bcrypt = Bcrypt(app)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session or session.get('rol') != 'admin':
            flash("Acceso denegado. Se requieren privilegios de administrador.", "error")
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_rut(request.form['rut'])
    
    if not usuario:
        flash("RUT/Contraseña inválidos", "error")
        return redirect('/')
    
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("RUT/Contraseña inválidos", "error")
        return redirect('/')
    
    session['usuario_id'] = usuario.id
    session['rol'] = usuario.rol
    
    if usuario.rol == 'admin':
        return redirect('/admin')
    elif usuario.rol == 'financiera':
        return redirect('/financiera/juicios')
    elif usuario.rol == 'abogado':
        return redirect('/abogado/dashboard')
    return redirect('/dashboard')

@app.route('/abogado/dashboard')
def abogado_dashboard():
    if 'usuario_id' not in session or session.get('rol') != 'abogado':
        return redirect('/')
    
    # Obtener el usuario actual
    usuario = Usuario.get_by_id(session['usuario_id'])
    
    # Obtener los juicios del estudio del abogado
    from flask_app.models.juicio import Juicio
    juicios = Juicio.obtener_por_estudio(usuario.estudio_id)
    
    # Calcular estadísticas
    total_juicios = len(juicios)
    juicios_pendientes = len([j for j in juicios if j.estado == 'Pendiente'])
    juicios_asignados = len([j for j in juicios if j.estado == 'Asignado'])
    
    return render_template('abogado/dashboard.html',
                           total_juicios=total_juicios,
                           juicios_pendientes=juicios_pendientes,
                           juicios_asignados=juicios_asignados)

@app.route('/abogado/juicios')
def abogado_juicios():
    if 'usuario_id' not in session or session.get('rol') != 'abogado':
        return redirect('/')
    
    # Obtener el usuario actual
    usuario = Usuario.get_by_id(session['usuario_id'])
    
    # Obtener los juicios del estudio del abogado
    from flask_app.models.juicio import Juicio
    juicios = Juicio.obtener_por_estudio(usuario.estudio_id)
    
    return render_template('abogado/juicios.html', juicios=juicios)

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    usuarios = Usuario.get_all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/nuevo')
@admin_required
def nuevo_usuario():
    estudios = Estudio.get_all()
    return render_template('admin/nuevo_usuario.html', estudios=estudios)

@app.route('/admin/usuarios/crear', methods=['POST'])
@admin_required
def crear_usuario():
    if not Usuario.validar_usuario(request.form):
        return redirect('/admin/usuarios/nuevo')
    
    # Crear el hash del password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # Crear el diccionario de datos
    data = {
        'rut': request.form['rut'],
        'nombre': request.form['nombre'],
        'email': request.form['email'],
        'password': pw_hash,
        'rol': request.form['rol'],
        'estudio_id': request.form.get('estudio_id') if request.form['rol'] == 'abogado' else None
    }
    
    Usuario.save(data)
    flash("Usuario creado exitosamente", "success")
    return redirect('/admin/usuarios')

@app.route('/admin/usuarios/eliminar/<int:id>')
@admin_required
def eliminar_usuario(id):
    Usuario.delete(id)
    flash("Usuario eliminado exitosamente", "success")
    return redirect('/admin/usuarios')

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente", "success")
    return redirect('/')
