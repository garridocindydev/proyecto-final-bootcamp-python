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
            
        # Remover puntos y guión
        rut = rut.replace(".", "").replace("-", "").upper()
        
        # Verificar longitud
        if len(rut) < 8 or len(rut) > 9:
            return False

        # Verificar que todos los caracteres son válidos
        if not re.match(r'^[0-9]+[0-9K]$', rut):
            return False

        # Separar número y dígito verificador
        numero = rut[:-1]
        dv = rut[-1]
        
        try:
            # Convertir a integer
            num = int(numero)
            
            # Validar rango
            if num < 1000000 or num > 99999999:
                return False
                
            # Calcular dígito verificador
            suma = 0
            multiplicador = 2
            
            # Recorrer cada dígito de derecha a izquierda
            for d in reversed(numero):
                suma += int(d) * multiplicador
                multiplicador = multiplicador + 1 if multiplicador < 7 else 2
            
            # Calcular dígito verificador esperado
            resto = suma % 11
            dv_esperado = str(11 - resto)
            
            if dv_esperado == '11':
                dv_esperado = '0'
            elif dv_esperado == '10':
                dv_esperado = 'K'
                
            # Comparar dígito verificador
            return dv == dv_esperado
            
        except ValueError:
            return False

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
        roles_validos = ['admin', 'financiera', 'abogado', 'incautador']
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
    def save(cls, data):
        query = """
            INSERT INTO usuarios (rut, nombre, email, password, rol, estudio_id)
            VALUES (%(rut)s, %(nombre)s, %(email)s, %(password)s, %(rol)s, %(estudio_id)s);
        """
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def delete(cls, usuario_id):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, {'id': usuario_id})
