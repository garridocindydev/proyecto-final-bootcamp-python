from flask_app import app #Importamos la app de la carpeta flask_app

# Importación de controladores
from flask_app.controllers import usuarios
from flask_app.controllers import financieras
from flask_app.controllers import estudios
from flask_app.controllers import abogados
from flask_app.controllers import asignaciones

if __name__=="__main__": #Ejecutamos la aplicación
    app.run(debug=True, host='0.0.0.0', port=5001)  # Ejecuta la aplicación en modo de depuración
