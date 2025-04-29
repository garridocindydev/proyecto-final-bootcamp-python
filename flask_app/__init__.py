from flask import Flask #Importación de Flask
from flask_bcrypt import Bcrypt #Importamos Bcrypt

app = Flask(__name__) #Crea instancia de Flask
bcrypt = Bcrypt(app) #Generamos un objeto llamado bcrypt

app.secret_key = "1234"
