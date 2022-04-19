import os
from .models import Process2, Group
from app import db, app
from flask import request, jsonify
from flask_cors import cross_origin

MODULE = "Proceso"

""" Get all processes """
@app.route("/processes/getall")
def get_processes():
    try:
        processes = Process2.query.all()
        return jsonify([process.serialize() for process in processes])
    except Exception as e:
        return str(e)


""" Get all processes by project """
@app.route("/processes/getall/<int:project_id>")
@cross_origin()
def get_processes_by_project(project_id):
    processes = Process2.query.filter_by(project_id=project_id)
    if processes.count() > 0:
        return jsonify([process.serialize() for process in processes])
    else:
        return jsonify([])


""" Add a new process """
@app.route("/processes/add", methods=["POST"])
def add_processes():
    if request.method == "POST":
        name = request.json.get("name", None)
        category = request.json.get("category", None)
        value = request.json.get("value", None)
        group_id = request.json.get("group_id", None)
        project_id = request.json.get("project_id", None)

        try:
            process = Process2(name=name, category=category, value=value, group_id=group_id, project_id=project_id)
            db.session.add(process)
            db.session.commit()

            return jsonify(process.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})


""" Delete a process """
@app.route("/processes/delete/<int:id_>", methods=["DELETE"])
def delete_processes(id_):
    if request.method == "DELETE":
        process = Process2.query.get_or_404(id_)
        try:
            db.session.delete(process)
            db.session.commit()

            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


""" Edit a process """
@app.route("/processes/update/<int:id_>", methods=["PUT"])
def update_processes_name(id_):
    if request.method == "PUT":
        process = Process2.query.get_or_404(id_)
        name = request.json.get("name", None)
        value = request.json.get("value", None)

        process.name = name
        process.value = value
        try:
            db.session.commit()

            return jsonify(process.serialize())
        except:
            return jsonify({"server": "ERROR"})


""" Get all groups """
@app.route("/processes/groups/getall")
def get_all_groups():
    try:
        groups = Group.query.all()
        return jsonify([group.serialize() for group in groups])
    except Exception as e:
        return str(e)


""" Add a new group """
@app.route("/processes/groups/add", methods=["POST"])
def add_group():
    if request.method == "POST":
        name = request.json.get("name", None)

        try:
            group = Group(name=name)
            db.session.add(group)
            db.session.commit()

            return jsonify(group.serialize())
        except Exception as e:
            print(e)
            return jsonify({"server": "ERROR"})

