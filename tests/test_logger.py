import sys, os, tempfile, pytest, json
import app
from mixer.backend.flask import mixer

from apps.user.models import UserA as User
from apps.logger.models import Logger, LoggerEvents
from apps.logger.services import add_event_logger

from mixer.backend.sqlalchemy import Mixer


def test_logger_work():
    assert True


def test_getall_logs(client, init_database):
    # se inicializan dos logs temporales
    logger_0 = add_event_logger(1, LoggerEvents.add_project, "PROJECTS")
    logger_1 = add_event_logger(1, LoggerEvents.add_task, "TASKS")

    # se llama al servicio
    rv = client.get("/logger/getall")

    # se deserializa el response
    response = json.loads(rv.data.decode("utf-8"))

    # si retorna 2 logs funciona
    assert len(response) == 2
    app.db.session.commit()


def test_delete_log(client, init_database):
    # se crea un log temporal
    logger_0 = add_event_logger(1, LoggerEvents.add_project, "PROJECTS")
    log_id = str(logger_0.split("=")[1])

    # se llama al servicio
    rv = client.get("/logger/delete/" + log_id)

    # se deserializa el response
    response_json = json.loads(rv.data.decode("utf-8"))

    # se trata de hacer un get por ese id
    deleted_log = Logger.query.get(log_id)

    # se comprueba que el log no existe
    assert deleted_log is None
    app.db.session.commit()


@pytest.fixture
def client():
    db_fd, app.app.config["DATABASE"] = tempfile.mkstemp()
    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            yield client

    os.close(db_fd)
    os.unlink(app.app.config["DATABASE"])


@pytest.fixture
def init_database():
    app.db.create_all()

    user1 = User("bob3", "bob", "dylan", "emprendedor", "123")
    user2 = User("bob4", "bob", "esponja", "cocinero", "123")

    app.db.session.add(user1)
    app.db.session.add(user2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()
