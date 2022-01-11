import os
from datetime import datetime
from .models import *
from apps.sprints.models import *
from app import db, app
from flask import request, jsonify
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from flask_cors import CORS, cross_origin

MODULE = "Reunion"


""" Retorna fecha de reunion de planning y lista de resultados de un sprint """


@app.route("/meetings/planning/<int:sprint_id>", methods=["GET"])
def get_planning_by_sprint(sprint_id):
    if request.method == "GET":
        planning = Planning.query.filter_by(sprint_id=sprint_id).first()
        dic = {"planning": planning.serialize()}
        results = PlanningResult.query.filter_by(planning_id=planning.id)
        if results.count() > 0:
            dic["results"] = [item.serialize() for item in results.all()]
        return jsonify(dic)


""" Agregar planning """


@app.route("/meetings/planning/add", methods=["POST"])
def add_planning():
    if request.method == "POST":
        request_data = request.get_json()
        sprint_id = request_data["sprint_id"]
        date = datetime.strptime(request_data["date"], "%d/%m/%Y")

        try:
            planning = Planning(sprint_id=sprint_id, date=date)
            db.session.add(planning)

            db.session.commit()

            ###########Agregando evento al logger#######################
            # add_event_logger(sprint_id, LoggerEvents.add_planningResult, MODULE)
            ############################################################
            return jsonify(planning.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


""" Modificar planning """


@app.route("/meetings/planning/<int:_id>", methods=["PUT"])
def update_planning(_id):
    if request.method == "PUT":
        planning = Planning.query.get_or_404(_id)
        request_data = request.get_json()
        sprint_id = request_data["sprint_id"]
        date = datetime.strptime(request_data["date"], "%d/%m/%Y")

        planning.sprint_id = sprint_id
        planning.date = date

        db.session.commit()

        ###########Agregando evento al logger#######################
        # add_event_logger(sprint_id, LoggerEvents.add_planningResult, MODULE)
        ############################################################

        return jsonify(planning.serialize())


""" Agregar resultado de planning """


@app.route("/meetings/planning/<int:planning_id>/results/add", methods=["POST"])
def add_planningResult(planning_id):
    if request.method == "POST":
        planning_id = planning_id
        request_data = request.get_json()
        subject = request_data["subject"]
        activity = request_data["activity"]
        user_story_id = request_data["user_story_id"]
        assigned = request_data["assigned"]

        try:
            planningResult = PlanningResult(
                planning_id=planning_id,
                subject=subject,
                activity=activity,
                user_story_id=user_story_id,
                assigned=assigned,
            )
            db.session.add(planningResult)
            db.session.commit()

            ###########Agregando evento al logger#######################
            # add_event_logger(sprint_id, LoggerEvents.add_planningResult, MODULE)
            ############################################################

            return jsonify(planningResult.serialize())
        except:
            return jsonify({"server": "ERROR"})


""" Buscar resultado de planning """


""" Modificar resultado de planning """


@app.route("/meetings/planning/results/<int:id_>", methods=["PUT"])
def update_planningResult(id_):
    if request.method == "PUT":
        result = PlanningResult.query.get_or_404(id_)
        request_data = request.get_json()
        planning_id = request_data["planning_id"]
        subject = request_data["subject"]
        activity = request_data["activity"]
        user_story_id = request_data["user_story_id"]
        assigned = request_data["assigned"]

        result.planning_id = planning_id
        result.subject = subject
        result.activity = activity
        result.user_story_id = user_story_id
        result.assigned = assigned

        db.session.commit()

        ###########Agregando evento al logger##########################
        # add_event_logger(user_id, LoggerEvents.update_planningResult, MODULE)
        ###############################################################

        return jsonify(result.serialize())


""" Eliminar resultado de planning """


@app.route("/meetings/planning/results/delete/<id_>", methods=["DELETE"])
def delete_planningResult(id_):
    if request.method == "DELETE":
        planningResult = PlanningResult.query.get_or_404(id_)
        try:
            db.session.delete(planningResult)
            db.session.commit()

            ###########Agregando evento al logger###########################
            # add_event_logger(user_id, LoggerEvents.delete_daily, MODULE)
            ################################################################

            return jsonify({"server": "200_OK"})
        except:
            return jsonify({"server": "ERROR"})


""" Listar todas las reuniones de retrospectiva de un sprint """


@app.route("/meetings/retrospectives/<int:sprint_id>", methods=["GET"])
def get_retrospectives_by_sprint(sprint_id):
    if request.method == "GET":
        meetings = Retrospective.query.filter_by(sprint_id=sprint_id)
        if meetings.count() > 0:
            return jsonify([meeting.serialize() for meeting in meetings])
        else:
            return jsonify({"server": "NO_CONTENT"})


""" Agregar  reunion de retrospectiva """


@app.route("/meetings/retrospectives/add", methods=["POST"])
def add_retrospective():
    if request.method == "POST":
        request_data = request.get_json()
        sprint_id = request_data["sprint_id"]
        date = datetime.strptime(request_data["date"], "%d/%m/%Y")
        method = request_data["method"]
        positive = request_data["positive"]
        negative = request_data["negative"]
        decision = request_data["decision"]

        try:
            retrospective = Retrospective(
                sprint_id=sprint_id,
                date=date,
                method=method,
                positive=positive,
                negative=negative,
                decision=decision,
            )
            db.session.add(retrospective)
            db.session.commit()

            ###########Agregando evento al logger#######################
            # add_event_logger(sprint_id, LoggerEvents.add_retrospective, MODULE)
            ############################################################

            return jsonify(retrospective.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


""" Buscar reunion de retrospectiva """


""" Modificar reunion de retrospectiva """


@app.route("/meetings/retrospectives/<int:_id>", methods=["PUT"])
def update_retrospective(_id):
    if request.method == "PUT":
        retrospective = Retrospective.query.get_or_404(_id)
        request_data = request.get_json()
        sprint_id = request_data["sprint_id"]
        date = datetime.strptime(request_data["date"], "%d/%m/%Y")
        method = request_data["method"]
        positive = request_data["positive"]
        negative = request_data["negative"]
        decision = request_data["decision"]

        retrospective.sprint_id = sprint_id
        retrospective.date = date
        retrospective.method = method
        retrospective.positive = positive
        retrospective.negative = negative
        retrospective.decision = decision

        db.session.commit()

        ###########Agregando evento al logger#######################
        # add_event_logger(sprint_id, LoggerEvents.add_retrospective, MODULE)
        ############################################################

        return jsonify(retrospective.serialize())


""" Eliminar reunion de retrospectiva """


@app.route("/meetings/retrospectives/delete/<id_>", methods=["DELETE"])
def delete_retrospective(id_):
    if request.method == "DELETE":
        retrospective = Retrospective.query.get_or_404(id_)
        try:
            db.session.delete(retrospective)
            db.session.commit()

            ###########Agregando evento al logger###########################
            # add_event_logger(user_id, LoggerEvents.delete_daily, MODULE)
            ################################################################

            return jsonify({"server": "200_OK"})
        except:
            return jsonify({"server": "ERROR"})


""" Listar todos los dailies de un sprint """


@app.route("/meetings/dailies/<int:sprint_id>", methods=["GET"])
def get_dailies_by_sprint(sprint_id):
    if request.method == "GET":
        meetings = Daily.query.filter_by(sprint_id=sprint_id)
        if meetings.count() > 0:
            return jsonify([meeting.serialize() for meeting in meetings])
        else:
            return jsonify({"server": "NO_CONTENT"})


""" Agregar daily """


@app.route("/meetings/dailies/add", methods=["POST"])
def add_daily():
    if request.method == "POST":
        request_data = request.get_json()
        date = datetime.strptime(request_data["date"], "%d/%m/%Y")
        report = request_data["report"]
        sprint_id = request_data["sprint_id"]

        try:
            daily = Daily(date=date, report=report, sprint_id=sprint_id,)
            db.session.add(daily)
            db.session.commit()

            ###########Agregando evento al logger#######################
            # add_event_logger(sprint_id, LoggerEvents.add_daily, MODULE)
            ############################################################
            return jsonify(daily.serialize())
        except:
            return jsonify({"ERROR": "500_INTERNAL_SERVER_ERROR"})


""" Buscar daily """


@app.route("/meetings/dailies/search/<int:id_>", methods=["GET"])
def search_daily(id_):
    if request.method == "GET":
        daily = Daily.query.get_or_404(id_)
        ###########Agregando evento al logger###########################
        # add_event_logger(daily_id, LoggerEvents.search_daily, MODULE)
        ################################################################
        return jsonify(daily.serialize())


""" Modificar daily """


@app.route("/meetings/dailies/<id_>", methods=["PUT"])
def update_daily(id_):
    if request.method == "PUT":
        daily = Daily.query.get_or_404(id_)
        request_data = request.get_json()
        date = datetime.strptime(request_data["date"], "%d/%m/%Y")
        report = request_data["report"]
        sprint_id = request_data["sprint_id"]

        daily.date = date
        daily.report = report
        daily.sprint_id = sprint_id

        db.session.commit()

        ###########Agregando evento al logger##########################
        # add_event_logger(
        # daily.daily_id, LoggerEvents.update_daily, MODULE)
        ###############################################################

        return jsonify(daily.serialize())


""" Eliminar daily """


@app.route("/meetings/dailies/delete/<id_>", methods=["DELETE"])
def delete_daily(id_):
    if request.method == "DELETE":
        daily = Daily.query.get_or_404(id_)
        try:
            db.session.delete(daily)
            db.session.commit()

            ###########Agregando evento al logger###########################
            # add_event_logger(user_id, LoggerEvents.delete_daily, MODULE)
            ################################################################

            return jsonify({"server": "200_OK"})
        except:
            return jsonify({"server": "ERROR"})
