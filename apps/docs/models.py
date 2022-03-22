import os, enum
from datetime import datetime
from app import db

# from apps.projects.models import Project
from apps.user.models import UserA


class Documentation(db.Model):
    __tablename__ = "documentation"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    dev_met = db.Column(db.Text, nullable=False)
    version = db.Column(db.Float, nullable=False)
    metaphor = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, nullable=False)
    # project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    teams = db.relationship("Team", secondary="teams")

    def __init__(self, name, dev_met, version, project_id, metaphor):
        self.name = name
        self.dev_met = dev_met
        self.version = version
        self.project_id = project_id
        self.metaphor = metaphor

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        # project = Project.query.get_or_404(self.project_id)
        temp = self.teams
        teams = {}
        for team in temp:
            teams[team.name] = team.serialize()
        return {
            "id": self.id,
            "name": self.name,
            "project": {
                "id": self.project_id,
                "name": "Project " + str(self.project_id),
            },
            "teams": teams,
            "dev_met": self.dev_met,
            "version": self.version,
            "metaphor": self.metaphor,
        }


class Teams(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

    doc = db.relationship(
        "Documentation", backref=db.backref("doc_teams", cascade="all, delete-orphan")
    )
    team = db.relationship(
        "Team", backref=db.backref("teams_team", cascade="all, delete-orphan")
    )


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("userA.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

    user = db.relationship(
        UserA, backref=db.backref("team_users", cascade="all, delete-orphan")
    )
    team = db.relationship(
        "Team", backref=db.backref("team_team", cascade="all, delete-orphan")
    )


class Team(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    docs = db.relationship("Documentation", secondary="teams")
    users = db.relationship(UserA, secondary="users")

    def __init__(self, name):
        self.name = name

    def serialize(self):
        temp = self.users
        users = {}
        for user in temp:
            users[user.username] = user.serialize()
        return {"team id": self.id, "team name": self.name, "users": users}


class CopyRight(db.Model):
    __tablename__ = "copyR"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Intro(db.Model):
    __tablename__ = "intro"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Purpose(db.Model):
    __tablename__ = "purpose"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #"doc = Documentation.query.get_or_404(self.doc_id)"
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Motivation(db.Model):
    __tablename__ = "motivation"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Status(db.Model):
    __tablename__ = "status"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Scope(db.Model):
    __tablename__ = "scope"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
       #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Arq(db.Model):
    __tablename__ = "arq"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    path = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, path):
        self.doc_id = doc_id
        self.path = path

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "path": self.path,
        }


class Diag(db.Model):
    __tablename__ = "diag"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    path = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, path):
        self.doc_id = doc_id
        self.path = path

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "path": self.path,
        }


class Foundation(db.Model):
    __tablename__ = "foundation"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }


class Values(db.Model):
    __tablename__ = "values"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, content):
        self.doc_id = doc_id
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "content": self.content,
        }

class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey("documentation.project_id"), nullable=False)
    date = db.Column(db.Text, nullable=False)
    version = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    teams = db.Column(db.Text, nullable=False)

    def __init__(self, doc_id, date, version, description, teams):
        self.doc_id = doc_id
        self.date = date
        self.version = version
        self.description = description
        self.teams = teams

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        #doc = Documentation.query.get_or_404(self.doc_id)
        return {
            "id": self.id,
            "doc": {"id": str(self.doc_id)},
            "date": self.date,
            "version": self.version,
            "description": self.description,
            "teams": self.teams,
        }
