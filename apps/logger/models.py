import os, enum
from app import db
from apps.user.models import UserA
from datetime import datetime


class LoggerEvents(enum.Enum):
    add_project = "Agregar Proyecto"
    add_sprint = "Agregar Sprint"
    add_criteria = "Agregar Criterio de Aceptacion"
    add_test = "Agregar Prueba de Aceptacion"
    add_task = "Agregar Tarea"
    update_project = "Modificar Proyecto"
    update_sprint = "Modificar Sprint"
    update_criteria = "Modificar Criterio de Aceptacion"
    update_test = "Modificar Prueba de Aceptacion"
    activate_project = "Activar Proyecto"
    pause_project = "Pausar Proyecto"
    delete_project = "Eliminar Proyecto"
    search_project = "Buscar Proyecto"
    user_register = "Registro"
    user_login = "Inicio de Sesion"
    user_role_assign = "Rol Asignado"
    user_delete = "Usuario Eliminado"


class Logger(db.Model):
    __tablename__ = "logger"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("userA.id"))
    event = db.Column(
        db.Enum(LoggerEvents), default=LoggerEvents.user_login, nullable=False
    )
    date = db.Column(db.DateTime, default=datetime.utcnow)
    loged_module = db.Column(db.String(100), nullable=False)

    def __init__(self, user, event, loged_module):
        self.user = user
        self.event = event
        self.loged_module = loged_module

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "user": UserA.query.get_or_404(self.user).username,
            "event": self.event.value,
            "date": self.date.strftime("%d-%m-%Y"),
            "time": self.date.strftime("%H:%M"),
            "loged_module": self.loged_module,
        }
