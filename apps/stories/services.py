import os, sys
from .models import *
from apps.projects.models import Project, ProjectStatus
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from app import db, app
from flask import request, jsonify


MODULE = "Historia"

""" Listar todas las historias de un proyecto """


@app.route("/stories/getall/<int:project_id>")
def get_all_by_project(project_id):
    stories = Story.query.filter_by(project_id=project_id)
    if stories.count() > 0:
        return jsonify([story.serialize() for story in stories])
    else:
        return jsonify({"server": "NO_CONTENT"})


""" Agregar historia """


@app.route("/stories/add", methods=["POST"])
def add_story():
    if request.method == "POST":
        request_data = request.get_json()
        description = request_data["description"]
        project_id = request_data["project_id"]
        priority = request_data["priority"]
        epic_string = request_data["epic"]
        if epic_string == "true":
            epic = True
        else:
            epic = False
        try:
            story = Story(
                project_id=project_id,
                description=description,
                priority=priority,
                epic=epic,
            )
            db.session.add(story)
            db.session.commit()

            ###########Agregando evento al logger#######################
            # add_event_logger(user_id, LoggerEvents.add_project, MODULE)
            ############################################################

            return jsonify(story.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR", "response": e})


""" Eliminar una historia """


@app.route("/stories/delete/<int:id_>", methods=["DELETE"])
def delete_story(id_):
    if request.method == "DELETE":
        story = Story.query.get_or_404(id_)
        try:
            project_id = story.project_id
            db.session.delete(story)
            db.session.commit()

            ###########Agregando evento al logger###########################
            # add_event_logger(user_id, LoggerEvents.delete_project, MODULE)
            ################################################################

            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


"""Buscar un proyecto por su id"""


@app.route("/stories/search/<int:id_>")
def search_story(id_):
    try:
        story = Story.query.get_or_404(id_)

        project_id = story.project_id
        ###########Agregando evento al logger###########################
        # add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        ################################################################

        return jsonify([story.serialize()])
    except:
        return jsonify({"server": "ERROR"})


""" Modificar una historia """


@app.route("/stories/update/<int:id_>", methods=["PUT"])
def update_story(id_):
    if request.method == "PUT":
        story = Story.query.get_or_404(id_)
        request_data = request.get_json()
        description = request_data["description"]
        project_id = request_data["project_id"]
        priority = request_data["priority"]
        epic_string = request_data["epic"]
        if epic_string == "true":
            epic = True
        else:
            epic = False

        done_string = request_data["done"]
        if done_string == "true":
            done = True
        else:
            done = False

        story.description = description
        story.project_id = project_id
        story.epic = epic
        story.priority = priority
        story.done = done
        try:
            db.session.commit()

            ###########Agregando evento al logger##########################
            # add_event_logger(user_id, LoggerEvents.update_project, MODULE)
            ###############################################################

            return jsonify(story.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR", "response": e})


"""Agrega historia a una epica"""


@app.route("/stories/add_to_epic/<int:story_id>/<int:epic_id>", methods=["PUT"])
def add_to_epic(story_id, epic_id):
    if request.method == "PUT":
        try:
            story = Story.query.get_or_404(story_id)
            new_parent = Story.query.get_or_404(epic_id)

            if new_parent.epic:
                new_parent.children.append(story)
                story.parent_id = new_parent.id
            else:
                return jsonify({"server": "ERROR: Parent is not epic"})
            db.session.commit()
            ###########Agregando evento al logger###########################
            # add_event_logger(user_id, LoggerEvents.search_project, MODULE)
            ################################################################

            return jsonify(story.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


"""Elimina historia a una epica"""


@app.route("/stories/remove_from_epic/<int:story_id>/", methods=["DELETE"])
def remove_from_epic(story_id):
    if request.method == "DELETE":
        try:
            story = Story.query.get_or_404(story_id)
            parent = Story.query.get_or_404(story.parent_id)
            if parent.epic:
                parent.children.remove(story_id)
                story.parent_id = None
            else:
                return jsonify({"server": "ERROR: Parent is not epic"})
            db.session.commit()
            ###########Agregando evento al logger###########################
            # add_event_logger(user_id, LoggerEvents.search_project, MODULE)
            ################################################################

            return jsonify([parent.serialize()])
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


"""Retorna historias de una epica"""


@app.route("/stories/get_children/<int:id_>")
def get_children_from_epic(id_):
    try:
        parent = Story.query.get_or_404(id_)

        ###########Agregando evento al logger###########################
        # add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        ################################################################

        return jsonify([child.serialize() for child in parent.children])
    except Exception as e:
        print(e)
        return jsonify({"server": "ERROR"})


"""Retorna historias de una epica"""


@app.route("/stories/get_parent/<int:id_>")
def get_parent_from_story(id_):
    try:
        story = Story.query.get_or_404(id_)

        ###########Agregando evento al logger###########################
        # add_event_logger(user_id, LoggerEvents.search_project, MODULE)
        ################################################################
        parent = Story.query.get_or_404(story.parent_id)

        return jsonify(parent.serialize())
    except Exception as e:
        print(e)
        return jsonify({"server": "ERROR"})
