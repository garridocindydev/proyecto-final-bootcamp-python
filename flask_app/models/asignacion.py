from flask_app.config.my_sql_conection import connectToMySQL
from flask import flash
from datetime import datetime
from flask_app.models.notificacion import Notificacion

class Asignacion:
    def __init__(self, data):
        self.id = data['id']
        self.juicio_id = data['juicio_id']
        self.abogado_id = data['abogado_id']
        self.incautador_id = data['incautador_id']
        self.fecha_asignacion = data['fecha_asignacion']
        self.fecha_ejecucion = data['fecha_ejecucion']
        self.estado = data['estado']
        self.observaciones = data['observaciones']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Para almacenar datos relacionados
        self.juicio = None
        self.abogado = None
        self.comentarios = []

    @classmethod
    def get_asignaciones_incautador(cls, incautador_id):
        query = """
            SELECT a.*, j.*, u.nombre as abogado_nombre,
                   j.id as juicio_id, j.rol, j.tribunal
            FROM asignaciones_juicios a
            JOIN juicios j ON a.juicio_id = j.id
            JOIN usuarios u ON a.abogado_id = u.id
            WHERE a.incautador_id = %(incautador_id)s
            ORDER BY a.fecha_asignacion DESC
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'incautador_id': incautador_id})
        asignaciones = []
        for row in results:
            asignacion = cls(row)
            asignacion.juicio = {
                'id': row['juicio_id'],
                'rol': row['rol'],
                'tribunal': row['tribunal'],
                'patente_vehiculo': row['patente_vehiculo']
            }
            asignacion.abogado = {
                'nombre': row['abogado_nombre']
            }
            asignacion.comentarios = Comentario.get_by_asignacion(asignacion.id)
            asignaciones.append(asignacion)
        return asignaciones

    @classmethod
    def get_asignaciones_con_comentarios(cls, abogado_id):
        query = """
            SELECT a.*, j.*, u.nombre as incautador_nombre, c.*,
                   j.id as juicio_id, j.rol, j.tribunal
            FROM asignaciones_juicios a
            JOIN juicios j ON a.juicio_id = j.id
            JOIN usuarios u ON a.incautador_id = u.id
            LEFT JOIN comentarios_incautador c ON a.id = c.asignacion_id
            WHERE a.abogado_id = %(abogado_id)s
            ORDER BY c.fecha_comentario DESC
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'abogado_id': abogado_id})
        asignaciones = {}
        
        for row in results:
            if row['id'] not in asignaciones:
                asignacion = cls(row)
                asignacion.juicio = {
                    'id': row['juicio_id'],
                    'rol': row['rol'],
                    'tribunal': row['tribunal']
                }
                asignacion.incautador = {
                    'nombre': row['incautador_nombre']
                }
                asignacion.comentarios = []
                asignaciones[row['id']] = asignacion
            
            if row['comentario'] is not None:
                comentario = {
                    'id': row['id'],
                    'comentario': row['comentario'],
                    'tipo_comentario': row['tipo_comentario'],
                    'fecha_comentario': row['fecha_comentario']
                }
                asignaciones[row['id']].comentarios.append(comentario)
        
        return list(asignaciones.values())

    @classmethod
    def actualizar_estado(cls, asignacion_id, nuevo_estado, observaciones=None):
        query = """
            UPDATE asignaciones_juicios
            SET estado = %(estado)s,
                fecha_ejecucion = CASE 
                    WHEN %(estado)s = 'Ejecutado' THEN NOW()
                    ELSE fecha_ejecucion
                END,
                observaciones = CASE
                    WHEN %(observaciones)s IS NOT NULL THEN %(observaciones)s
                    ELSE observaciones
                END
            WHERE id = %(id)s
        """
        data = {
            'id': asignacion_id,
            'estado': nuevo_estado,
            'observaciones': observaciones
        }
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, data)

class Comentario:
    def __init__(self, data):
        self.id = data['id']
        self.asignacion_id = data['asignacion_id']
        self.incautador_id = data['incautador_id']
        self.comentario = data['comentario']
        self.tipo_comentario = data['tipo_comentario']
        self.fecha_comentario = data['fecha_comentario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def crear(cls, data):
        # Insertar el comentario
        query = """
            INSERT INTO comentarios_incautador
            (asignacion_id, incautador_id, comentario, tipo_comentario)
            VALUES (%(asignacion_id)s, %(incautador_id)s, %(comentario)s, %(tipo_comentario)s)
        """
        comentario_id = connectToMySQL('incautaciones_judiciales_db').query_db(query, data)
        
        # Obtener la asignación para saber quién es el abogado
        query = """
            SELECT aj.abogado_id
            FROM asignaciones_juicios aj
            WHERE aj.id = %(asignacion_id)s
        """
        result = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'asignacion_id': data['asignacion_id']})
        
        if result and result[0]['abogado_id']:
            # Crear notificación para el abogado
            
            notificacion_data = {
                'comentario_id': comentario_id,
                'abogado_id': result[0]['abogado_id']
            }
            Notificacion.crear_notificacion(notificacion_data)
        
        return comentario_id

    @classmethod
    def get_by_asignacion(cls, asignacion_id):
        query = """
            SELECT c.*, u.nombre as incautador_nombre
            FROM comentarios_incautador c
            JOIN usuarios u ON c.incautador_id = u.id
            WHERE c.asignacion_id = %(asignacion_id)s
            ORDER BY c.fecha_comentario DESC
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'asignacion_id': asignacion_id})
        comentarios = []
        for row in results:
            comentario = cls(row)
            comentario.incautador_id = row['incautador_id']
            comentarios.append(comentario)
        return comentarios
