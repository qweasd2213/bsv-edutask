import pytest
from src.controllers.usercontroller import UserController
import unittest.mock as mock

@pytest.fixture
def sut():
    dao_mock = mock.MagicMock()
    return UserController(dao_mock), dao_mock

@pytest.mark.unit
@pytest.mark.parametrize('invalid_email', ['wronformat.com', '', 'noat',])

def test_get_user_by_email_invalid(sut, invalid_email):
    controller, _ = sut # as ive only used one fixture, to reach my desired return value i need to define the return value = sut to use it
    
    with pytest.raises(ValueError):
        controller.get_user_by_email(invalid_email)

def test_get_user_by_email_one_user(sut):
    controller, dao = sut # assigned both return values a definition

    user = {'email': "test@email.com"}
    dao.find.return_value = [user]

    result = controller.get_user_by_email('test@email.com') # calls function with the test email

    assert result == user # if result find the desired user
    dao.find.assert_called_once_with({'email': "test@email.com"}) # asserts that find is called only once

def test_get_user_by_email_many_users(sut, capsys):
    controller, dao = sut

    user1 = {'email': "test@email.com"}
    user2 = {'email': "test@email.com"} # same email to test multiple users found under same email, expected return = user1
    dao.find.return_value = [user1, user2]

    result = controller.get_user_by_email('test@email.com')

    cap = capsys.readouterr()

    assert result == user1 # if multiple users are found under the same email, return the first (oracle)
    assert 'more than one user found' in cap.out

# ARVID implement test case 6 and 7 here

