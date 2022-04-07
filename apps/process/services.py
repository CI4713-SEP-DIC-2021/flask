import os
from .models import ProcessCategory, ProcessGroup, Process
from app import db, app
from flask import request, jsonify


MODULE = "Procesos"

""" Listar todos los procesos """


@app.route("/process/category/all")
def all_process_category():
    try:
        processCategoryList = ProcessCategory.query.all()
        return jsonify([process.serialize() for process in processCategoryList])
    except Exception as e:
        return str(e)

@app.route("/process/all")
def all_process():
    try:
        processList = Process.query.all()
        return jsonify([process.serialize() for process in processList])
    except Exception as e:
        return str(e)


@app.route("/process/add", methods=["POST"])
def add_process():
    if request.method == "POST":

        name = request.json.get("name", None)
        group = request.json.get("group", None)
        qualitative_value = request.json.get("qualitative_value", None)
        quantitative_value = request.json.get("quantitative_value", None)
        try:
            process = Process(
                name=name, group=group, qualitative_value=qualitative_value, quantitative_value=quantitative_value
            )
            db.session.add(process)
            db.session.commit()

            return jsonify(process.serialize())
        except Exception as e:
            print(e) 
            return jsonify({"server": "ERROR"})


@app.route("/process/delete/<int:id_>", methods=["DELETE"])
def delete_process(id_):
    if request.method == "DELETE":
        process = Process.query.get_or_404(id_)
        try:
            id = process.id
            db.session.delete(process)
            db.session.commit()

            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


@app.route("/process/update/<int:id_>", methods=["PUT"])
def update_process(id_):
    if request.method == "PUT":
        process = Process.query.get_or_404(id_)

        name = request.json.get("name", None)
        group = request.json.get("group", None)
        qualitative_value = request.json.get("qualitative_value", None)
        quantitative_value = request.json.get("quantitative_value", None)

        process.name = name
        process.group = group
        process.qualitative_value = qualitative_value
        process.quantitative_value = quantitative_value
        try:
            db.session.commit()
            return jsonify(process.serialize())
        except:
            return jsonify({"server": "ERROR"})


@app.route("/process/search/<int:id_>")
def search_process(id_):
    try:
        process = Process.query.get_or_404(id_)

        id = process.id
        return jsonify([process.serialize()])
    except:
        return jsonify({"server": "ERROR"})


@app.route("/process/category/add", methods=["POST"])
def add_process_category():
    if request.method == "POST":

        name = request.json.get("name", None)
        try:
            process = ProcessCategory(
                name=name
            )
            db.session.add(process)
            db.session.commit()

            return jsonify(process.serialize())
        except Exception as e:
            print(e) 
            return jsonify({"server": "ERROR"})


@app.route("/process/category/delete/<int:id_>", methods=["DELETE"])
def delete_process_category(id_):
    if request.method == "DELETE":
        process = ProcessCategory.query.get_or_404(id_)
        try:
            id = process.id
            db.session.delete(process)
            db.session.commit()

            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


@app.route("/process/category/update/<int:id_>", methods=["PUT"])
def update_process_category(id_):
    if request.method == "PUT":
        process = Process.query.get_or_404(id_)

        name = request.json.get("name", None)
        groups = request.json.get("groups", None)

        process.name = name
        process.groups = groups
        try:
            db.session.commit()
            return jsonify(process.serialize())
        except:
            return jsonify({"server": "ERROR"})


@app.route("/process/category/search/<int:id_>")
def search_process_category(id_):
    try:
        process = ProcessCategory.query.get_or_404(id_)

        id = process.id
        return jsonify([process.serialize()])
    except:
        return jsonify({"server": "ERROR"})

@app.route("/process/group/all")
def all_process_group():
    try:
        processList = ProcessGroup.query.all()
        return jsonify([process.serialize() for process in processList])
    except Exception as e:
        return str(e)


@app.route("/process/group/add", methods=["POST"])
def add_process_group():
    if request.method == "POST":

        name = request.json.get("name", None)
        category = request.json.get("category", None)
        try:
            process = ProcessGroup(
                name=name, category=category
            )
            db.session.add(process)
            db.session.commit()

            return jsonify(process.serialize())
        except Exception as e:
            print(e) 
            return jsonify({"server": "ERROR"})


@app.route("/process/group/delete/<int:id_>", methods=["DELETE"])
def delete_process_group(id_):
    if request.method == "DELETE":
        process = ProcessGroup.query.get_or_404(id_)
        try:
            id = process.id
            db.session.delete(process)
            db.session.commit()

            return jsonify({"server": "200"})
        except:
            return jsonify({"server": "ERROR"})


@app.route("/process/group/update/<int:id_>", methods=["PUT"])
def update_process_group(id_):
    if request.method == "PUT":
        process = Process.query.get_or_404(id_)

        name = request.json.get("name", None)
        category = request.json.get("category", None)
        processes = request.json.get("processes", None)

        process.name = name
        process.category = category
        process.processes = processes
        try:
            db.session.commit()
            return jsonify(process.serialize())
        except:
            return jsonify({"server": "ERROR"})


@app.route("/process/group/search/<int:id_>")
def search_process_group(id_):
    try:
        process = ProcessGroup.query.get_or_404(id_)

        id = process.id
        return jsonify([process.serialize()])
    except:
        return jsonify({"server": "ERROR"})