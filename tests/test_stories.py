import sys, os, tempfile, pytest, json
import app
import apps.projects.services as services
from apps.stories.models import Story, StoryPriority
from apps.user.models import UserA as User


def test_stories_work():
    assert True


def test_stories_add_story(client, init_database):
    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description", project_id=1, epic=False, priority="high"
        ),
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    new_story = Story.query.get(response_json["id"])

    assert new_story.description == "Test description"
    assert new_story.priority == StoryPriority.high
    app.db.session.commit()


def test_stories_delete_story(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic=False, priority="high"
        ),
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    new_story_id = response_json["id"]
    rv = client.delete("/stories/delete/" + str(new_story_id))
    deleted_story = Story.query.get(new_story_id)

    assert deleted_story is None
    app.db.session.commit()


def test_stories_change_story_epicness(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )

    response_json = json.loads(rv.data.decode("utf-8"))

    new_story_id = response_json["id"]
    rv = client.put(
        "/stories/update/" + str(new_story_id),
        data=dict(
            project_id=1,
            description="Modified description",
            epic="true",
            priority="high",
        ),
    )

    response_json = json.loads(rv.data.decode("utf-8"))
    modified_story = Story.query.get(response_json["id"])

    assert modified_story.epic
    app.db.session.commit()


def test_stories_update_story(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )

    response_json = json.loads(rv.data.decode("utf-8"))

    new_story_id = response_json["id"]
    rv = client.put(
        "/stories/update/" + str(new_story_id),
        data=dict(
            project_id=1,
            description="Modified description",
            epic="true",
            priority="high",
        ),
    )

    response_json = json.loads(rv.data.decode("utf-8"))
    modified_story = Story.query.get(response_json["id"])

    assert modified_story.epic
    app.db.session.commit()


def test_stories_add_to_epic(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="true", priority="high"
        ),
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    parent_story_id = response_json["id"]
    parent_story = Story.query.get(parent_story_id)

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )
    child_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    child_story = Story.query.get(child_story_id)

    rv = client.put(
        "/stories/add_to_epic/" + str(child_story_id) + "/" + str(parent_story_id)
    )

    updated_parent = Story.query.get(parent_story_id)
    updated_child = Story.query.get(child_story_id)

    assert child_story in updated_parent.children
    assert updated_child.parent_id == parent_story_id

    app.db.session.commit()


def test_stories_add_to_non_epic(client, init_database):
    # Prueba tipo Frontera
    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    parent_story_id = response_json["id"]
    parent_story = Story.query.get(parent_story_id)

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )
    child_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    child_story = Story.query.get(child_story_id)

    rv = client.put(
        "/stories/add_to_epic/" + str(child_story_id) + "/" + str(parent_story_id)
    )
    response_json = json.loads(rv.data.decode("utf-8"))
    error_message = response_json["server"]

    assert "ERROR" in error_message

    app.db.session.commit()


def test_stories_remove_from_epic(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic=False, priority="high"
        ),
    )
    parent_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    rv = client.patch("/stories/classification/" + str(parent_story_id))
    parent_story = Story.query.get(parent_story_id)

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic=False, priority="high"
        ),
    )
    child_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    child_story = Story.query.get(child_story_id)

    rv = client.put("/stories/remove_from_epic/" + str(child_story_id))

    updated_parent = Story.query.get(parent_story_id)
    updated_child = Story.query.get(child_story_id)

    assert child_story not in updated_parent.children
    assert updated_child.parent_id is None

    app.db.session.commit()


def test_stories_get_children_from_epic(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="true", priority="high"
        ),
    )
    parent_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    parent_story = Story.query.get(parent_story_id)

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )
    child_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    child_story = Story.query.get(child_story_id)
    rv = client.put(
        "/stories/add_to_epic/" + str(child_story_id) + "/" + str(parent_story_id)
    )
    rv = client.get("/stories/get_children/" + str(parent_story_id))

    children = json.loads(rv.data.decode("utf-8"))

    assert child_story_id in [elem["id"] for elem in children]

    app.db.session.commit()


def test_stories_get_parent_from_child(client, init_database):

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="true", priority="high"
        ),
    )
    parent_story_id = json.loads(rv.data.decode("utf-8"))["id"]

    parent_story = Story.query.get(parent_story_id)

    rv = client.post(
        "/stories/add",
        data=dict(
            description="Test description1", project_id=1, epic="false", priority="high"
        ),
    )
    child_story_id = json.loads(rv.data.decode("utf-8"))["id"]
    child_story = Story.query.get(child_story_id)
    rv = client.put(
        "/stories/add_to_epic/" + str(child_story_id) + "/" + str(parent_story_id)
    )

    rv = client.get("/stories/get_parent/" + str(child_story_id))

    parent = json.loads(rv.data.decode("utf-8"))

    assert parent_story_id == parent["id"]

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
