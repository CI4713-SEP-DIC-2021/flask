import os
from .models import *
from app import db, app
from flask import request, jsonify
from datetime import datetime
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from flask_cors import CORS, cross_origin

MODULE = "Sprint"
cors = CORS(app)


@app.route("/sprint/getbyproject/<project_id>")
def get_sprints_by_project(project_id):
    """
    Funcion que permitira retornar todos los
    sprints por proyectos, destinada
    para la lista general de los mismos.
    
    Responde al url: /sprint/getall/<project_id>
    """
    sprints = Sprint.query.filter_by(project_id=project_id)
    if sprints.count() > 0:
        return jsonify([sprint.serialize() for sprint in sprints])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/sprint/active/<project_id>")
def get_sprint_active_by_project(project_id):

    sprints = Sprint.query.filter_by(project_id=project_id).filter_by(closed=False)
    if sprints.count() > 0:
        return jsonify([sprint.serialize() for sprint in sprints])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/sprint/<sprint_id>")
def get_sprint(sprint_id):

    sprints = Sprint.query.filter_by(id=sprint_id)
    if sprints.count() > 0:
        return jsonify([sprint.serialize() for sprint in sprints])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/sprint/getstories/<sprint_id>")
def get_stories_by_sprint(sprint_id):

    stories = Story.query.filter_by(sprint_id=sprint_id)
    if stories.count() > 0:
        return jsonify([story.serialize() for story in stories])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/criteria/getbystory/<story_id>")
def get_criteria_by_story(story_id):
    """
    Funcion que permitira retornar todos los
    los criterios de aceptacion por historia, destinada
    para la lista general de los mismos.
    
    Responde al url: /criteria/getbystory/<story_id>
    """
    criteria = AcceptanceCriteria.query.filter_by(story_id=story_id)
    if criteria.count() > 0:
        return jsonify([c.serialize() for c in criteria])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/tests/getbystory/<story_id>")
def get_tests_by_story(story_id):
    """
    Funcion que permitira retornar todos los
    los criterios de aceptacion por historia, destinada
    para la lista general de los mismos.
    
    Responde al url: /tests/getbystory/<story_id>
    """
    tests = AcceptanceTest.query.filter_by(story_id=story_id)
    if tests.count() > 0:
        return jsonify([test.serialize() for test in tests])
    else:
        return jsonify({"server": "NO_CONTENT"})


@app.route("/sprint/add", methods=["POST"])
def add_sprint():
    if request.method == "POST":
        description = request.json.get("description")
        project_id = request.json.get("project_id")
        end_date = request.json.get("end_date")
        user_id = request.json.get("user_id")
        sp_date = end_date.split("/")
        date = int(sp_date[0])
        mount = int(sp_date[1])
        year = int(sp_date[2])
        try:
            sprint = Sprint(
                user_id=user_id,
                description=description,
                project_id=project_id,
                closed=False,
                end_date=datetime(year, mount, date),
            )
            db.session.add(sprint)
            db.session.commit()
            ###########Agregando evento al logger#######################
            add_event_logger(user_id, LoggerEvents.add_sprint, MODULE)
            ############################################################
            return jsonify(sprint.serialize()), 200
        except Exception as e:
            print(e)
            return jsonify({"server": e})


@app.route("/criteria/add", methods=["POST"])
def add_criteria():
    if request.method == "POST":
        description = request.json.get("description")
        story_id = request.json.get("story_id")
        user_id = request.json.get("user_id")

        user = UserA.query.get_or_404(user_id)
        if user.role != "Scrum Team":
            return jsonify({"server": "Debe ser Scrum Team"}), 405

        try:
            criteria = AcceptanceCriteria(
                story_id=story_id,
                description=description,
                user_id=user_id,
                approved=False,
            )
            db.session.add(criteria)
            db.session.commit()

            ###########Agregando evento al logger#######################
            add_event_logger(user_id, LoggerEvents.add_criteria, MODULE)
            ############################################################

            return jsonify(criteria.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


@app.route("/criteria/delete/<criteria_id>", methods=["POST"])
def delete_criteria(criteria_id):
    try:
        criteria = AcceptanceCriteria.query.filter_by(id=criteria_id).delete()
        db.session.commit()
        return jsonify(criteria), 200
    except Exception as e:
        return str(e)


@app.route("/tests/add", methods=["POST"])
def add_tests():
    if request.method == "POST":
        description = request.json.get("description")
        story_id = request.json.get("story_id")
        user_id = request.json.get("user_id")

        user = UserA.query.get_or_404(user_id)
        if user.role != "Product Owner":
            return jsonify({"server": "Debe ser Product Owner"}), 405

        try:
            test = AcceptanceTest(
                story_id=story_id,
                description=description,
                user_id=user_id,
                approved=False,
            )
            db.session.add(test)
            db.session.commit()

            ###########Agregando evento al logger#######################
            add_event_logger(user_id, LoggerEvents.add_test, MODULE)
            ############################################################

            return jsonify(test.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


@app.route("/tests/delete/<test_id>", methods=["POST"])
def delete_test(test_id):
    try:
        test = AcceptanceTest.query.filter_by(id=test_id).delete()
        db.session.commit()
        return jsonify(test), 200
    except Exception as e:
        return str(e)


@app.route("/sprint/addstory/<sprint_id>/<story_id>", methods=["GET"])
def add_story_to_sprint(story_id, sprint_id):
    if request.method == "GET":
        try:
            story = Story.query.get_or_404(story_id)
            story.sprint_id = sprint_id
            db.session.commit()
            return jsonify(story.serialize())
        except:
            return jsonify({"server": "ERROR"})


@app.route("/sprint/update/<sprint_id>", methods=["PUT"])
def update_sprint(sprint_id):
    if request.method == "PUT":
        sprint = Sprint.query.get_or_404(sprint_id)

        if request.json.get("description"):
            description = request.json.get("description")
            sprint.description = description

        if request.json.get("closed"):
            print("closed")
            closed = request.json.get("closed")
            sprint.closed = closed

        try:
            db.session.commit()

            ###########Agregando evento al logger##########################
            add_event_logger(sprint.user_id, LoggerEvents.update_sprint, MODULE)
            ###############################################################

            return jsonify(sprint.serialize())
        except:
            return jsonify({"server": "ERROR"})


@app.route("/criteria/update/<criteria_id>", methods=["PUT"])
def update_criteria(criteria_id):
    if request.method == "PUT":
        criteria = AcceptanceCriteria.query.get_or_404(criteria_id)

        if request.json.get("description"):
            description = request.json.get("description")
            criteria.description = description

        if request.json.get("approved"):
            approved = request.json.get("approved")
            criteria.approved = approved

        try:
            db.session.commit()

            ###########Agregando evento al logger##########################
            add_event_logger(criteria.user_id, LoggerEvents.update_criteria, MODULE)
            ###############################################################

            return jsonify(criteria.serialize())
        except:
            return jsonify({"server": "ERROR"})


@app.route("/test/update/<test_id>", methods=["PUT"])
def update_test(test_id):
    if request.method == "PUT":
        test = AcceptanceTest.query.get_or_404(test_id)

        if request.json.get("description"):
            description = request.json.get("description")
            test.description = description

        if request.json.get("approved"):
            approved = request.json.get("approved")
            test.approved = approved

        try:
            db.session.commit()

            ###########Agregando evento al logger##########################
            add_event_logger(test.user_id, LoggerEvents.update_test, MODULE)
            ###############################################################

            return jsonify(test.serialize())
        except:
            return jsonify({"server": "ERROR"})
