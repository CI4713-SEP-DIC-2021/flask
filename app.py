import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from settings.environment import APP_SETTINGS
from flask import g
from flask_cors import CORS


# Inicializacion de Flask y SQLite
app = Flask(__name__)
app.config.from_object(APP_SETTINGS)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)

# A partir de aca se importan los servicios de las aplicaciones
from apps.example_app.services import *
from apps.projects.services import *
from apps.user.services import *
from apps.stories.services import *
from apps.sprints.services import *
from apps.tasks.services import *
from apps.logger.services import *
from apps.meetings.services import *
from apps.docs.services import *
from apps.process.services import *

########################################
# Para caso de desear agregar interface.
@app.route("/")
@cross_origin()
def hello():
    return "Hello World!"


#######################################


if __name__ == "__main__":
    app.run()
