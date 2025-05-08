from flask_app.config.my_sql_conection import MySQLConnection
from flask_app.models.usuario import Usuario

class Notificacion:
    def __init__(self, data):
        self.id = data['id']
        self.comentario_id = data['comentario_id']
        self.abogado_id = data['abogado_id']
        self.leido = data.get('leido', False)
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        
        # Objeto Comentario
        if 'comentario_texto' in data:
            from flask_app.models.asignacion import Comentario
            comentario_data = {
                'id': data['comentario_id'],
                'asignacion_id': data['asignacion_id'],
                'incautador_id': data['incautador_id'],
                'comentario': data['comentario_texto'],
                'tipo_comentario': data['tipo_comentario'],
                'fecha_comentario': data.get('fecha_comentario'),
                'created_at': data.get('comentario_created_at'),
                'updated_at': data.get('comentario_updated_at'),
                'incautador_nombre': data.get('incautador_nombre')
            }
            self.comentario = Comentario(comentario_data)
            # Agregar el nombre del incautador directamente al objeto comentario
            self.comentario.incautador_nombre = data.get('incautador_nombre')
        else:
            self.comentario = None

    @classmethod
    def crear_notificacion(cls, data):
        query = """
            INSERT INTO notificaciones (comentario_id, abogado_id, leido)
            VALUES (%(comentario_id)s, %(abogado_id)s, FALSE)
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def obtener_no_leidas(cls, abogado_id):
        query = """
            SELECT 
                n.id,
                n.comentario_id,
                n.abogado_id,
                n.leido,
                n.created_at,
                n.updated_at,
                c.comentario as comentario_texto,
                c.asignacion_id,
                c.incautador_id,
                c.tipo_comentario,
                c.fecha_comentario,
                c.created_at as comentario_created_at,
                c.updated_at as comentario_updated_at,
                u.nombre as incautador_nombre,
                u.id as incautador_id
            FROM notificaciones n
            JOIN comentarios_incautador c ON n.comentario_id = c.id
            JOIN usuarios u ON c.incautador_id = u.id
            WHERE n.abogado_id = %(abogado_id)s
            AND n.leido = FALSE
            ORDER BY n.created_at DESC
        """
        results = MySQLConnection('incautaciones_judiciales_db').query_db(query, {'abogado_id': abogado_id})
        return [cls(result) for result in results] if results else []

    @classmethod
    def marcar_como_leida(cls, notificacion_id):
        query = """
            UPDATE notificaciones
            SET leido = TRUE
            WHERE id = %(notificacion_id)s
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, {'notificacion_id': notificacion_id})

    @classmethod
    def contar_no_leidas(cls, abogado_id):
        query = """
            SELECT COUNT(*) as count
            FROM notificaciones
            WHERE abogado_id = %(abogado_id)s
            AND leido = FALSE
        """
        resultado = MySQLConnection('incautaciones_judiciales_db').query_db(query, {'abogado_id': abogado_id})
        return resultado[0]['count'] if resultado else 0
