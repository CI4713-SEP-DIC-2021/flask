import sys, os, tempfile, pytest, json
import app
import apps.projects.services as services
import datetime
from flask import url_for
from apps.meetings.models import *
from apps.user.models import UserA as User


def test_meetings_work():
    assert True


def test_users_register(client, init_database):
    rv = client.post(
        "/user/register?username=debiaslumen&first_name=Pedro&last_name=Perez&role=Scrum%20Team&password=1234"
    )
    print(rv.data)
    response_json = json.loads(rv.data.decode("utf-8"))

    assert response_json["username"] == "debiaslumen"
    assert response_json["first_name"] == "Pedro"
    assert response_json["last_name"] == "Perez"
    assert response_json["role"] == "Scrum Team"
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
