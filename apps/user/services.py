import os
from app import db, app
from .models import UserA
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger
from flask import request, jsonify, json
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    current_user,
)
import datetime

jwt = JWTManager(app)
MODULE = "Usuario"

# Provide json body with username, first_name, last_name, role and password
@app.route("/user/register", methods=["POST"])
def register():
    request_link = False

    if not request.is_json:
        try:
            username = request.args.get("username")
            first_name = request.args.get("first_name")
            last_name = request.args.get("last_name")
            role = request.args.get("role")
            password = request.args.get("password")
            request_link = True
            print(1)
        except Exception as e:
            return jsonify({"msg": "Missing JSON in request"}), 400

    if request_link:
        try:
            print(2)
            print(username, first_name)
            user = UserA(
                username=username,
                first_name=first_name,
                last_name=last_name,
                role=role,
                password=password,
            )
            print(3, user)
            db.session.add(user)
            db.session.commit()

            ############Agregando evento al logger#########################
            add_event_logger(user.id, LoggerEvents.user_register, MODULE)
            ###############################################################

            return jsonify(user.serialize()), 200
        except Exception as e:
            print(e)
            return str(e)
    else:

        roles = ["Product Owner", "Scrum Master", "Scrum Team"]
        parameters = {
            "username": None,
            "first_name": None,
            "last_name": None,
            "role": None,
            "password": None,
        }
        parameters = {
            param: request.json.get(param, None) for param in parameters.keys()
        }

        for param, value in parameters.items():
            if not value:
                return jsonify({"msg": "Missing " + param + " parameter"}), 400

        if UserA.query.filter_by(username=parameters["username"]).first():
            return (
                jsonify(
                    {"msg": "Username '" + parameters["username"] + "' already exist"}
                ),
                400,
            )

        if not parameters["role"] in roles:
            return jsonify({"msg": "Role '" + parameters["role"] + "' invalid"}), 400
        try:
            user = UserA(
                username=parameters["username"],
                first_name=parameters["first_name"],
                last_name=parameters["last_name"],
                role=parameters["role"],
                password=parameters["password"],
            )
            db.session.add(user)
            db.session.commit()

            ############Agregando evento al logger#########################
            add_event_logger(user.id, LoggerEvents.user_register, MODULE)
            ###############################################################

            return jsonify(user.serialize()), 200
        except Exception as e:
            return str(e)


@app.route("/user/getall")
def getall():
    try:
        users = UserA.query.all()
        return jsonify([user.serialize() for user in users])
    except Exception as e:
        return str(e)


# Provide json body with username and password parameters
@app.route("/user/login", methods=["POST"])
def login():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    password = request.json.get("password", None)
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = UserA.query.filter_by(username=username).first()

    if (not user) or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    expires = datetime.timedelta(days=365)
    # Identity can be any data that is json serializable

    tokens = {
        "access_token": create_access_token(identity=username, expires_delta=expires),
        "refresh_token": create_refresh_token(identity=username),
        "userId": user.id,
        **user.serialize(),
    }

    ############Agregando evento al logger####################
    add_event_logger(user.id, LoggerEvents.user_login, MODULE)
    ##########################################################

    return jsonify(tokens), 200


# Dont look at it
@app.route("/user/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {"access_token": create_access_token(identity=current_user)}
    return jsonify(ret), 200


# Provide Header with access token and json body with username and new_role parameters
# -H "Authorization" : "Bearer <access_token provided in the login response>"
@app.route("/user/edit", methods=["POST"])
@jwt_required
def edit():
    current_user = (
        UserA.query.filter_by(username=get_jwt_identity()).first().serialize()
    )
    if not current_user["role"] == "Product Owner":
        return (
            jsonify({"msg": current_user.usarname + " does not have privileges"}),
            400,
        )

    username = request.json.get("username", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    roles = ["Product Owner", "Scrum Master", "Scrum Team"]
    new_role = request.json.get("new_role", None)
    if (not new_role) or (not new_role in roles):
        return jsonify({"msg": "Invalid new_role parameter"}), 400

    target = UserA.query.filter_by(username=username).first()
    target.role = new_role
    db.session.commit()

    #############Agregando evento al logger###########################
    add_event_logger(current_user["id"], LoggerEvents.user_role_assign, MODULE)
    ##################################################################

    return jsonify({"msg": username + " role changed to " + new_role}), 200

# Delete users
@app.route("/user/delete", methods=["POST"])
@jwt_required
def delete():
    current_user = (
        UserA.query.filter_by(username=get_jwt_identity()).first().serialize()
    )
    if not current_user["role"] == "Product Owner":
        return (
            jsonify({"msg": current_user["username"] + " does not have privileges"}),
            400,
        )
        
    
    username = request.json.get("username", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    deletedUser = UserA.query.filter_by(username=username).delete()

    if (deletedUser) :
        db.session.commit()
        return jsonify({"msg": "User deleted successfully" }), 200
        
    #############Agregando evento al logger###########################
    add_event_logger(current_user["id"], LoggerEvents.user_delete, MODULE)
    ##################################################################

    return jsonify({"msg": "User not found" }), 404

    

# Provide Header with access token
# -H "Authorization" : "Bearer <access_token provided in the login response>"
@app.route("/user/profiles", methods=["GET"])
@jwt_required
def profiles():
    # Access the identity of the current user with get_jwt_identity

    try:
        current_user = (
            UserA.query.filter_by(username=get_jwt_identity()).first().serialize()
        )
        users = UserA.query.all()
        users = [user.serialize() for user in users]
        temp = {"current_user": current_user, "users": users}
        return jsonify(temp), 200
    except Exception as e:
        return str(e)

# Provide Header with access token and json body with username and new_password parameters
# -H "Authorization" : "Bearer <access_token provided in the login response>"
@app.route("/user/editPassword", methods=["POST"])
@jwt_required
def editPassword():
    current_user = (
        UserA.query.filter_by(username=get_jwt_identity()).first().serialize()
    )
    if not current_user["role"] == "Product Owner":
        return (
            jsonify({"msg": current_user.usarname + " does not have privileges"}),
            400,
        )

    username = request.json.get("username", None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400

    new_password = request.json.get("new_password", None)
    if (not new_password):
        return jsonify({"msg": "Invalid new_password parameter"}), 400

    target = UserA.query.filter_by(username=username).first()
    target.password = new_password
    db.session.commit()

    #############Agregando evento al logger###########################
    add_event_logger(current_user["id"], LoggerEvents.user_role_assign, MODULE)
    ##################################################################

    return jsonify({"msg": username + " password changed"}), 200

