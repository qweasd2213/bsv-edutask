# assignment 3
import pytest
import pymongo
from dotenv import dotenv_values
import os
import uuid

from src.util.dao import DAO

@pytest.fixture
def test_db():
    #fixture for test db
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    db_name = f"test{uuid.uuid4().hex}"#så alla test får en egen db

    test_mongo_url = f"{LOCAL_MONGO_URL.rstrip('/')}/{db_name}"

    os.environ['MONGO_URL'] = test_mongo_url

    yield #Wait for test to run

    #drop test db
    client = pymongo.MongoClient(test_mongo_url)
    client.drop_database(db_name)

    #ta bort test URLen så det inte trollar
    del os.environ['MONGO_URL']

@pytest.mark.integration
def test_create_valid(test_db):
    dao = DAO("user")#get the user.json validator

    user_data = { #valid data
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com"
    }
    
    #call create method
    result = dao.create(user_data)

    #check _id exists and data is correct
    assert "_id" in result
    assert result["firstName"] == "Winter"
    assert result["lastName"] == "Burger"
    assert result["email"] == "zee3d.contact@gmail.com"

