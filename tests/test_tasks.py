import sys, os, tempfile, pytest, json
import http.client
import app
from mixer.backend.flask import mixer
from datetime import datetime

from apps.user.models import UserA as User
from apps.sprints.models import *
from apps.tasks.models import *


def add_temp_sprint(user, description, project, closed, end_date):
    try:

        sp_date = end_date.split("/")
        date = int(sp_date[0])
        mount = int(sp_date[1])
        year = int(sp_date[2])

        sprint = Sprint(
            user_id=user,
            description=description,
            project_id=project,
            closed=closed,
            end_date=datetime(year, mount, date),
        )
        db.session.add(sprint)
        db.session.commit()
        return [sprint.id, sprint.project_id, sprint.user_id]
    except Exception as e:
        return str(e)


def add_temp_task(description, sprint_id, task_type, task_status, task_class, user_id):
    try:
        task = Task(
            user_id=user_id,
            description=description,
            sprint_id=sprint_id,
            task_type=task_type,
            task_status=task_status,
            task_class=task_class,
        )
        db.session.add(task)
        db.session.commit()
        return [task.id, task.sprint_id]
    except Exception as e:
        return str(e)


def test_get_taskBySprint(client, init_database):
    # creando sprint temporal
    sprint0 = add_temp_sprint(1, "test description", 1, False, "01/01/2020")
    task0 = add_temp_task(
        "test description",
        sprint0[0],
        TaskType.design,
        TaskStatus.init,
        TaskClass.hard,
        1,
    )
    task1 = add_temp_task(
        "test description2",
        sprint0[0],
        TaskType.design,
        TaskStatus.init,
        TaskClass.hard,
        1,
    )

    # se llama al servicio
    rv = client.get("/tasks/getbysprint/" + str(sprint0[0]))

    # se deserializa el response
    tasks = json.loads(rv.data.decode("utf-8"))

    print(tasks)

    # se verifica numero de elementos y si los temporales estan entre ellos
    assert (task0[0] in [elem["id"] for elem in tasks]) and (
        task0[1] in [elem["id"] for elem in tasks]
    )
    assert len(tasks) == 2
    app.db.session.commit()


def test_delete_task(client, init_database):
    # creando sprint y task temporales asociadas
    sprint0 = add_temp_sprint(1, "test description", 1, False, "01/01/2020")
    task0 = add_temp_task(
        "test description",
        sprint0[0],
        TaskType.design,
        TaskStatus.init,
        TaskClass.hard,
        1,
    )

    # se llama al servicio
    rv = client.post("/tasks/delete/" + str(task0[0]))

    # se deserializa el response
    response_json = json.loads(rv.data.decode("utf-8"))

    # se trata de hacer un get por ese id
    deleted_task = AcceptanceCriteria.query.get(task0[0])

    # se comprueba que el log no existe
    assert deleted_task is None
    app.db.session.commit()


def test_add_tasks(client, init_database):

    sprint0 = add_temp_sprint(1, "test description", 1, False, "01/01/2020")

    data = dict(
        user_id=1,
        description="Test description",
        sprint_id=sprint0[0],
        task_type="design",
        task_status="init",
        task_class="hard",
        users=[1, 2],
    )
    url = "/tasks/add"

    response = client.post(url, json=data)

    response_json = json.loads(response.data.decode("utf-8"))
    print(response_json)
    new_task = Task.query.get(response_json["id"])

    assert new_task.description == "Test description"
    assert new_task.sprint_id == sprint0[0]
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

    user1 = User("bob3", "bob", "dylan", "Scrum Team", "123")
    user2 = User("bob4", "bob", "esponja", "Product Owner", "123")
    user2 = User("bob5", "bob", "esponja", "Product Owner", "123")

    app.db.session.add(user1)
    app.db.session.add(user2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()
