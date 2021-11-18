import os, enum
from datetime import datetime
from app import db
from apps.user.models import UserA
from apps.sprints.models import Sprint


class PlanningResult(db.Model):
    __tablename__ = "planningResults"

    id = db.Column(db.Integer, primary_key=True)
    planning_id = db.Column(db.Integer, db.ForeignKey("plannings.id"))
    subject = db.Column(db.Text)
    activity = db.Column(db.Text)
    user_story_id = db.Column(db.Text)
    assigned = db.Column(db.Text)

    def __init__(self, planning_id, subject, activity, user_story_id, assigned):
        self.planning_id = planning_id
        self.subject = subject
        self.activity = activity
        self.user_story_id = user_story_id
        self.assigned = assigned

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "activity": self.activity,
            "user_story_id": self.user_story_id,
            "assigned": self.assigned,
        }


class Planning(db.Model):
    __tablename__ = "plannings"

    id = db.Column(db.Integer, primary_key=True)
    results = db.relationship("PlanningResult", backref="planning")
    date = db.Column(db.DateTime, nullable=False)
    ###### RELACIONES CON SPRINT
    # relacion one sprint - one planning meeting
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))

    def __init__(self, sprint_id, date):
        self.sprint_id = sprint_id
        self.date = date

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {"id": self.id, "sprint_id": self.sprint_id, "date": self.date}


class Daily(db.Model):
    __tablename__ = " dailies"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    report = db.Column(db.Text)
    # Relacion 1 sprint - n reuniones diarias
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))

    def __init__(self, sprint_id, date, report):
        self.sprint_id = sprint_id
        self.date = date
        self.report = report

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "sprint_id": self.sprint_id,
            "date": self.date,
            "report": self.report,
        }


class Retrospective(db.Model):
    __tablename__ = "retrospectives"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    method = db.Column(db.Text)
    positive = db.Column(db.Text)
    negative = db.Column(db.Text)
    decision = db.Column(db.Text)
    # Relacion 1 sprint - n reuniones de retrospectiva
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))

    def __init__(self, sprint_id, date, method, positive, negative, decision):
        self.sprint_id = sprint_id
        self.date = date
        self.method = method
        self.positive = positive
        self.negative = negative
        self.decision = decision

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "sprint_id": self.sprint_id,
            "date": self.date,
            "method": self.method,
            "positive": self.positive,
            "negative": self.negative,
            "decision": self.decision,
        }
