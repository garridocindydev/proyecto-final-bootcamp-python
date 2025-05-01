from flask_app.config.my_sql_conection import connectToMySQL
from flask import flash

class Estudio:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @staticmethod
    def validar_estudio(data):
        is_valid = True
        
        if len(data['nombre']) < 3:
            flash("El nombre del estudio debe tener al menos 3 caracteres", "error")
            is_valid = False
            
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM estudios ORDER BY nombre;"
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query)
        estudios = []
        for estudio in results:
            estudios.append(cls(estudio))
        return estudios

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM estudios WHERE id = %(id)s;"
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'id': id})
        return cls(results[0]) if results else None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO estudios (nombre)
            VALUES (%(nombre)s);
        """
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE estudios 
            SET nombre = %(nombre)s
            WHERE id = %(id)s;
        """
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM estudios WHERE id = %(id)s;"
        return connectToMySQL('incautaciones_judiciales_db').query_db(query, {'id': id})

    @classmethod
    def get_juicios_asignados(cls, id):
        query = """
            SELECT j.* FROM juicios j
            WHERE j.estudio = %(id)s
            ORDER BY j.created_at DESC;
        """
        results = connectToMySQL('incautaciones_judiciales_db').query_db(query, {'id': id})
        from flask_app.models.juicio import Juicio
        return [Juicio(juicio) for juicio in results] if results else []
