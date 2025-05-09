from flask_app.config.my_sql_conection import connectToMySQL
from flask import flash
from flask_app.models.estudio import Estudio
import re

class Usuario:
    def __init__(self, data):
        self.id = data.get('id')
        self.rut = data.get('rut')
        self.nombre = data.get('nombre')
        self.email = data.get('email')
        self.password = data.get('password')
        self.rol = data.get('rol')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        # Si tenemos datos del estudio en el diccionario, creamos un objeto Estudio
        if 'estudio_id' in data and data['estudio_id']:
            estudio_data = {
                'id': data['estudio_id'],
                'nombre': data.get('estudio_nombre', '')
            }
            self.estudio = Estudio(estudio_data)
        else:
            self.estudio = None

    @staticmethod
    def validar_rut(rut):
        # Si el RUT está vacío
        if not rut:
            return False
            
        # Verificar formato básico (8-9 dígitos + guión + dígito verificador)
        if not re.match(r'^\d{7,8}-[0-9kK]$', rut):
            return False
            
        # Verificar rango básico
        numero = rut.split('-')[0]
        if not (1000000 <= int(numero) <= 99999999):
            return False
            
        return True

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        
        # Validar RUT
        if not Usuario.validar_rut(usuario['rut']):
            flash("RUT inválido. Formato esperado: 12345678-9", "error")
            is_valid = False
            
        # Validar nombre
        if len(usuario['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", "error")
            is_valid = False
            
        # Validar email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email inválido", "error")
            is_valid = False
            
        # Validar contraseña
        if len(usuario['password']) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "error")
            is_valid = False
            
        # Validar rol
        roles_validos = ['admin', 'financiera', 'super_abogado', 'abogado', 'incautador']
        if usuario['rol'] not in roles_validos:
            flash("Rol inválido", "error")
            is_valid = False
            
        return is_valid

    @classmethod
    def get_by_rut(cls, rut):
        query = """
            SELECT u.*, e.id as estudio_id, e.nombre as estudio_nombre 
            FROM usuarios u
            LEFT JOIN estudios e ON u.estudio_id = e.id
            WHERE u.rut = %(rut)s;
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'rut': rut})
        return cls(results[0]) if results else None

    @classmethod
    def get_all(cls):
        query = """
            SELECT u.*, e.id as estudio_id, e.nombre as estudio_nombre 
            FROM usuarios u
            LEFT JOIN estudios e ON u.estudio_id = e.id
            ORDER BY u.nombre;
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query)
        return [cls(result) for result in results]

    @classmethod
    def get_by_role(cls, rol):
        query = "SELECT * FROM usuarios WHERE rol = %(rol)s"
        resultados = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'rol': rol})
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def obtener_por_rol_y_estudio(cls, rol, estudio_id):
        query = """
            SELECT u.*, e.id as estudio_id, e.nombre as estudio_nombre 
            FROM usuarios u
            LEFT JOIN estudios e ON u.estudio_id = e.id
            WHERE u.rol = %(rol)s AND u.estudio_id = %(estudio_id)s
        """
        resultados = connectToMySQL('incautaciones_judiciales_db').query_db(query, {
            'rol': rol,
            'estudio_id': estudio_id
        })
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (rut, nombre, email, password, rol, estudio_id)
            VALUES (%(rut)s, %(nombre)s, %(email)s, %(password)s, %(rol)s, %(estudio_id)s);
        """
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT u.*, e.id as estudio_id, e.nombre as estudio_nombre 
            FROM usuarios u
            LEFT JOIN estudios e ON u.estudio_id = e.id
            WHERE u.id = %(id)s;
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'id': id})
        return cls(results[0]) if results else None

    @classmethod
    def delete(cls, usuario_id):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, {'id': usuario_id})
