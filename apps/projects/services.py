import os

from flask_cors import cross_origin
from .models import Project, ProjectStatus
from app import db, app
from flask import request, jsonify
from apps.logger.models import LoggerEvents
from apps.logger.services import add_event_logger


MODULE = "Proyecto"


""" Listar todos los proyectos de un usuario """


@app.route("/projects/getall/<int:user_id>")
@cross_origin()
def get_all_by_user(user_id):
    projects = Project.query.filter_by(user_id=user_id).order_by(Project.date_created.asc())
    
    if projects.count() > 0:
        return   jsonify([project.serialize() for project in projects])
    else:
        return  jsonify([])


""" Agregar un proyecto """


@app.route("/projects/add", methods=["POST"])
def add_project():
    if request.method == "POST":
        description = request.json.get("description", None)
        user_id = request.json.get("user_id", None)
        type = request.json.get("type", None)
        try:
            project = Project(
                description=description, user_id=user_id, status=ProjectStatus.active, type=type
            )
            db.session.add(project)
            db.session.commit()
            add_event_logger(user_id, LoggerEvents.add_project, MODULE)
            return jsonify(project.serialize())
        except Exception as e:
            print(e) 
            return jsonify({"server": "ERROR"})


""" Pausar un proyecto """


@app.route("/projects/pause/<int:id_>", methods=["PATCH"])
def pause_project(id_):
    if request.method == "PATCH":
        try:
            project = Project.query.get_or_404(id_)
            project.status = ProjectStatus.paused
            db.session.commit()

            user_id = project.user_id
            add_event_logger(user_id, LoggerEvents.pause_project, MODULE)
            return jsonify(project.serialize())
        except:
            return jsonify({"server": "ERROR"})


""" Activar nuevamente un proyecto """


@app.route("/projects/reactivate/<int:id_>", methods=["PATCH"])
def reactivate_project(id_):
    if request.method == "PATCH":
        try:
            project = Project.query.get_or_404(id_)
            project.status = ProjectStatus.active
            db.session.commit()

            user_id = project.user_id
            add_event_logger(user_id, LoggerEvents.reactivate_project, MODULE)
            return jsonify(project.serialize())
        except:
            return jsonify({"server": "ERROR"})


""" Eliminar un proyecto """


@app.route("/projects/delete/<int:id_>", methods=["DELETE"])
def delete_project(id_):
    if request.method == "DELETE":
        project = Project.query.get_or_404(id_)
        try:
            user_id = project.user_id
            db.session.delete(project)
            db.session.commit()
            add_event_logger(user_id, LoggerEvents.delete_project, MODULE)
            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


""" Modificar un proyecto """


@app.route("/projects/update/<int:id_>", methods=["PUT"])
def update_project(id_):
    if request.method == "PUT":
        project = Project.query.get_or_404(id_)
        description = request.json.get("description", None)
        user_id = request.json.get("user_id", None)
        type = request.json.get("type", None)

        project.description = description
        project.user_id = user_id
        project.type = type
        try:
            db.session.commit()

            add_event_logger(user_id, LoggerEvents.update_project, MODULE)
            return jsonify(project.serialize())
        except:
            return jsonify({"server": "ERROR"})


"""Buscar un proyecto por su id"""


@app.route("/projects/search/<int:id_>")
def search_project(id_):
    try:
        project = Project.query.get_or_404(id_)

        user_id = project.user_id
        add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        return jsonify([project.serialize()])
    except:
        return jsonify({"server": "ERROR"})
