from unittest.mock import Mock

from kokon.functions.user import handle_get_all_users

from tests.helpers import AppDB, UserMock


def test_get_all_users(db):
    request = Mock()
    request.db = AppDB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")
    request.args = {"limit": 10}

    response = handle_get_all_users(request)

    assert response.status_code == 200
    items = response.json["items"]
    assert "email" in items[0]
