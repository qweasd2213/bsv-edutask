import pytest
from src.util.helpers import hasAttribute

@pytest.mark.unit
def test_hasAttributeTrue():
    result = hasAttribute({'name': 'Jane'}, 'name')
    assert result == True

@pytest.mark.unit
def test_hasAttributeFalse():
    result = hasAttribute({'name': 'Jane'}, 'age')
    assert result == False

# @pytest.mark.unit
# def test_hasAttributeNone():
#     result = hasAttribute(None, 'age')
#     assert result == False
