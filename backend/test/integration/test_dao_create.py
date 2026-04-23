# assignment 3
import pytest
import pymongo
from dotenv import dotenv_values
import uuid
from unittest.mock import patch
from src.util.dao import DAO
from bson.objectid import ObjectId
from datetime import datetime

# ---FIXTURE---
@pytest.fixture
def test_db():
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    db_name = f"test{uuid.uuid4().hex}"#så alla test får en egen db

    #switch to test db by patching
    real_client = pymongo.MongoClient
    def patch_client_with_testDB(*args, **kwargs):
        client = real_client(*args, **kwargs)
        client.edutask = client[db_name]#seting test db instead of edutask
        return client

    with patch('pymongo.MongoClient', side_effect=patch_client_with_testDB):
        yield #wait for tests to run

    # drop test db
    client = pymongo.MongoClient(LOCAL_MONGO_URL)
    client.drop_database(db_name)

# ---TESTS---
#user validator
@pytest.mark.integration
def test_create_valid_user_with_optional():
    dao = DAO("user")

    user_data = { #valid data
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com",
        "tasks": [ObjectId(), ObjectId(), ObjectId()]
    }
    
    # call create method
    result = dao.create(user_data)

    # check _id exists and data is correct
    assert "_id" in result
    assert result["firstName"] == "Winter"
    assert result["lastName"] == "Burger"
    assert result["email"] == "zee3d.contact@gmail.com"
    assert len(result["tasks"]) == 3

@pytest.mark.integration
def test_create_valid_user_no_optional():
    dao = DAO("user")

    user_data = { #valid data
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com"
    }
    
    # call create method
    result = dao.create(user_data)

    # check _id exists and data is correct
    assert "_id" in result
    assert result["firstName"] == "Winter"
    assert result["lastName"] == "Burger"
    assert result["email"] == "zee3d.contact@gmail.com"

@pytest.mark.integration
def test_create_no_email():
    dao = DAO("user")

    user_data = {
        "firstName": "Arvid",
        "lastName": "Stenkvarg"
    }

    with pytest.raises(Exception):
        dao.create(user_data)

@pytest.mark.integration
def test_create_no_firstname():
    dao = DAO("user")

    user_data = {
        "lastName": "Sten",
        "email": "sten@gmail.com"
    }

    with pytest.raises(Exception):
        dao.create(user_data)

@pytest.mark.integration
def test_create_no_lastname():
    dao = DAO("user")

    user_data = {
        "firstName": "Arvid",
        "email": "sten@gmail.com"
    }

    with pytest.raises(Exception):
        dao.create(user_data)

@pytest.mark.integration
def test_create_wrong_name_type():
    dao = DAO("user")

    user_data = {
        "firstName": 123,
        "lastName": "Stenkvarg",
        "email": "stenkvarg@gmail.com"
    }

    with pytest.raises(Exception):
        dao.create(user_data)

@pytest.mark.integration
def test_create_wrong_tasks_type():
    dao = DAO("user")

    user_data = {
        "firstName": "Felix",
        "lastName": "Stenkvarg",
        "email": "stenkvarg@gmail.com",
        "tasks": 123
    }

    with pytest.raises(Exception):
        dao.create(user_data)

@pytest.mark.integration
def test_create_duplicate_email():
    dao = DAO("user")

    user_data_1 = {
        "firstName": "Felix",
        "lastName": "Hammarstrom",
        "email": "cgullmgmt@gmail.com"
    }

    user_data_2 = {
        "firstName": "Arvid",
        "lastName": "Stenkvarg",
        "email": "cgullmgmt@gmail.com"
    }

    dao.create(user_data_1)

    with pytest.raises(Exception):
        dao.create(user_data_2)

#task validator
@pytest.mark.integration
def test_create_valid_task_with_optionals():
    dao = DAO("task")

    obj1 = ObjectId()
    obj2 = ObjectId()
    obj3 = ObjectId()
    obj4 = ObjectId()

    task_data = {
        "title": "watch video 1",
        "description": "video 1 contains school material",
        "startdate": datetime(2026, 4, 22),
        "duedate": datetime(2026, 4, 26),
        "requires": [obj1],
        "categories": ["video", "school"],
        "todos": [obj2, obj3],
        "video": obj4
    }

    result = dao.create(task_data)

    assert "_id" in result
    assert result["title"] == "watch video 1"
    assert result["description"] == "video 1 contains school material"
    assert result["startdate"]["$date"] == "2026-04-22T00:00:00Z"
    assert result["duedate"]["$date"] == "2026-04-26T00:00:00Z"
    assert result["requires"][0]["$oid"] == str(obj1)
    assert result["categories"] == ["video", "school"]
    assert result["todos"][0]["$oid"] == str(obj2)
    assert result["todos"][1]["$oid"] == str(obj3)
    assert result["video"]["$oid"] == str(obj4)

