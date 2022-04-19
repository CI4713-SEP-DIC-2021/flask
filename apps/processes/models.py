import os
from app import db
from apps.projects.models import Project

class Process2(db.Model):
    __tablename__ = "processes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.String(50))
    value = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def __init__(self, name, category, value, group_id, project_id):
        self.name = name
        self.category = category
        self.value = value
        self.group_id = group_id
        self.project_id = project_id

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "value": self.value,
            "group_id": self.group_id,
            "project_id": self.project_id,
        }


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
