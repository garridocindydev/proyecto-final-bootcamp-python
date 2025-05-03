from flask_app import app #Importamos la app de la carpeta flask_app
from flask_app.controllers import usuarios
from flask_app.controllers import financieras
from flask_app.controllers import estudios

if __name__=="__main__": #Ejecutamos la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)  # Ejecuta la aplicación en modo de depuración
