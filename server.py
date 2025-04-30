from flask_app import app #Importamos la app de la carpeta flask_app
from flask_app.controllers import usuario
from flask_app.controllers import juicios

if __name__=="__main__": #Ejecutamos la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)  # Ejecuta la aplicación en modo de depuración