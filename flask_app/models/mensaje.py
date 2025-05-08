from flask_app.config.my_sql_conection import MySQLConnection
from flask_app.models.usuario import Usuario

class Mensaje:
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.juicio_id = data['juicio_id']
        self.emisor_id = data['emisor_id']
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        
        # Objeto Emisor
        if 'emisor_id' in data and data['emisor_id']:
            emisor_data = {
                'id': data['emisor_id'],
                'nombre': data.get('emisor_nombre', ''),
                'email': data.get('emisor_email', '')
            }
            self.emisor = Usuario(emisor_data)
        else:
            self.emisor = None

    @classmethod
    def crear_mensaje(cls, data):
        query = """
            INSERT INTO mensajes (contenido, juicio_id, emisor_id)
            VALUES (%(contenido)s, %(juicio_id)s, %(emisor_id)s)
        """
        return MySQLConnection('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def obtener_por_juicio(cls, juicio_id):
        query = """
            SELECT m.*, 
                u.id as emisor_id, u.nombre as emisor_nombre, u.email as emisor_email
            FROM mensajes m
            LEFT JOIN usuarios u ON m.emisor_id = u.id
            WHERE m.juicio_id = %(juicio_id)s
            ORDER BY m.created_at DESC
        """
        resultados = MySQLConnection('incautaciones_judiciales_db').query_db(query, {'juicio_id': juicio_id})
        mensajes = []
        for mensaje in resultados:
            mensajes.append(cls(mensaje))
        return mensajes