@pytest.mark.integration
def test_create_valid_task_without_optionals():
    dao = DAO("task")

    task_data = {
        "title": "watch video 2",
        "description": "video 2 contains school material"
    }

    result = dao.create(task_data)

    assert "_id" in result
    assert result["title"] == "watch video 2"
    assert result["description"] == "video 2 contains school material"

@pytest.mark.integration
def test_create_task_duplicate_title():
    dao = DAO("task")

    task_data_1 = {
        "title": "watch video 3",
        "description": "video 3 contains fun"
    }

    task_data_2 = {
        "title": "watch video 3",
        "description": "video 3 contains fun"
    }

    dao.create(task_data_1)

    with pytest.raises(Exception):
        dao.create(task_data_2)

@pytest.mark.integration
def test_create_task_invalid_description_type():
    dao = DAO("task")

    task_data = {
        "title": "title1",
        "description": 123
    }

    with pytest.raises(Exception):
        dao.create(task_data)

@pytest.mark.integration
def test_create_task_invalid_startdate_type():
    dao = DAO("task")

    task_data = {
        "title": "title1",
        "description": "very fun vid",
        "startdate": 123
    }

    with pytest.raises(Exception):
        dao.create(task_data)

@pytest.mark.integration
def test_create_task_invalid_requires_type():
    dao = DAO("task")

    task_data = {
        "title": "title1",
        "description": "very fun vid",
        "startdate": datetime(2026, 4, 22),
        "requires": 123
    }

    with pytest.raises(Exception):
        dao.create(task_data)

@pytest.mark.integration
def test_create_task_invalid_video_type():
    dao = DAO("task")

    obj1 = ObjectId()


    task_data = {
        "title": "title1",
        "description": "very fun vid",
        "startdate": datetime(2026, 4, 22),
        "requires": [obj1],
        "video": 123
    }

    with pytest.raises(Exception):
        dao.create(task_data)

@pytest.mark.integration
def test_create_task_no_title():
    dao = DAO("task")

    task_data = {
        "description": "description yay!"
    }

    with pytest.raises(Exception):
        dao.create(task_data)

@pytest.mark.integration
def test_create_task_no_description():
    dao = DAO("task")

    task_data = {
        "title": "title1"
    }

    with pytest.raises(Exception):
        dao.create(task_data)

#todo validator
@pytest.mark.integration
def test_create_todo():
    dao = DAO("todo")

    todo_data = {
        "description": "Walk the dog",
        "done": True
    }

    result = dao.create(todo_data)

    assert "_id" in result
    assert result["description"] == "Walk the dog"
    assert result["done"] == True

@pytest.mark.integration
def test_create_todo_duplicate_description():
    dao = DAO("todo")

    todo_data = {
        "description": "Walk the dog",
        "done": True
    }

    todo_data_duplicate = {
        "description": "Walk the dog",
        "done": True
    }

    dao.create(todo_data)

    with pytest.raises(Exception):
        dao.create(todo_data_duplicate)

@pytest.mark.integration
def test_create_todo_wrong_type():
    dao = DAO("todo")

    todo_data = {
        "description": 123,
        "done": True
    }

    with pytest.raises(Exception):
        dao.create(todo_data)

@pytest.mark.integration
def test_create_todo_wrong_type_done():
    dao = DAO("todo")

    todo_data = {
        "description": "Walk the dog",
        "done": 123
    }

    with pytest.raises(Exception):
        dao.create(todo_data)

@pytest.mark.integration
def test_create_todo_missing_required_field():
    dao = DAO("todo")

    todo_data = {
        "done": True
    }

    with pytest.raises(Exception):
        dao.create(todo_data)

#video validator
@pytest.mark.integration
def test_create_video():
    dao = DAO("video")

    video_data = {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }

    result = dao.create(video_data)

    assert "_id" in result
    assert result["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

@pytest.mark.integration
def test_create_video_wrong_type():
    dao = DAO("video")

    video_data = {
        "url": False
    }

    with pytest.raises(Exception):
        dao.create(video_data)

@pytest.mark.integration
def test_create_video_missing_required_field():
    dao = DAO("video")

    video_data = {
    }

    with pytest.raises(Exception):
        dao.create(video_data)

#Validator independent tests
#extra data test
@pytest.mark.integration
def test_create_user_extra_fields():
    dao = DAO("user")

    user_data = {
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com",
        "tasks": [ObjectId(), ObjectId(), ObjectId()],
        "location": "Sweden",
        "favorite_color": "red40"
    }
    
    result = dao.create(user_data)

    assert "_id" in result
    assert result["firstName"] == "Winter"
    assert result["lastName"] == "Burger"
    assert result["email"] == "zee3d.contact@gmail.com"
    assert len(result["tasks"]) == 3
    assert result["location"] == "Sweden"
    assert result["favorite_color"] == "red40"

#no data test
@pytest.mark.integration
def test_create_user_missing_required_field():
    dao = DAO("user")

    no_data = {
    }

    with pytest.raises(Exception):
        dao.create(no_data)