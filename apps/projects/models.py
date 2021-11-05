import os, enum
from datetime import datetime
from app import db
from apps.user.models import UserA


class ProjectStatus(enum.Enum):
    completed = "completed"
    paused = "paused"
    active = "active"


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("userA.id"))
    status = db.Column(
        db.Enum(ProjectStatus), default=ProjectStatus.active, nullable=False
    )
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, description, status):
        self.description = description
        self.user_id = user_id
        self.status = ProjectStatus.active

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "user_id": self.user_id,
            "status": self.status.value,
            "date_created": self.date_created,
        }
