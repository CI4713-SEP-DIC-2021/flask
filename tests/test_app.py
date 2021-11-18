import sys, os
import tempfile

import pytest

import app


def test_app_work():
    assert True


def test_app_empty_db(client):
    rv = client.get("/")
    assert rv.data != None


@pytest.fixture
def client():
    db_fd, app.app.config["DATABASE"] = tempfile.mkstemp()
    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            yield client

    os.close(db_fd)
    os.unlink(app.app.config["DATABASE"])
