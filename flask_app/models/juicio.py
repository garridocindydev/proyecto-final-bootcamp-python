from flask_app.config.my_sql_conection import MySQLConnection
from flask import flash

class Juicio:
    def __init__(self, data):
        self.id = data.get('id')
        self.id_pagare = data['id_pagare']
        self.rol = data['rol']
        self.tribunal = data['tribunal']
        self.estudio = data.get('estudio')
        self.cuantia = data['cuantia']
        self.estado = data.get('estado', 'Pendiente')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @classmethod
    def crear_juicio(cls, data):
        query = """
            INSERT INTO juicios (id_pagare, rol, tribunal, cuantia, estado)
            VALUES (%(id_pagare)s, %(rol)s, %(tribunal)s, %(cuantia)s, 'Pendiente')
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM juicios"
        resultados = MySQLConnection('incautaciones_judiciales_db').query_db(query)
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
