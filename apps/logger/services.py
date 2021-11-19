import os
from .models import Logger
from app import db, app
from flask import request, jsonify
from datetime import datetime
from apps.user.models import UserA


# dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string)


@app.route("/logger/getall")
def get_all_logs():
    """
    Funcion que permitira retornar todos los
    eventos almacenados en el logger, destinada
    para la lista general de los mismos.
    
    Responde al url: /logger/getall
    """
    try:
        logger = Logger.query.all()
        return jsonify([e.serialize() for e in logger])
    except Exception as e:
        return str(e)


@app.route("/logger/delete/<id_>", methods=["DELETE"])
def delete_log(id_):
    try:
        log = Logger.query.filter_by(id=id_).delete()
        db.session.commit()
        return jsonify(log), 200
    except Exception as e:
        return str(e)

def add_event_logger(user, event, module):
    """
    Funcion que sera llamada en cada uno de los eventos
    para registrar en el logger.
    """
    try:
        log = Logger(user=user, event=event, loged_module=module)
        db.session.add(log)
        db.session.commit()
        return "Log added. log id={}".format(log.id)
    except Exception as e:
        return str(e)
