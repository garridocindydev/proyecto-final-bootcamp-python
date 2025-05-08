from flask_app.config.my_sql_conection import MySQLConnection
from flask import flash
from flask_app.models.estudio import Estudio
from flask_app.models.usuario import Usuario

class Juicio:
    def __init__(self, data):
        self.id = data['id']
        self.id_pagare = data['id_pagare']
        self.rol = data['rol']
        self.tribunal = data['tribunal']
        self.cuantia = data['cuantia']
        self.estado = data.get('estado', 'Pendiente')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.abogado_id = data.get('abogado_id')
        self.incautador_id = data.get('incautador_id')
        
        # Objeto Estudio
        if 'estudio_id' in data and data['estudio_id']:
            estudio_data = {
                'id': data['estudio_id'],
                'nombre': data.get('estudio_nombre', '')
            }
            self.estudio = Estudio(estudio_data)
        else:
            self.estudio = None
            
        # Objeto Abogado
        if 'abogado_id' in data and data['abogado_id']:
            abogado_data = {
                'id': data['abogado_id'],
                'nombre': data.get('abogado_nombre', ''),
                'email': data.get('abogado_email', '')
            }
            self.abogado = Usuario(abogado_data)
        else:
            self.abogado = None
            
        # Objeto Incautador
        if 'incautador_id' in data and data['incautador_id']:
            incautador_data = {
                'id': data['incautador_id'],
                'nombre': data.get('incautador_nombre', ''),
                'email': data.get('incautador_email', '')
            }
            self.incautador = Usuario(incautador_data)
        else:
            self.incautador = None

    @classmethod
    def crear_juicio(cls, data):
        query = """
            INSERT INTO juicios (id_pagare, rol, tribunal, cuantia, estado)
            VALUES (%(id_pagare)s, %(rol)s, %(tribunal)s, %(cuantia)s, 'Pendiente')
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def obtener_todos(cls):
        query = """
            SELECT j.id as juicio_id, j.id_pagare, j.tribunal,j.abogado_id,j.cuantia,
        j.estado, e.id as estudio_id,e.nombre as nombre_estudio
        FROM juicios j
        INNER JOIN estudios e ON j.estudio = e.id
        ORDER BY j.created_at DESC
        """
        resultados = MySQLConnection('incautaciones_judiciales_db').query_db(query)
        juicios = []
        for juicio in resultados:
            juicios.append(juicio)
        return juicios
        
    @classmethod
    def obtener_por_estudio(cls, estudio_id):
        query = """
            SELECT j.*
            FROM juicios j
            WHERE j.estudio = %(estudio_id)s
            ORDER BY j.created_at DESC
        """
        resultados = MySQLConnection('incautaciones_judiciales_db').query_db(query, {'estudio_id': estudio_id})
        juicios = []
        for juicio in resultados:
            juicios.append(cls(juicio))
        return juicios

    @classmethod
    def asignar_estudio(cls, juicio_id, estudio_id):
        query = """
            UPDATE juicios 
            SET estudio = %(estudio_id)s, estado = 'Asignado'
            WHERE id = %(juicio_id)s
        """
        data = {
            'juicio_id': juicio_id,
            'estudio_id': estudio_id
        }
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def terminar_juicio(cls, juicio_id):
        query = """
            UPDATE juicios 
            SET estado = 'Terminado'
            WHERE id = %(juicio_id)s
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, {'juicio_id': juicio_id})

    @classmethod
    def obtener_por_abogado(cls, abogado_id):
        query = """
            SELECT j.*, 
                e.id as estudio_id, e.nombre as estudio_nombre,
                a.id as abogado_id, a.nombre as abogado_nombre, a.email as abogado_email
            FROM juicios j
            LEFT JOIN estudios e ON j.estudio = e.id
            LEFT JOIN usuarios a ON j.abogado_id = a.id
            WHERE j.abogado_id = %(abogado_id)s
            ORDER BY j.created_at DESC
        """
        resultados = MySQLConnection('incautaciones_judiciales_db').query_db(query, {'abogado_id': abogado_id})
        juicios = []
        for juicio in resultados:
            juicios.append(cls(juicio))
        return juicios

    @classmethod
    def obtener_por_id(cls, juicio_id):
        query = """
            SELECT j.*, 
                e.id as estudio_id, e.nombre as estudio_nombre,
                a.id as abogado_id, a.nombre as abogado_nombre, a.email as abogado_email,
                i.id as incautador_id, i.nombre as incautador_nombre, i.email as incautador_email
            FROM juicios j
            LEFT JOIN estudios e ON j.estudio = e.id
            LEFT JOIN usuarios a ON j.abogado_id = a.id
            LEFT JOIN usuarios i ON j.incautador_id = i.id
            WHERE j.id = %(juicio_id)s
        """
        resultado = MySQLConnection('incautaciones_judiciales_db').query_db(query, {'juicio_id': juicio_id})
        return cls(resultado[0]) if resultado else None

    @classmethod
    def asignar_incautador(cls, juicio_id, incautador_id):
        query = """
            UPDATE juicios 
            SET incautador_id = %(incautador_id)s
            WHERE id = %(juicio_id)s
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, {
            'juicio_id': juicio_id,
            'incautador_id': incautador_id
        })

    @classmethod
    def asignar_abogado(cls, juicio_id, abogado_id):
        query = """
            UPDATE juicios 
            SET abogado_id = %(abogado_id)s
            WHERE id = %(juicio_id)s
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, {
            'juicio_id': juicio_id,
            'abogado_id': abogado_id
        })

    @classmethod
    def asignar_abogado_juicio(cls, juicio_id, abogado_id):
        query = """
            UPDATE juicios 
            SET abogado_id = %(abogado_id)s, estado = 'Asignado'
            WHERE id = %(juicio_id)s
        """
        data = {
            'juicio_id': juicio_id,
            'abogado_id': abogado_id
        }
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, data)

    @staticmethod
    def validar_juicio(juicio):
        is_valid = True
        if not juicio['id_pagare']:
            flash('El ID del pagaré es requerido', 'error')
            is_valid = False
        if not juicio['rol']:
            flash('El rol es requerido', 'error')
            is_valid = False
        if not juicio['tribunal']:
            flash('El tribunal es requerido', 'error')
            is_valid = False
        if not juicio['cuantia'] or float(juicio['cuantia']) <= 0:
            flash('La cuantía debe ser mayor a 0', 'error')
            is_valid = False
        return is_valid
