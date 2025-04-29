from flask import render_template, request ,redirect,session
from flask_app import app,bcrypt  # Importamos la app de la carpeta flask_app



@app.route("/", methods=["GET"])
def index():
   return render_template("index.html")