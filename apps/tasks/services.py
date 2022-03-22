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


##########
@app.route("/tasks/getbystory/<story_id>")
def get_tasks_by_story(story_id):
    tasks = Task.query.filter_by(story_id=story_id)
    if tasks.count() > 0:
        return jsonify([c.serialize() for c in tasks])
    else:
        return jsonify({"server": "NO_CONTENT"})
##########


@app.route("/tasks/delete/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task = Task.query.filter_by(id=task_id).delete()
        db.session.commit()
        return jsonify(task), 200
    except Exception as e:
        return str(e)


## Update task
@app.route("/tasks/update/<task_id>", methods=["PUT"])
def update_task(task_id):
    if request.method == "PUT":
        task = Task.query.get_or_404(task_id)

        if request.json.get("description"):
            description = request.json.get("description")
            task.description = description

        if request.json.get("functions"):
            functions = request.json.get("functions")
            task.functions = functions

        if request.json.get("task_type"):
            task_type = request.json.get("task_type")
            task.task_type = task_type

        if request.json.get("task_status"):
            task_status = request.json.get("task_status")
            task.task_status = task_status

        if request.json.get("task_class"):
            task_class = request.json.get("task_class")
            task.task_class = task_class

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
            db.session.commit()
            task.asignners = users
            db.session.commit()

            return jsonify(task.serialize())
        except:
            return jsonify({"server": "ERROR"})
## Update task


@app.route("/tasks/add", methods=["POST"])
def add_tasks():

    if request.method == "POST":
        description = request.json.get("description")
        functions = request.json.get("functions")
        story_id = request.json.get("story_id")
        sprint_id = request.json.get("sprint_id")
        task_type = request.json.get("task_type")
        task_status = request.json.get("task_status")
        task_class = request.json.get("task_class")

        # usuario que crea la tarea
        user_id = request.json.get("user_id")
        user_creator = UserA.query.get_or_404(user_id)
        if user_creator.role not in ["Scrum Master", "Scrum Team", "Product Owner"]:
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
                functions=functions,
                story_id=story_id,
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
