import os
from .models import *
from app import db, app
from flask import request, jsonify, make_response
from datetime import datetime
from apps.sprints.models import *
from apps.user.models import UserA
from apps.logger.services import add_event_logger
from apps.logger.models import LoggerEvents

MODULE = "Tarea"


@app.route("/tasks/getbysprint/<sprint_id>")
def get_tasks(sprint_id):
    tasks = Task.query.filter_by(sprint_id=sprint_id)
    if tasks.count() > 0:
        return jsonify([c.serialize() for c in tasks])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/tasks/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id).delete()
        db.session.commit()
        return jsonify(task), 200
    except Exception as e:
        return str(e)


@app.route("/tasks/add", methods=["POST"])
def add_tasks():

    if request.method == "POST":
        description = request.json.get("description")
        sprint_id = request.json.get("sprint_id")
        task_type = request.json.get("task_type")
        task_status = request.json.get("task_status")
        task_class = request.json.get("task_class")

        # usuario que crea la tarea
        user_id = request.json.get("user_id")
        user_creator = UserA.query.get_or_404(user_id)
        if user_creator.role not in ["Scrum Master", "Scrum Team"]:
            return jsonify({"server": "Debe ser parte del equipo"}), 405

        # usuarios a los que se las asignan
        users = []
        if len(request.json.get("users")) > 2:
            return make_response(jsonify("maximo 2 usuarios permitidos"), 404)
        elif len(request.json.get("users")) == 0:
            pass
        else:
            for i in request.json.get("users"):
                user = UserA.query.get_or_404(i)
                users.append(user)

        try:
            task = Task(
                description=description,
                sprint_id=sprint_id,
                task_type=task_type,
                task_status=task_status,
                task_class=task_class,
                user_id=user_creator.id,
            )
            db.session.add(task)
            db.session.commit()
            task.asignners = users
            db.session.commit()

            ###########Agregando evento al logger#######################
            add_event_logger(user_id, LoggerEvents.add_task, MODULE)
            ############################################################

            return jsonify(task.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})
