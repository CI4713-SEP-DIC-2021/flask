import os, enum
from datetime import datetime
from app import db
from apps.stories.models import *
from apps.user.models import assign, UserA
from apps.sprints.models import *
from sqlalchemy.orm import relationship
import json


class TaskType(enum.Enum):
    develop = "Desarrollo"
    design = "Diseño"
    fix = "Reparar"
    refact = "Refactor"


class TaskStatus(enum.Enum):
    new = "Nueva"
    init = "Iniciada"
    to_test = "Lista para Pruebas"
    ended = "Culminada"


class TaskClass(enum.Enum):
    easy = "Sencilla"
    middle = "Media"
    hard = "Compleja"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    # relacion one task - one story OBLIGATORIO
    # story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    # relacion one task - one sprint OBLIGATORIO
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"), nullable=False)
    task_type = db.Column(db.Enum(TaskType), default=TaskType.develop, nullable=False)
    task_status = db.Column(db.Enum(TaskStatus), default=TaskStatus.new, nullable=False)
    task_class = db.Column(db.Enum(TaskClass), default=TaskClass.easy, nullable=False)
    # init_date = db.Column(db.DateTime, default=datetime.utcnow)
    # end_date = db.Column(db.DateTime)
    # duration = db.Column(db.Integer)
    # est_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("userA.id"))

    def __init__(
        self,
        description,
        sprint_id,
        task_type,
        task_status,
        task_class,
        user_id,
        users=None,
    ):
        self.description = description
        self.sprint_id = sprint_id
        self.task_type = task_type
        self.task_status = task_status
        self.task_class = task_class
        self.user_id = user_id
        self.users = users

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        users = []
        try:
            # assignees = db.query(assign).filter(task_id == self.id)
            resultado = db.engine.execute(
                "select * from assign where task_id =" + str(self.id) + ";"
            )
            for row in resultado:
                user = UserA.query.get_or_404(row.user_id)
                users.append({"id": user.id, "username": user.username})
        except ValueError:
            pass

        return {
            "id": self.id,
            "description": self.description,
            "sprint_id": self.sprint_id,
            "task_type": self.task_type.value,
            "task_status": self.task_status.value,
            "task_class": self.task_class.value,
            "user_id": self.user_id,
            "users": users,
        }
