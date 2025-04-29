from flask_app import app #Importamos la app de la carpeta flask_app
from flask_app.controllers import usuario

if __name__=="__main__": #Ejecutamos la aplicación

   app.run(debug=True)  # Ejecuta la aplicación en modo de depuración/debug para detectar cualquier cambio y recargarlo