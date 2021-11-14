import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from settings.environment import APP_SETTINGS
from flask import g


# Inicializacion de Flask y SQLite
app = Flask(__name__)
app.config.from_object(APP_SETTINGS)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# A partir de aca se importan los servicios de las aplicaciones
from apps.example_app.services import *

########################################
# Para caso de desear agregar interface.
@app.route("/")
def hello():
    return "Hello World!"
#######################################


if __name__ == '__main__':
    app.run()