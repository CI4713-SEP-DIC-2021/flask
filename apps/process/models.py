import enum
from app import db
from sqlalchemy.orm import relationship

class QualitativeEnum(enum.Enum):
    unachieved="No logrado"
    partially_achieved="Parcialmente logrado -"
    partially_achieved_plus="Parcialmente logrado +"
    mostly_achieved="Logrado en gran medida -"
    mostly_achieved_plus="Logrado en gran medida +"
    totally_achieved="Totalmente logrado"

class ProcessCategory(db.Model):

    __tablename__="processCategory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    groups = relationship("ProcessGroup")

    def __init__(self, name):

        self.name = name

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "groups": [group.serialize() for group in self.groups]
        }

class ProcessGroup(db.Model):

    __tablename__="processGroup"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("processCategory.id"), nullable=False)
    processes = relationship("Process")

    def __init__(self, name, category):

        self.name = name
        self.category = category

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            "category": ProcessCategory.query.get_or_404(self.category).name,
            "processes": [process.serialize() for process in self.processes]
        }

class Process(db.Model):

    __tablename__="process"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group = db.Column(db.Integer, db.ForeignKey("processGroup.id"), nullable=False)
    qualitative_value = db.Column(db.Enum(QualitativeEnum))
    quantitative_value = db.Column(db.Integer)

    def __init__(self, name, group, quantitative_value=None, qualitative_value=None):

        self.name = name
        self.group = group
        self.qualitative_value = qualitative_value
        self.quantitative_value = quantitative_value

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):

        if self.qualitative_value is not None:
            return {
                "id": self.id,
                "name": self.name,
                "group": ProcessGroup.query.get_or_404(self.group).name,
                "value": self.qualitative_value.value
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "group": ProcessGroup.query.get_or_404(self.group).name,
                "value": self.quantitative_value
            }


