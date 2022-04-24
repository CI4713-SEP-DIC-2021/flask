import os
from itertools import groupby

from apps.processes.models import Group, Process2
from .models import Project, ProjectStatus
from app import db, app
from flask import request, jsonify
from flask_cors import cross_origin
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger


MODULE = "Proyecto"

""" Listar todos los proyectos """


@app.route("/projects/all")
def all():
    try:
        projects = Project.query.all()
        return jsonify([user.serialize() for user in projects])
    except Exception as e:
        return str(e)

##################################################################
# New: Get all projects

""" Listar todos los proyectos de un usuario """

@app.route("/projects/getall")
def getall_projects():
    try:
        projects = Project.query.all()
        return jsonify([project.serialize() for project in projects])
    except Exception as e:
        return str(e)

##################################################################
""" Listar todos los proyectos de un usuario """


@app.route("/projects/getall/<int:user_id>")
@cross_origin()
def get_all_by_user(user_id):
    projects = Project.query.filter_by(user_id=user_id).order_by(Project.date_created.asc())
    if projects.count() > 0:
        return jsonify([project.serialize() for project in projects])
    else:
        return jsonify([])


""" Agregar un proyecto """


@app.route("/projects/add", methods=["POST"])
def add_project():
    if request.method == "POST":
        """request_data = request.get_json()
        description = request_data['description']
        user_id = request_data['user_id']
        type = request_data['type']
        # JSON
        request_data = request.get_json()

        description = request_data['description']
        status = request_data['status']
        user_id = request_data['user_id']
        type = request_data['type']
        # JSON"""
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
            add_event_logger(user_id, LoggerEvents.reactive_project, MODULE)

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
        """request_data = request.get_json()
        description = request_data['description']
        user_id = request_data['user_id']
        type = request_data['type']
        # JSON
        request_data = request.get_json()

        description = request_data['description']
        status = request_data['status']
        user_id = request_data['user_id']
        type = request_data['type']
        # JSON"""
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

@app.route("/projects/processes/<int:id_>")
def get_project_processes(id_):

    try:

        project = Project.query.get_or_404(id_) 
        processes = Process2.query.filter_by(project_id=id_).order_by("category")

        processes_by_category = [list(group) for key, group in groupby(processes, lambda p: p.category)]

        project_categories = []

        for category_processes in processes_by_category:

            category_processes.sort(key=lambda p: p.group_id)
            by_group = [list(group) for key, group in groupby(category_processes, lambda p: p.group_id)]

            category_groups = []

            for process in by_group:

                group_name = Group.query.get_or_404(process[0].group_id).name
                category_groups.append(
                    {
                        "group_name": group_name,
                        "processes": list(map(lambda p: {"name": p.name, "value": p.value}, process))
                    }
                )

            project_categories.append(
                {
                    "category_name": category_processes[0].category,
                    "groups": category_groups
                }
            )
        
        response = {
            "project_description": project.description,
            "categories": project_categories
        }

        return jsonify(response)

                



    except:
        return jsonify({"server": "ERROR"})