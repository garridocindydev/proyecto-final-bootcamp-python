import os
from dotenv import load_dotenv
import pymysql.cursors  # Utilizamos un cursor para interactuar con BD

# Carga las variables de entorno desde el archivo .env
load_dotenv()

class MySQLConnection: #Clase que permite generar instancia de conexión con BD
    def __init__(self, db):
        print("Initializing MySQLConnection...")
        print("os.getenv('HOST')", os.getenv('HOST'))
        print("os.getenv('USER')", os.getenv('USER_DB'))
        print("os.getenv('PASSWORD')", os.getenv('PASSWORD_DB'))

        connection = pymysql.connect(host = os.getenv("HOST"),
                                    user = os.getenv("USER_DB"), # Cambia el usuario y contraseña
                                    password = os.getenv("PASSWORD_DB"), 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection 

    # El método que se encarga de la consulta

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # La consulta INSERT regresan el id del nuevo registro
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # La consulta SELECT regresa una LISTA DE DICCIONARIOS con los datos
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE y DELETE no regresan nada
                    self.connection.commit()
            except Exception as e:
                # En caso de alguna falla, regresa FALSE
                print("Something went wrong", e)
                return False
            finally:
                # Cerramos conexión
                self.connection.close()


# connectToMySQL recibe el nombre de la base de datos y genera una instancia de MySQLConnection

def connectToMySQL(db):
    return MySQLConnection(db)