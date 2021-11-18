import sys, os, tempfile, pytest, json
import app
import apps.projects.services as services
import datetime
from pprint import pprint
from apps.meetings.models import *
from apps.user.models import UserA as User

""" Todas estas "cuentan" como tests de integracion """


def test_meetings_work():
    assert True


def test_meetings_add(client, init_database):
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    assert new_meeting.sprint_id is 1
    app.db.session.commit()


def test_meetings_get_plannings_by_sprint(client, init_database):
    data = dict(sprint_id=1, date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    data = dict(
        planning_id=new_meeting.id,
        subject="sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )
    rv = client.post(
        "/meetings/planning/" + str(new_meeting.id) + "/results/add", data=data
    )
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)

    data = dict(
        planning_id=new_meeting.id,
        subject="sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )
    rv = client.post(
        "/meetings/planning/" + str(new_meeting.id) + "/results/add", data=data
    )

    rv = client.get("/meetings/planning/1", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))

    pprint(response_json)
    assert response_json["planning"]["date"] == "Tue, 03 Mar 2020 00:00:00 GMT"
    assert len(response_json) == 2
    assert len(response_json["results"]) == 2
    app.db.session.commit()


def test_meetings_update(client, init_database):
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    data = dict(sprint_id="2", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.put("/meetings/planning/" + str(new_meeting.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    updated_meeting = Planning.query.get(response_json["id"])

    assert updated_meeting.sprint_id is 2
    app.db.session.commit()


def test_meetings_add_result(client, init_database):
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    data = dict(
        planning_id=new_meeting.id,
        subject="sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )
    rv = client.post(
        "/meetings/planning/" + str(new_meeting.id) + "/results/add", data=data
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    new_result = PlanningResult.query.get(response_json["id"])

    assert new_result.planning_id is new_meeting.id
    app.db.session.commit()


def test_meetings_update_result(client, init_database):
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    data = dict(
        planning_id=new_meeting.id,
        subject="sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )
    rv = client.post(
        "/meetings/planning/" + str(new_meeting.id) + "/results/add", data=data
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    new_result = PlanningResult.query.get(response_json["id"])

    data = dict(
        planning_id=new_meeting.id,
        subject="new sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )

    rv = client.put("/meetings/planning/results/" + str(new_meeting.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))

    updated_result = PlanningResult.query.get(response_json["id"])

    assert updated_result.subject == "new sub"

    app.db.session.commit()


def test_meetings_delete_result(client, init_database):
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    data = dict(
        planning_id=new_meeting.id,
        subject="sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )
    rv = client.post(
        "/meetings/planning/" + str(new_meeting.id) + "/results/add", data=data
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    new_result = PlanningResult.query.get(response_json["id"])

    data = dict(
        planning_id=new_meeting.id,
        subject="new sub",
        activity="act",
        user_story_id="1",
        assigned="bob",
    )

    rv = client.delete("/meetings/planning/results/delete/" + str(new_meeting.id))
    deleted_result = PlanningResult.query.get(new_meeting.id)

    assert deleted_result is None

    app.db.session.commit()


def test_meetings_add_retrospective(client, init_database):
    data = dict(
        sprint_id=1,
        date="Tue, 03 Mar 2020 00:00:00 GMT",
        method="TDD",
        positive="Bueno",
        negative="Malo",
        decision="Bien",
    )
    rv = client.post("/meetings/retrospectives/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_retrospective = Retrospective.query.get(response_json["id"])

    assert new_retrospective.sprint_id == 1
    app.db.session.commit()


def test_meetings_update_retrospective(client, init_database):
    data = dict(sprint_id="1", date="Tue, 03 Mar 2020 00:00:00 GMT")
    rv = client.post("/meetings/planning/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_meeting = Planning.query.get(response_json["id"])

    data = dict(
        sprint_id=1,
        date="Tue, 03 Mar 2020 00:00:00 GMT",
        method="TDD",
        positive="Bueno",
        negative="Malo",
        decision="Bien",
    )
    rv = client.post("/meetings/retrospectives/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_retrospective = Retrospective.query.get(response_json["id"])

    data = dict(
        sprint_id=1,
        date="Tue, 03 Mar 2020 00:00:00 GMT",
        method="TDD",
        positive="Mejor",
        negative="Malo",
        decision="Bien",
    )
    rv = client.put("/meetings/retrospectives/" + str(new_retrospective.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))

    updated_retrospective = Retrospective.query.get(response_json["id"])

    assert updated_retrospective.positive == "Mejor"

    app.db.session.commit()


def test_meetings_delete_retrospective(client, init_database):
    data = dict(
        sprint_id=1,
        date="Tue, 03 Mar 2020 00:00:00 GMT",
        method="TDD",
        positive="Bueno",
        negative="Malo",
        decision="Bien",
    )
    rv = client.post("/meetings/retrospectives/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_retrospective = Retrospective.query.get(response_json["id"])

    rv = client.delete(
        "/meetings/retrospectives/delete/" + str(new_retrospective.id), data=data
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    deleted_retrospective = Retrospective.query.get(new_retrospective.id)

    assert deleted_retrospective is None
    app.db.session.commit()


def test_meetings_add_daily(client, init_database):
    data = dict(date="Tue, 03 Mar 2020 00:00:00 GMT", sprint_id=1, report="TDD",)
    rv = client.post("/meetings/dailies/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_daily = Daily.query.get(response_json["id"])

    assert new_daily.sprint_id == 1
    app.db.session.commit()


def test_meetings_update_daily(client, init_database):
    data = dict(date="Tue, 03 Mar 2020 00:00:00 GMT", sprint_id=1, report="TDD",)
    rv = client.post("/meetings/dailies/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_daily = Daily.query.get(response_json["id"])

    data = dict(date="Tue, 03 Mar 2020 00:00:00 GMT", sprint_id=1, report="DDT",)

    rv = client.put("/meetings/dailies/" + str(new_daily.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))

    updated_daily = Daily.query.get(response_json["id"])

    assert updated_daily.report == "DDT"

    app.db.session.commit()


def test_meetings_delete_daily(client, init_database):
    data = dict(date="Tue, 03 Mar 2020 00:00:00 GMT", sprint_id=1, report="TDD",)
    rv = client.post("/meetings/dailies/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_daily = Daily.query.get(response_json["id"])

    rv = client.delete("/meetings/dailies/delete/" + str(new_daily.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    deleted_daily = Daily.query.get(new_daily.id)

    assert deleted_daily is None
    app.db.session.commit()


def test_meetings_search_daily(client, init_database):
    data = dict(date="Tue, 03 Mar 2020 00:00:00 GMT", sprint_id=1, report="TDD",)
    rv = client.post("/meetings/dailies/add", data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    new_daily = Daily.query.get(response_json["id"])

    rv = client.get("/meetings/dailies/search/" + str(new_daily.id), data=data)
    response_json = json.loads(rv.data.decode("utf-8"))
    searched_daily = Daily.query.get(new_daily.id)

    assert new_daily == searched_daily
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

    user1 = User("bob33", "BOB", "dylan", "emprendedor", "123")
    user2 = User("bob44", "bob", "esponja", "cocinero", "123")

    app.db.session.add(user1)
    app.db.session.add(user2)

    app.db.session.commit()

    yield app.db

    app.db.drop_all()
