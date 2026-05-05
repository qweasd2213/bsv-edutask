# assignment 3
import pytest
from unittest.mock import patch
from src.util.dao import DAO

# ---FIXTURE---
@pytest.fixture
def dao_fixture():
    dao = DAO("user") # get dao object
    yield dao # wait for test to run
    dao.drop() # drop to reset dao

# ---TESTS---
#test1
@pytest.mark.integration
def test_create_valid(dao_fixture):
    dao = dao_fixture

    user_data_valid = {
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com"
    }

    result = dao.create(user_data_valid)

    # check _id exists and data is correct
    assert "_id" in result
    assert result["firstName"] == "Winter"
    assert result["lastName"] == "Burger"
    assert result["email"] == "zee3d.contact@gmail.com"

#test 2
@pytest.mark.integration
def test_create_missing_required(dao_fixture):
    dao = dao_fixture

    user_data_missing_field = {
        "firstName": "Winter",
        "lastName": "Burger",
    }

    with pytest.raises(Exception):
        dao.create(user_data_missing_field)

#test 3
@pytest.mark.integration
def test_create_invalid_datatype(dao_fixture):
    dao = dao_fixture

    user_data_missing_field = {
        "firstName": 123,
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com"
    }

    with pytest.raises(Exception):
        dao.create(user_data_missing_field)

#test 4
@pytest.mark.integration
def test_create_duplicate(dao_fixture):
    dao = dao_fixture

    user_data_1 = {
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com"
    }

    user_data_2 = {
        "firstName": "Winter",
        "lastName": "Burger",
        "email": "zee3d.contact@gmail.com"
    }

    dao.create(user_data_1)

    with pytest.raises(Exception):
        dao.create(user_data_2)

#test 5
@pytest.mark.integration
def test_create_empty(dao_fixture):
    dao = dao_fixture

    no_data = {
    }

    with pytest.raises(Exception):
        dao.create(no_data)
