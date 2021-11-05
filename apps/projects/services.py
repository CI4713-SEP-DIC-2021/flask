import os
from .models import Project, ProjectStatus
from app import db, app
from flask import request, jsonify


MODULE = "Proyecto"


""" Listar todos los proyectos de un usuario """


@app.route("/projects/getall/<int:user_id>")
def get_all_by_user(user_id):
    projects = Project.query.filter_by(user_id=user_id)
    if projects.count() > 0:
        return jsonify([project.serialize() for project in projects])
    else:
        return jsonify({"server": "NO_CONTENT"})


""" Agregar un proyecto """


@app.route("/projects/add", methods=["POST"])
def add_project():
    if request.method == "POST":
        description = request.form.get("description")
        user_id = request.form.get("user_id")
        try:
            project = Project(
                description=description, user_id=user_id, status=ProjectStatus.active
            )
            db.session.add(project)
            db.session.commit()

            return jsonify(project.serialize())
        except:
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

            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


""" Modificar un proyecto """


@app.route("/projects/update/<int:id_>", methods=["PUT"])
def update_project(id_):
    if request.method == "PUT":
        project = Project.query.get_or_404(id_)
        description = request.form.get("description")
        user_id = request.form.get("user_id")

        project.description = description
        project.user_id = user_id
        try:
            db.session.commit()


            return jsonify(project.serialize())
        except:
            return jsonify({"server": "ERROR"})


"""Buscar un proyecto por su id"""


@app.route("/projects/search/<int:id_>")
def search_project(id_):
    try:
        project = Project.query.get_or_404(id_)

        user_id = project.user_id

        return jsonify([project.serialize()])
    except:
        return jsonify({"server": "ERROR"})
