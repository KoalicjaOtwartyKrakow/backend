from unittest.mock import Mock

from kokon.functions.user import handle_get_all_users
from kokon.utils.db import DB

from tests.helpers import UserMock


def test_get_all_users(db):
    request = Mock()
    request.db = DB()
    request.user = UserMock(guid="782962fc-dc11-4a33-8f08-b7da532dd40d")

    response = handle_get_all_users(request)

    assert response.status_code == 200
    data = response.json
    assert "email" in data[0]
